from datetime import datetime
import time
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydantic import BaseModel, EmailStr, validator
from fastapi import HTTPException, status
import uuid

from app.core.logging import app_logger
from app.utils.emailSettings import get_email_settings
from app.models.email import EmailTemplate, EmailContent
from app.config.email import EmailConfig
from app.exceptions.database import EmailSendError
from app.services.email.smtp import SMTPService, DefaultSMTPClient
from app.services.email.renderer import EmailRenderer, JinjaEmailRenderer


class EmailMetadata(BaseModel):
    """Email metadata for tracking and analytics"""
    message_id: str
    sent_at: datetime
    template: EmailTemplate
    recipient: EmailStr
    status: str
    error: Optional[str] = None
    retry_count: int = 0
    duration: float = 0.0

class TemplateData(BaseModel):
    """Base model for email template data validation"""
    username: str
    url: Optional[str] = None
    expires_in_hours: Optional[int] = None
    
    @validator('username')
    def username_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Username cannot be empty')
        return v

class EmailResult(BaseModel):
    """Result of email sending operation"""
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None
    metadata: Optional[EmailMetadata] = None
    

class RetryConfig(BaseModel):
    """Configuration for email retry mechanism"""
    max_retries: int = 3
    retry_delay: int = 300  # 5 minutes
    backoff_factor: float = 2.0

class EmailService:
    """
    Simplified email service with improved error handling and retry mechanism
    """
    
    def __init__(
        self,
        settings = get_email_settings(),
        renderer: Optional[EmailRenderer] = None,
        smtp_service: Optional[SMTPService] = None,
        email_config: EmailConfig = EmailConfig(),
        retry_config: Optional[RetryConfig] = None,
         
    ):
        self.settings = settings
        self.email_config = email_config
        self.retry_config = retry_config or RetryConfig()
        
        
        # Initialize services
        template_dir = Path(__file__).parent.parent.parent / "templates" / "email"
        self.renderer = renderer or JinjaEmailRenderer(template_dir)
        self.smtp_service = smtp_service or SMTPService(settings, DefaultSMTPClient)
        
        

    

    def _create_message(self, content: EmailContent) -> Tuple[MIMEMultipart, str]:
        try:
            html_content, text_content = self.renderer.render(
                content.template_name.value,
                content.template_data
            )

            message = MIMEMultipart('alternative')
            message['Subject'] = content.subject
            message['From'] = f"{content.from_name or self.settings.MAIL_FROM_NAME} <{content.from_email or self.settings.MAIL_FROM}>"
            message['To'] = content.to_email
            
            # Generate a unique message ID
            message_id = str(uuid.uuid4())
            message['Message-ID'] = f"<{message_id}@{self.settings.MAIL_FROM.split('@')[1]}>"

            message.attach(MIMEText(text_content, 'plain'))
            message.attach(MIMEText(html_content, 'html'))
            
            return message, message_id  # Return both the message and message_id
            
        except Exception as e:
            app_logger.log_error(
                "Failed to create email message",
                error=str(e),
                extra={"template": content.template_name.value}
            )
            raise EmailSendError(f"Failed to create email message: {str(e)}")

    def _get_full_url(self, template: EmailTemplate, token: Optional[str] = None, custom_url: Optional[str] = None) -> str:
        if custom_url:
            return custom_url

        try:
            config = self.email_config.get_template_config(template)
            if not config.url_pattern:
                return self.settings.FRONT_END_URL
            
            path = config.url_pattern.format(token=token) if token else config.url_pattern
            return f"{self.settings.FRONT_END_URL.rstrip('/')}/{path.lstrip('/')}"
            
        except KeyError as e:
            app_logger.log_error(f"Template configuration not found for {template}")
            raise EmailSendError(f"Template configuration not found: {str(e)}")

    def _validate_template_data(self, template: EmailTemplate, data: Dict[str, Any]) -> None:
        try:
            if template in [
                EmailTemplate.ACCOUNT_ACTIVATION,
                EmailTemplate.PASSWORD_RESET,
                EmailTemplate.ACCOUNT_ACTIVATION_CONFIRM,
                EmailTemplate.WELCOME
            ]:
                TemplateData(**data)
        except ValueError as e:
            raise EmailSendError(f"Invalid template data: {str(e)}")

    async def send_email(self, content: EmailContent, retry_count: int = 0) -> EmailResult:
        start_time = time.time()
        
        try:
            
            message, message_id = self._create_message(content)
            await self.smtp_service.send_message(message)
            
            duration = time.time() - start_time
            metadata = EmailMetadata(
                message_id=message_id,
                sent_at=datetime.now(),
                template=content.template_name,
                recipient=content.to_email,
                status="sent",
                retry_count=retry_count,
                duration=duration
            )
            
            
            
            app_logger.log_success(
                "Email sent successfully",
                extra={
                    "message_id": message_id,
                    "template": content.template_name.value,
                    "recipient": content.to_email,
                    "duration": duration
                }
            )
            
            return EmailResult(
                success=True,
                message_id=message_id,
                metadata=metadata
            )
            
        except Exception as e:
            error_msg = str(e)
            duration = time.time() - start_time
            
            if retry_count < self.retry_config.max_retries:
                retry_delay = self.retry_config.retry_delay * (
                    self.retry_config.backoff_factor ** retry_count
                )
                
                app_logger.log_error(
                    f"Email send failed, retrying in {retry_delay}s",
                    extra={
                        "template": content.template_name.value,
                        "recipient": content.to_email,
                        "error": error_msg,
                        "retry_count": retry_count + 1
                    }
                )
                
                
                return await self.send_email(content, retry_count + 1)
            
            metadata = EmailMetadata(
                message_id="",
                sent_at=datetime.now(),
                template=content.template_name,
                recipient=content.to_email,
                status="failed",
                error=error_msg,
                retry_count=retry_count,
                duration=duration
            )
            
           
            
            app_logger.log_error(
                "Failed to send email after retries",
                extra={
                    "template": content.template_name.value,
                    "recipient": content.to_email,
                    "error": error_msg,
                    "duration": duration,
                    "retry_count": retry_count
                }
            )
            
            return EmailResult(
                success=False,
                error=error_msg,
                metadata=metadata
            )

    async def send_template_email(
        self,
        template: EmailTemplate,
        to_email: EmailStr,
        template_data: Dict[str, Any],
        token: Optional[str] = None,
        custom_url: Optional[str] = None,
        email_type: str = "generic"
    ) -> EmailResult:
        """
        Send an email using a specified template.

        Args:
            template (EmailTemplate): The email template to use.
            to_email (EmailStr): The recipient's email address.
            template_data (Dict[str, Any]): The data to populate the template.
            token (Optional[str]): An optional token for the email.
            custom_url (Optional[str]): An optional custom URL to include in the email.
            email_type (str): The type of email to send (e.g., "confirmation", "generic").

        Returns:
            EmailResult: The result of the email send operation.
        """
        try:
            config = self.email_config.get_template_config(template)
            full_template_data = dict(template_data)
            url = self._get_full_url(template, token, custom_url)
            full_template_data["url"] = url
            
            if config.expires_in_hours:
                full_template_data["expires_in_hours"] = config.expires_in_hours
            
            self._validate_template_data(template, full_template_data)
            
            content = EmailContent(
                subject=config.subject,
                template_name=template,
                template_data=full_template_data,
                to_email=to_email
            )
            
            return await self.send_email(content)
            
        except EmailSendError:
            raise
        except Exception as e:
            raise EmailSendError(f"Failed to send {email_type} email: {str(e)}")

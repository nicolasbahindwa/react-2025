from typing import Optional, Dict, Any, Protocol
from pathlib import Path
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from pydantic import EmailStr
from app.core.logging import app_logger
from app.utils.emailSettings import get_email_settings
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import asyncio
from functools import wraps
from app.exceptions.database import EmailSendError
import time

class EmailTemplate(Enum):
    """Enum for email templates to avoid string literals"""
    ACCOUNT_ACTIVATION = "account_activation"
    PASSWORD_RESET = "password_reset"
    WELCOME = "welcome"
    ACCOUNT_ACTIVATION_CONFIRM = "account_activation_confirm"
    # Add other templates here

@dataclass
class EmailContent:
    """Data class for email content"""
    subject: str
    template_name: EmailTemplate
    template_data: Dict[str, Any]
    to_email: EmailStr
    from_name: Optional[str] = None
    from_email: Optional[str] = None

class SMTPClient(Protocol):
    """Protocol for SMTP client implementations"""
    async def connect(self) -> None: ...
    async def starttls(self) -> None: ...
    async def login(self, username: str, password: str) -> None: ...
    async def send_message(self, message: MIMEMultipart) -> None: ...
    async def quit(self) -> None: ...

class EmailRenderer(ABC):
    """Abstract base class for email rendering"""
    @abstractmethod
    def render(self, template_name: str, template_data: Dict[str, Any]) -> tuple[str, str]:
        """Render email templates"""
        pass

class JinjaEmailRenderer(EmailRenderer):
    """Jinja2 implementation of email renderer"""
    def __init__(self, template_dir: Path):
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True
        )

    def render(self, template_name: str, template_data: Dict[str, Any]) -> tuple[str, str]:
        html_content = self._render_template(f"{template_name}.html", template_data)
        text_content = self._render_template(f"{template_name}.txt", template_data)
        return html_content, text_content

    def _render_template(self, template_file: str, data: Dict[str, Any]) -> str:
        try:
            template = self.jinja_env.get_template(template_file)
            return template.render(**data)
        except Exception as e:
            app_logger.log_error(f"Template rendering failed: {str(e)}", 
                           extra={"template": template_file})
            raise

def retry_on_connection_error(max_retries: int = 3, delay: float = 1.0):
    """Decorator for handling SMTP connection retries"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except (aiosmtplib.SMTPConnectError, 
                        aiosmtplib.SMTPServerDisconnected) as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        await asyncio.sleep(delay * (attempt + 1))
            raise last_exception
        return wrapper
    return decorator

class EmailService:
    """Email service with dependency injection and proper separation of concerns"""
    
    def __init__(
        self,
        settings = get_email_settings(),
        renderer: Optional[EmailRenderer] = None,
        smtp_client: Optional[SMTPClient] = None
    ):
        """Initialize with dependencies"""
        self.settings = settings
        template_dir = Path(__file__).parent.parent / "templates" / "email"
        self.renderer = renderer or JinjaEmailRenderer(template_dir)
        self.smtp_client = smtp_client or aiosmtplib.SMTP

    def _create_message(self, content: EmailContent) -> MIMEMultipart:
        """Create email message with both HTML and plain text versions"""
        html_content, text_content = self.renderer.render(
            content.template_name.value,
            content.template_data
        )
        print(self.settings.SMTP_PASSWORD)
        message = MIMEMultipart('alternative')
        message['Subject'] = content.subject
        message['From'] = f"{content.from_name or self.settings.MAIL_FROM_NAME} <{content.from_email or self.settings.MAIL_FROM}>"
        message['To'] = content.to_email

        message.attach(MIMEText(text_content, 'plain'))
        message.attach(MIMEText(html_content, 'html'))
        
        return message

    @retry_on_connection_error()
    async def _send_smtp(self, message: MIMEMultipart) -> None:
        """Send email via SMTP with retry mechanism"""
        smtp = self.smtp_client(
            hostname=self.settings.SMTP_HOST,
            port=self.settings.SMTP_PORT,
            use_tls=self.settings.SMTP_USE_TLS
        )
        
        try:
            await smtp.connect()
            if self.settings.SMTP_USE_TLS:
                await smtp.starttls()
            await smtp.login(self.settings.SMTP_USER, self.settings.SMTP_PASSWORD)
            
            if self.settings.EMAIL_DEBUG_MODE:
                app_logger.log_success(
                    "Debug Mode: Email sending simulated",
                    extra={
                        "to": message["To"],
                        "subject": message["Subject"],
                        "smtp_host": self.settings.SMTP_HOST,
                    }
                )
                return
                
            await smtp.send_message(message)
            
        finally:
            await smtp.quit()
 
    
    
    async def send_email(self, content: EmailContent) -> bool:
        """Send an email using provided content""" 
        start_time = time.time() 
        try: 
            message = self._create_message(content) 
            await self._send_smtp(message) 
            app_logger.log_success( 
                                   "Email sent successfully",
                                   extra={ "template": content.template_name.value,
                                          "recipient": content.to_email,
                                          "duration": time.time() - start_time } ) 
            print(f"Email to {content.to_email} sent successfully.") 
            return True 
        except EmailSendError as e:
            app_logger.log_error( 
                                 "Failed to send email",
                                 extra={ "template": content.template_name.value,
                                        "recipient": content.to_email, "error": str(e),
                                        "duration": time.time() - start_time } ) 
            print(f"Failed to send email to {content.to_email}: {str(e)}") 
            return False

    

    async def send_activation_email(
        self,
        to_email: EmailStr,
        username: str,
        activation_token: str,
        activation_url: Optional[str] = None
    ) -> bool:
        """Send account activation email"""
        if not activation_url:
            activation_url = f"{self.settings.FRONT_END_URL}/activate/{activation_token}"

        content = EmailContent(
            subject="Activate Your Account",
            template_name=EmailTemplate.ACCOUNT_ACTIVATION,
            template_data={
                "username": username,
                "activation_url": activation_url,
                "token": activation_token,
                "expires_in_hours": 24
            },
            to_email=to_email
        )
        
        return await self.send_email(content)

    async def send_password_reset_email(
        self,
        to_email: EmailStr,
        username: str,
        reset_token: str,
        reset_url: Optional[str] = None
    ) -> bool:
        """Send password reset email"""
        if not reset_url:
            reset_url = f"{self.settings.FRONT_END_URL}/reset-password/{reset_token}"

        content = EmailContent(
            subject="Reset Your Password",
            template_name=EmailTemplate.PASSWORD_RESET,
            template_data={
                "username": username,
                "reset_url": reset_url,
                "token": reset_token,
                "expires_in_hours": 24
            },
            to_email=to_email
        )
        
        return await self.send_email(content)
    

    
    async def send_confirmation_email(
        self,
        to_email: EmailStr,
        username: str
    ) -> bool:
        """Send account confirmation email with login URL"""
        # Construct the login URL (you can customize the URL structure if needed)
        login_url = f"{self.settings.FRONT_END_URL}/login"

        # Prepare the content of the email
        content = EmailContent(
            subject="Please confirm your account",
            template_name=EmailTemplate.ACCOUNT_ACTIVATION_CONFIRM,
            template_data={
                "username": username,
                "login_url": login_url
            },
            to_email=to_email
        )

        # Send the email using the send_email method
        return await self.send_email(content)
# services/email/smtp.py
import aiosmtplib
from email.mime.multipart import MIMEMultipart
from app.core.protocols import SMTPClient
from app.core.decorators import retry_on_connection_error
from app.utils.emailSettings import get_email_settings
from app.core.logging import app_logger

class DefaultSMTPClient(SMTPClient):
    """Default SMTP client implementation"""
    def __init__(self, hostname: str, port: int, use_tls: bool):
        self.client = aiosmtplib.SMTP(hostname=hostname, port=port, use_tls=use_tls)
    
    async def connect(self) -> None:
        await self.client.connect()
    
    async def starttls(self) -> None:
        await self.client.starttls()
    
    async def login(self, username: str, password: str) -> None:
        await self.client.login(username, password)
    
    async def send_message(self, message: MIMEMultipart) -> None:
        await self.client.send_message(message)
    
    async def quit(self) -> None:
        await self.client.quit()

class SMTPService:
    """SMTP service implementation"""
    def __init__(self, settings = get_email_settings(), smtp_client_class = DefaultSMTPClient):
        self.settings = settings
        self.smtp_client_class = smtp_client_class

    @retry_on_connection_error()
    async def send_message(self, message: MIMEMultipart) -> None:
        """Send email via SMTP with retry mechanism"""
        smtp = self.smtp_client_class(
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
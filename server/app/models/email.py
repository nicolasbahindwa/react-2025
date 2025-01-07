from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any
from pydantic import EmailStr

class EmailTemplate(Enum):
    """Enum for email templates to avoid string literals"""
    ACCOUNT_ACTIVATION = "account_activation"
    PASSWORD_RESET = "password_reset"
    WELCOME = "welcome"
    ACCOUNT_ACTIVATION_CONFIRM = "account_activation_confirm"

    @classmethod
    def get_template_name(cls, template: 'EmailTemplate') -> str:
        """Get the template file name without extension"""
        return template.value

@dataclass
class EmailTemplateConfig:
    """Configuration for email templates"""
    subject: str
    expires_in_hours: Optional[int] = None
    url_pattern: Optional[str] = None

    def get_url(self, base_url: str, token: Optional[str] = None) -> str:
        """Generate full URL for the template"""
        if not self.url_pattern:
            return base_url
        
        path = self.url_pattern.format(token=token) if token else self.url_pattern
        return f"{base_url.rstrip('/')}{path}"

@dataclass
class EmailContent:
    """Data class for email content"""
    subject: str
    template_name: EmailTemplate
    template_data: Dict[str, Any]
    to_email: EmailStr
    from_name: Optional[str] = None
    from_email: Optional[str] = None
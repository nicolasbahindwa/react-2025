from app.models.email import EmailTemplate, EmailTemplateConfig
from typing import Dict

class EmailConfig:
    """Centralized email template configurations"""
    TEMPLATES: Dict[EmailTemplate, EmailTemplateConfig] = {
        EmailTemplate.ACCOUNT_ACTIVATION: EmailTemplateConfig(
            subject="Activate Your Account",
            expires_in_hours=24,
            url_pattern="/activate/{token}"
        ),
        EmailTemplate.PASSWORD_RESET: EmailTemplateConfig(
            subject="Reset Your Password",
            expires_in_hours=24,
            url_pattern="/reset-password/{token}"
        ),
        EmailTemplate.ACCOUNT_ACTIVATION_CONFIRM: EmailTemplateConfig(
            subject="Please confirm your account",
            url_pattern="/login"
        ),
        EmailTemplate.WELCOME: EmailTemplateConfig(
            subject="Welcome to our platform"
        )
    }

    @classmethod
    def get_template_config(cls, template: EmailTemplate) -> EmailTemplateConfig:
        """
        Get template configuration for a given template type.
        Raises KeyError if template is not found.
        """
        return cls.TEMPLATES[template]

    @classmethod
    def add_template_config(
        cls, 
        template: EmailTemplate, 
        config: EmailTemplateConfig
    ) -> None:
        """Add or update a template configuration"""
        cls.TEMPLATES[template] = config
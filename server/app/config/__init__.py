from .settings import get_settings  # Import the get_settings function
from .email import EmailConfig

__all__ = ['EmailConfig', 'settings', 'get_settings', 'email']  # Include get_settings in the export list

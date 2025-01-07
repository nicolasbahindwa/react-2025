from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from app.core.logging import app_logger

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
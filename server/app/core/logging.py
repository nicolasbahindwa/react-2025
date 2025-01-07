import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from functools import wraps
from typing import Callable,Any, Optional
from pathlib import Path


class AppLogger:
    """
    Centralized logging configuration for the application.
    Handles both success and error logs with rotation capability.
    """
    def __init__(self, app_name:str='fastapi-app', base_dir:str=None):
        self.app_name = app_name
        if base_dir is None:
            # Use current working directory if no base
            base_dir = os.path.join(os.getcwd(), "logs")

        # Create Path objects
        self.log_dir = Path(base_dir)
        self.success_dir = self.log_dir / "success"
        self.error_dir = self.log_dir / "error"
        
        # Create log directories
        os.makedirs(self.success_dir, exist_ok=True)
        os.makedirs(self.error_dir, exist_ok=True)

       # Create log file paths
        self.success_log_path = self.success_dir / "success.log"
        self.error_log_path = self.error_dir / "error.log"

        # Initialize loggers
        self.success_logger = self._setup_logger(
            name=f"{app_name}_success",
            log_file=str(self.success_log_path),  # Convert Path to string
            level=logging.INFO
        )

        self.error_logger = self._setup_logger(
            name=f"{app_name}_error",
            log_file=str(self.error_log_path),  # Convert Path to string
            level=logging.ERROR
        )
    
    def _setup_logger(
        self,
        name: str,
        log_file: str,
        level: int,
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5
    ) -> logging.Logger:
        """Setup individual logger with rotation"""
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Remove existing handlers if any
        if logger.handlers:
            logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Create rotating file handler
        handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger

    def log_success(self, message: str, extra: dict = None) -> None:
        """Log success messages"""
        if extra:
            self.success_logger.info(f"{message} - Extra: {extra}")
        else:
            self.success_logger.info(message)

    def log_error(self, message: str, error: Exception = None, extra: dict = None) -> None:
        """Log error messages"""
        if error:
            self.error_logger.error(f"{message} - Error: {str(error)}", exc_info=True)
        elif extra:
            self.error_logger.error(f"{message} - Extra: {extra}")
        else:
            self.error_logger.error(message)

    # Create a global logger instance
app_logger = AppLogger()

# Decorator for logging repository operations
def log_operation(operation_name: str):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                app_logger.log_success(
                    f"Successfully executed {operation_name}",
                    extra={"function": func.__name__, "args": str(args), "kwargs": str(kwargs)}
                )
                return result
            except Exception as e:
                app_logger.log_error(
                    f"Error executing {operation_name}",
                    error=e,
                    extra={"function": func.__name__, "args": str(args), "kwargs": str(kwargs)}
                )
                raise
        return wrapper
    return decorator
import asyncio
from functools import wraps
from typing import TypeVar, Callable, Any
from app.core.logging import app_logger

T = TypeVar('T')

def retry_with_backoff(max_retries: int = 3, backoff_factor: int = 2):
    """Retry decorator with exponential backoff"""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        delay = (backoff_factor ** attempt)
                        app_logger.warning(
                            f"Email send attempt {attempt + 1} failed, retrying in {delay}s",
                            extra={"error": str(e)}
                        )
                        await asyncio.sleep(delay)
                    else:
                        app_logger.error(
                            f"Email send failed after {max_retries} attempts",
                            extra={"error": str(e)}
                        )
            raise last_exception
        return wrapper
    return decorator
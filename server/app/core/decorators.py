from functools import wraps
import asyncio
import aiosmtplib

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
from functools import wraps
from fastapi import HTTPException, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from datetime import datetime, timezone, timedelta
from typing import Callable, Optional, Dict, Type
from collections import defaultdict
import time
from dataclasses import dataclass
import logging
from app.database import get_db
from app.models.blocked_ip import BlockedIP

logger = logging.getLogger(__name__)

@dataclass
class RateWindow:
    count: int = 0
    start_time: float = time.time()

class RateLimitConfig:
    def __init__(
        self,
        max_requests: int,
        window_seconds: int,
        block_minutes: int,
        endpoints: Optional[list[str]] = None
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.block_minutes = block_minutes
        self.endpoints = endpoints or []

class AsyncRateLimiter:
    """
    Asynchronous rate limiter with database persistence for blocked IPs
    """
    _instance = None
    _windows: Dict[str, Dict[str, RateWindow]] = defaultdict(lambda: defaultdict(RateWindow))

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Skip initialization if already initialized
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        self._cleanup_task = None

    async def _get_db_session(self) -> AsyncSession:
        """Get database session"""
        async for session in get_db():
            return session

    async def is_ip_blocked(self, ip: str, session: AsyncSession) -> bool:
        """Check if IP is blocked in database"""
        stmt = select(BlockedIP).where(BlockedIP.ip == ip)
        result = await session.execute(stmt)
        blocked_ip = result.scalar_one_or_none()
        
        if blocked_ip and blocked_ip.is_blocked():
            return True
        elif blocked_ip:
            # Clean up expired block
            await session.delete(blocked_ip)
            await session.commit()
        return False

    async def block_ip(self, ip: str, minutes: int, session: AsyncSession) -> None:
        """Block IP in database"""
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=minutes)
        blocked_ip = BlockedIP(
            ip=ip,
            blocked_at=datetime.now(timezone.utc),
            expires_at=expires_at
        )
        session.add(blocked_ip)
        await session.commit()
        logger.warning(f"IP {ip} blocked until {expires_at}")

    async def _clean_expired_windows(self, window_seconds: int) -> None:
        """Clean expired rate windows"""
        current_time = time.time()
        for endpoint in list(self._windows.keys()):
            for ip in list(self._windows[endpoint].keys()):
                window = self._windows[endpoint][ip]
                if current_time - window.start_time >= window_seconds:
                    del self._windows[endpoint][ip]

    def rate_limit(
        self,
        max_requests: int = 5,
        window_seconds: int = 60,
        block_minutes: int = 15
    ) -> Callable:
        """
        Rate limiting decorator that can be applied to FastAPI route handlers
        
        Args:
            max_requests: Maximum number of requests allowed in the window
            window_seconds: Time window in seconds
            block_minutes: How long to block the IP if limit is exceeded
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Extract request from args or kwargs
                request = next((arg for arg in args if isinstance(arg, Request)), 
                             kwargs.get('request'))
                
                if not request:
                    raise ValueError("No Request object found in handler arguments")

                ip = request.client.host
                endpoint = request.url.path

                # Get database session
                session = await self._get_db_session()

                # Check if IP is already blocked
                if await self.is_ip_blocked(ip, session):
                    raise HTTPException(
                        status_code=429,
                        detail={
                            "error": "IP is blocked due to excessive requests",
                            "try_again_after": "15 minutes"
                        }
                    )

                # Clean expired windows periodically
                await self._clean_expired_windows(window_seconds)

                # Check rate limit
                window = self._windows[endpoint][ip]
                current_time = time.time()

                # Reset window if expired
                if current_time - window.start_time >= window_seconds:
                    window.count = 0
                    window.start_time = current_time

                window.count += 1

                # Block IP if limit exceeded
                if window.count > max_requests:
                    await self.block_ip(ip, block_minutes, session)
                    del self._windows[endpoint][ip]
                    raise HTTPException(
                        status_code=429,
                        detail={
                            "error": "Too many requests",
                            "try_again_after": f"{block_minutes} minutes"
                        }
                    )

                # Execute the route handler
                return await func(*args, **kwargs)

            return wrapper
        return decorator

# Create a global instance
rate_limiter = AsyncRateLimiter()
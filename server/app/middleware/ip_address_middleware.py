from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Final

class IPAddressMiddleware(BaseHTTPMiddleware):
    X_FORWARDED_FOR: Final[str] = "X-Forwarded-For"
    
    async def dispatch(self, request: Request, call_next):
        client_ip = self._get_client_ip(request)
        request.state.client_ip = client_ip
        return await call_next(request)
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request headers or client host"""
        if x_forwarded_for := request.headers.get(self.X_FORWARDED_FOR):
            return x_forwarded_for.split(",")[0].strip()
        return request.client.host
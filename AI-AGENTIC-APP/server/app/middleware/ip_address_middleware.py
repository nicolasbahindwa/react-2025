from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class IPAddressMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Check if X-Forwarded-For header exists
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        if x_forwarded_for:
            # The header can contain a list of IPs, we take the first one
            client_ip = x_forwarded_for.split(",")[0].strip()
        else:
            # Fallback to the request's client host (127.0.0.1 if local)
            client_ip = request.client.host
        
        # Store the IP address in request.state for easy access
        request.state.client_ip = client_ip
        
        # Proceed with the request
        response = await call_next(request)
        return response
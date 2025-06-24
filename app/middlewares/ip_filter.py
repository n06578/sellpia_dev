from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException

class IPFilterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        allowed_ips = ["127.0.0.1", "testclient"]

        print("💡 Middleware IP 확인:", client_ip)

        if client_ip not in allowed_ips:
            raise HTTPException(status_code=403, detail=f"Access forbidden from IP {client_ip}")

        response = await call_next(request)
        return response
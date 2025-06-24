# YTEST: 인증 및 인가 로직
from fastapi import Request, HTTPException, status
from ipaddress import ip_address, ip_network
from app.core.config import settings
from typing import Callable

def get_ip_address_from_request(request: Request) -> str:
    """클라이언트의 IP 주소를 반환합니다. X-Forwarded-For 헤더를 우선적으로 사용합니다."""
    # YTEST: 실제 운영 환경에서는 프록시 설정에 따라 IP 주소를 가져오는 방식이 달라질 수 있습니다.
    if "x-forwarded-for" in request.headers:
        ip_addresses = request.headers["x-forwarded-for"].split(',')
        print("ip_addresses : ",ip_addresses)
        return ip_addresses[0].strip() # YTEST: 첫 번째 IP 주소를 클라이언트 IP로 간주
    return request.client.host

def require_ip_range_auth(request: Request) -> bool:
    """요청 IP 주소가 허용된 IP 대역에 속하는지 확인합니다."""
    # YTEST: 특정 IP 대역에서만 접근을 허용하는 인증 로직
    client_ip = get_ip_address_from_request(request)
    if not client_ip:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not determine client IP address."
        )

    try:
        ip = ip_address(client_ip)

        for allowed_range in settings.ALLOWED_IP_RANGES:
            if ip in ip_network(allowed_range):
                return True
    except ValueError:
        # YTEST: 잘못된 IP 주소 또는 대역 포맷 처리
        pass

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access forbidden from this IP address."
    )

def create_auth_dependency(auth_type: str) -> Callable[[Request], bool]:
    """다양한 인증 방식을 동적으로 생성합니다."""
    # YTEST: APIRouter 그룹별 인증 방식 설정을 위한 팩토리 함수
    if auth_type == "ip_range":
        return require_ip_range_auth
    elif auth_type == "key_auth":
        # YTEST: 추후 API Key 인증 로직 추가
        raise NotImplementedError("API Key authentication not yet implemented.")
    else:
        raise ValueError(f"Unknown authentication type: {auth_type}")

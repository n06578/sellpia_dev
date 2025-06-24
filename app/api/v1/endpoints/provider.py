# YTEST: /provider 엔드포인트 예시
# YTEST: /provider 엔드포인트 정의
from fastapi import APIRouter, Depends, HTTPException, status
from app.dtos.provider import ProviderCreateDTO, ProviderUpdateDTO, ProviderResponseDTO
from app.services.provider import ProviderService
from app.repositories.provider import ProviderRepository
from app.core.security import create_auth_dependency # 인증 의존성 생성 함수 임포트
from typing import List

router = APIRouter()

# ProviderService 인스턴스를 생성하고 반환하는 의존성 주입용 함수입니다.
# 이 함수는 ProviderRepository의 인스턴스를 ProviderService에 주입합니다.
def get_provider_service() -> ProviderService:
    return ProviderService(provider_repo=ProviderRepository())

provider_auth_dependency = Depends(create_auth_dependency("ip_range"))


# POST / 요청을 처리하여 새로운 계정을 생성하는 엔드포인트입니다.
# 응답 모델은 AccountResponseDTO이며, 성공 시 상태 코드는 201 (Created)입니다.
# provider_auth_dependency를 통해 이 엔드포인트에 접근하기 전에 인증을 수행합니다.
@router.post("/", response_model=ProviderResponseDTO, status_code=status.HTTP_201_CREATED, dependencies=[provider_auth_dependency])
async def create_provider(
    provider_in: ProviderCreateDTO, # 요청 본문으로 받을 데이터의 DTO (Data Transfer Object)
    provider_service: ProviderService = Depends(get_provider_service) # AccountService 의존성 주입
):
    """
    새로운 계정을 생성합니다.
    - provider_in: 생성할 계정 정보를 담은 DTO.
    - provider_service: 계정 관련 비즈니스 로직을 처리하는 서비스.
    성공 시 생성된 계정 정보를, 실패 시 적절한 HTTP 예외를 반환합니다.
    """
    try:
        # AccountService를 사용하여 계정 생성 로직을 호출합니다.
        new_provider = provider_service.create_provider(provider_in)
        print(new_provider)
        return new_provider
    except ValueError as e:
        # 서비스 계층에서 중복 등의 이유로 ValueError가 발생하면 409 Conflict를 반환합니다.
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        # 그 외 예상치 못한 오류 발생 시 500 Internal Server Error를 반환합니다.
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create provider: {e}")
    return {"message": "Provider created (Auth by IP Range)"}


@router.delete("/{provider_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[provider_auth_dependency])
async def delete_provider(
    provider_id: int, # 경로 매개변수로 받을 삭제할 계정의 ID
    provider_service: ProviderService = Depends(get_provider_service) # ProviderService 의존성 주입
):
    """
    특정 ID의 계정을 삭제합니다.
    - provider_id: 삭제할 계정의 ID.
    - provider_service: 계정 삭제 로직을 처리하는 서비스.
    성공 시 아무 내용 없는 응답(204 No Content)을, 계정이 없거나 삭제 실패 시 404 Not Found 예외를 반환합니다.
    """
    # ProviderService를 사용하여 계정을 삭제합니다.
    if not provider_service.delete_provider(provider_id):
        # 계정이 존재하지 않거나 삭제에 실패하면 404 Not Found 오류를 발생시킵니다.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found or delete failed")
    # 성공 시 별도의 응답 본문 없이 204 상태 코드가 반환됩니다.

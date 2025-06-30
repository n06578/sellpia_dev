# YTEST: /subaccount 엔드포인트 정의
from fastapi import APIRouter, Depends, HTTPException, status
from app.dtos.subaccount import SubAccountCreateDTO, SubAccountUpdateDTO, SubAccountResponseDTO, BulkCreateResponseDTO
from app.services.subaccount import SubAccountService
from app.repositories.subaccount import SubAccountRepository
from app.core.security import create_auth_dependency # 인증 의존성 생성 함수 임포트
from typing import List
import logging

logger = logging.getLogger(__name__)
# APIRouter 인스턴스를 생성하여 이 파일의 엔드포인트들을 그룹화합니다.
router = APIRouter()

# SubAccountService 인스턴스를 생성하고 반환하는 의존성 주입용 함수입니다.
# 이 함수는 SubAccountRepository의 인스턴스를 SubAccountService에 주입합니다.
def get_subaccount_service() -> SubAccountService:
    return SubAccountService(subaccount_repo=SubAccountRepository())

# 라우터의 엔드포인트에 적용될 인증 의존성 생성 - "/subaccount"
# 타입의 인증을 사용하도록 설정 - "ip_range"
subaccount_auth_dependency = Depends(create_auth_dependency("ip_range"))

# POST / 요청을 처리하여 새로운 계정을 생성하는 엔드포인트입니다.
# 응답 모델 - SubAccountResponseDTO
# 엔드포인트에 접근하기 전에 인증을 수행 - subaccount_auth_dependency
@router.post("/", response_model=SubAccountResponseDTO, status_code=status.HTTP_201_CREATED, dependencies=[subaccount_auth_dependency])
async def create_subaccount(
    subaccount_in: SubAccountCreateDTO, # 요청 본문으로 받을 데이터의 DTO (Data Transfer Object)
    subaccount_service: SubAccountService = Depends(get_subaccount_service) # SubAccountService 의존성 주입
):
    try:
        new_subaccount = subaccount_service.create_subaccount(subaccount_in)
        return new_subaccount
    except ValueError as e:
        # 서비스 계층에서 중복 등의 이유로 ValueError가 발생하면 409 Conflict를 반환
        logger.warning(f"아이디 중복 (valueError) : {str(e)}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        # 그 외 예상치 못한 오류 발생 시 500 Internal Server Error를 반환.
        logger.error(f"계정 생성 오류(Failed to create subaccount) : {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create subaccount: {e}")


@router.get("/{subaccount_id}", response_model=SubAccountResponseDTO, dependencies=[subaccount_auth_dependency])
async def read_subaccount(
    subaccount_id: str, # 경로 매개변수로 받을 계정 ID
    subaccount_service: SubAccountService = Depends(get_subaccount_service) # SubAccountService 의존성 주입
):
    try:
        subaccount = subaccount_service.get_subaccount(subaccount_id)  # 서비스 호출
        if not subaccount:
            logger.warning(f"아이디 미 존재 조회 불가 : {subaccount_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SubAccount not found")
        return subaccount
    except HTTPException as http_exc:  # 이미 HTTPException인 경우 그대로 전달
        raise http_exc
    except ValueError as ve:
        logger.error(f"서비스에서 발생 가능한 특정 비즈니스 오류 : {str(ve)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.error(f"Error in read_subaccount for ID : {subaccount_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred."
        )

# PATCH /{subaccount_id} 요청을 처리하여 특정 ID의 계정 정보를 수정하는 엔드포인트입니다.
# 응답 모델은 SubAccountResponseDTO입니다.
# subaccount_auth_dependency를 통해 인증을 수행합니다.
@router.patch("/{subaccount_id}", response_model=SubAccountResponseDTO, dependencies=[subaccount_auth_dependency])
async def update_subaccount(
    subaccount_id: str, # 경로 매개변수로 받을 수정할 계정의 ID
    subaccount_in: SubAccountUpdateDTO, # 요청 본문으로 받을 수정할 계정 정보 DTO
    subaccount_service: SubAccountService = Depends(get_subaccount_service) # SubAccountService 의존성 주입
):
    """
    특정 ID의 계정 정보를 수정합니다.
    - subaccount_id: 수정할 계정의 ID.
    - subaccount_in: 수정할 내용을 담은 DTO.
    - subaccount_service: 계정 수정 로직을 처리하는 서비스.
    성공 시 수정된 계정 정보를, 계정이 없거나 수정 실패 시 404 Not Found 예외를 반환합니다.
    """
    # SubAccountService를 사용하여 계정 정보를 수정합니다.
    updated_subaccount = subaccount_service.update_subaccount(subaccount_id, subaccount_in)
    if not updated_subaccount:
        # 계정이 존재하지 않거나 업데이트에 실패하면 404 Not Found 오류를 발생시킵니다.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SubAccount not found or update failed")
    return updated_subaccount


@router.delete("/{subaccount_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[subaccount_auth_dependency])
async def delete_subaccount(
    subaccount_id: str, # 경로 매개변수로 받을 삭제할 계정의 ID
    subaccount_service: SubAccountService = Depends(get_subaccount_service) # SubAccountService 의존성 주입
):
    """
    특정 ID의 계정을 삭제합니다.
    - subaccount_id: 삭제할 계정의 ID.
    - subaccount_service: 계정 삭제 로직을 처리하는 서비스.
    성공 시 아무 내용 없는 응답(204 No Content)을, 계정이 없거나 삭제 실패 시 404 Not Found 예외를 반환합니다.
    """
    # SubAccountService를 사용하여 계정을 삭제합니다.
    if not subaccount_service.delete_subaccount(subaccount_id):
        # 계정이 존재하지 않거나 삭제에 실패하면 404 Not Found 오류를 발생시킵니다.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SubAccount not found or delete failed")
    # 성공 시 별도의 응답 본문 없이 204 상태 코드가 반환됩니다.


# 부운영자 일괄 저장 (DB CONNECTION 부분 처리 필요)
# @router.post("/bulk", response_model=BulkCreateResponseDTO, status_code=status.HTTP_200_OK, dependencies=[subaccount_auth_dependency])
# async def create_subaccounts_bulk(
#     subaccounts_in: List[SubAccountCreateDTO], # 요청 본문으로 '리스트'를 받습니다.
#     subaccount_service: SubAccountService = Depends(get_subaccount_service)
# ):
#     """
#     여러 부계정을 일괄적으로 생성합니다.
#
#     - **요청 본문**: 생성할 계정 정보 객체의 배열(리스트)
#     - **응답**: 성공적으로 생성된 계정 목록과 실패한 계정 목록(실패 사유 포함)을 반환합니다.
#     """
#     try:
#         result = subaccount_service.create_subaccounts_bulk(subaccounts_in)
#         return result
#     except Exception as e:
#         # 서비스 로직 자체에서 예상치 못한 큰 오류가 발생한 경우
#         logger.error(f"일괄 생성 API 처리 중 심각한 오류 발생: {e}", exc_info=True)
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="An unexpected error occurred during the bulk creation process."
#         )

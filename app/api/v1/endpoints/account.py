# YTEST: /account 엔드포인트 정의
from fastapi import APIRouter, Depends, HTTPException, status
from app.dtos.account import AccountCreateDTO, AccountUpdateDTO, AccountResponseDTO
from app.services.account import AccountService
from app.repositories.account import AccountRepository
from app.core.security import create_auth_dependency # 인증 의존성 생성 함수 임포트
from typing import List

# APIRouter 인스턴스를 생성하여 이 파일의 엔드포인트들을 그룹화합니다.
router = APIRouter()

# AccountService 인스턴스를 생성하고 반환하는 의존성 주입용 함수입니다.
# 이 함수는 AccountRepository의 인스턴스를 AccountService에 주입합니다.
def get_account_service() -> AccountService:
    return AccountService(account_repo=AccountRepository())

# "/account" 라우터의 엔드포인트에 적용될 인증 의존성을 생성합니다.
# 여기서는 "ip_range" 타입의 인증을 사용하도록 설정합니다.
account_auth_dependency = Depends(create_auth_dependency("ip_range"))

# POST / 요청을 처리하여 새로운 계정을 생성하는 엔드포인트입니다.
# 응답 모델은 AccountResponseDTO이며, 성공 시 상태 코드는 201 (Created)입니다.
# account_auth_dependency를 통해 이 엔드포인트에 접근하기 전에 인증을 수행합니다.
@router.post("/", response_model=AccountResponseDTO, status_code=status.HTTP_201_CREATED, dependencies=[account_auth_dependency])
async def create_account(
    account_in: AccountCreateDTO, # 요청 본문으로 받을 데이터의 DTO (Data Transfer Object)
    account_service: AccountService = Depends(get_account_service) # AccountService 의존성 주입
):
    """
    새로운 계정을 생성합니다.
    - account_in: 생성할 계정 정보를 담은 DTO.
    - account_service: 계정 관련 비즈니스 로직을 처리하는 서비스.
    성공 시 생성된 계정 정보를, 실패 시 적절한 HTTP 예외를 반환합니다.
    """
    try:
        # AccountService를 사용하여 계정 생성 로직을 호출합니다.
        new_account = account_service.create_account(account_in)
        print(new_account)
        return new_account
    except ValueError as e:
        # 서비스 계층에서 중복 등의 이유로 ValueError가 발생하면 409 Conflict를 반환합니다.
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        # 그 외 예상치 못한 오류 발생 시 500 Internal Server Error를 반환합니다.
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create account: {e}")

# GET /{account_id} 요청을 처리하여 특정 ID의 계정 정보를 조회하는 엔드포인트입니다.
# 응답 모델은 AccountResponseDTO입니다.
# account_auth_dependency를 통해 인증을 수행합니다.
@router.get("/{account_id}", response_model=AccountResponseDTO, dependencies=[account_auth_dependency])
async def read_account(
    account_id: int, # 경로 매개변수로 받을 계정 ID
    account_service: AccountService = Depends(get_account_service) # AccountService 의존성 주입
):
    """
    특정 ID의 계정 정보를 조회합니다.
    - account_id: 조회할 계정의 ID.
    - account_service: 계정 조회 로직을 처리하는 서비스.
    계정이 존재하면 계정 정보를, 없으면 404 Not Found 예외를 반환합니다.
    """
    # AccountService를 사용하여 특정 계정 정보를 가져옵니다.
    try:
        # AccountService의 get_accounts 함수가 비동기(async)라면,
        # 반드시 'await' 키워드를 사용하여 호출해야 합니다.
        account = account_service.get_account(account_id)  # 서비스 호출
        if not account:
            # 계정이 없거나 서비스에서 None을 반환한 경우 명시적으로 404 처리
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
        return account  # 유효한 account 객체 반환
    except HTTPException as http_exc:  # 이미 HTTPException인 경우 그대로 전달
        raise http_exc
    except ValueError as ve:  # 서비스에서 발생 가능한 특정 비즈니스 오류
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        # 기타 예상치 못한 오류
        # 서비스나 리포지토리 계층에서 오류 발생 시 로그를 남기고,
        # 클라이언트에게는 일반적인 서버 오류 메시지를 반환합니다.
        print(f"Error in read_account for ID {account_id}: {e}")  # 디버깅용 로그
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred."
        )

# GET / 요청을 처리하여 여러 계정 정보를 리스트 형태로 조회하는 엔드포인트입니다.
# 응답 모델은 AccountResponseDTO의 리스트(List[AccountResponseDTO])입니다.
# account_auth_dependency를 통해 인증을 수행합니다.
@router.get("/", response_model=List[AccountResponseDTO], dependencies=[account_auth_dependency])
async def read_accounts(
    skip: int = 0, # 페이지네이션을 위한 건너뛸 항목 수 (쿼리 매개변수)
    limit: int = 100, # 페이지네이션을 위한 한 번에 가져올 최대 항목 수 (쿼리 매개변수)
    account_service: AccountService = Depends(get_account_service) # AccountService 의존성 주입
):
    """
    여러 계정 정보를 리스트 형태로 조회합니다. (페이지네이션 지원)
    - skip: 건너뛸 레코드 수.
    - limit: 반환할 최대 레코드 수.
    - account_service: 계정 목록 조회 로직을 처리하는 서비스.
    조회된 계정 목록을 반환합니다.
    """
    try:
        # AccountService의 get_accounts 함수가 비동기(async)라면,
        # 반드시 'await' 키워드를 사용하여 호출해야 합니다.
        accounts =  account_service.get_accounts(skip=skip, limit=limit)
        return accounts
    except Exception as e:
        # 서비스나 리포지토리 계층에서 오류 발생 시 로그를 남기고,
        # 클라이언트에게는 일반적인 서버 오류 메시지를 반환합니다.
        print("1----------------------------------------------------------------------")
        print(e)
        print("1----------------------------------------------------------------------")
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching accounts."
        )
    # AccountService를 사용하여 계정 목록을 가져옵니다.


# PATCH /{account_id} 요청을 처리하여 특정 ID의 계정 정보를 수정하는 엔드포인트입니다.
# 응답 모델은 AccountResponseDTO입니다.
# account_auth_dependency를 통해 인증을 수행합니다.
@router.patch("/{account_id}", response_model=AccountResponseDTO, dependencies=[account_auth_dependency])
async def update_account(
    account_id: int, # 경로 매개변수로 받을 수정할 계정의 ID
    account_in: AccountUpdateDTO, # 요청 본문으로 받을 수정할 계정 정보 DTO
    account_service: AccountService = Depends(get_account_service) # AccountService 의존성 주입
):
    """
    특정 ID의 계정 정보를 수정합니다.
    - account_id: 수정할 계정의 ID.
    - account_in: 수정할 내용을 담은 DTO.
    - account_service: 계정 수정 로직을 처리하는 서비스.
    성공 시 수정된 계정 정보를, 계정이 없거나 수정 실패 시 404 Not Found 예외를 반환합니다.
    """
    # AccountService를 사용하여 계정 정보를 수정합니다.
    updated_account = account_service.update_account(account_id, account_in)
    if not updated_account:
        # 계정이 존재하지 않거나 업데이트에 실패하면 404 Not Found 오류를 발생시킵니다.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found or update failed")
    return updated_account

# DELETE /{account_id} 요청을 처리하여 특정 ID의 계정을 삭제하는 엔드포인트입니다.
# 성공 시 상태 코드는 204 (No Content)입니다.
# account_auth_dependency를 통해 인증을 수행합니다.
@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[account_auth_dependency])
async def delete_account(
    account_id: int, # 경로 매개변수로 받을 삭제할 계정의 ID
    account_service: AccountService = Depends(get_account_service) # AccountService 의존성 주입
):
    """
    특정 ID의 계정을 삭제합니다.
    - account_id: 삭제할 계정의 ID.
    - account_service: 계정 삭제 로직을 처리하는 서비스.
    성공 시 아무 내용 없는 응답(204 No Content)을, 계정이 없거나 삭제 실패 시 404 Not Found 예외를 반환합니다.
    """
    # AccountService를 사용하여 계정을 삭제합니다.
    if not account_service.delete_account(account_id):
        # 계정이 존재하지 않거나 삭제에 실패하면 404 Not Found 오류를 발생시킵니다.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found or delete failed")
    # 성공 시 별도의 응답 본문 없이 204 상태 코드가 반환됩니다.

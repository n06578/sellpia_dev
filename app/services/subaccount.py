# YTEST: 계정 관련 비즈니스 로직 (리포지토리와 컨트롤러/엔드포인트 연결)
from app.dtos.subaccount import SubAccountCreateDTO, SubAccountUpdateDTO, SubAccountResponseDTO, BulkCreateResponseDTO, BulkCreateErrorDetail
from app.repositories.subaccount_models import SubAccount
from app.repositories.subaccount import SubAccountRepository
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)
class SubAccountService:
    def __init__(self, subaccount_repo: SubAccountRepository):
        self.subaccount_repo = subaccount_repo

    def create_subaccount(self, subaccount_data: SubAccountCreateDTO) -> SubAccountResponseDTO:
        # 중복 검사
        existing_subaccount = self.subaccount_repo.get(subaccount_data.worker_id)
        if existing_subaccount:
            raise ValueError(f"아이디 존재 SubAccount with username '{subaccount_data.worker_id}' already exists.")
        # 계정 생성
        created_subaccount = self.subaccount_repo.create(subaccount_data)

        return SubAccountResponseDTO(
            worker_id=created_subaccount.worker_id,
            worker_name=str(created_subaccount.worker_name),
            worker_cellphone=created_subaccount.worker_cellphone
        )

    def get_subaccount(self, subaccount_id: str) -> Optional[SubAccountResponseDTO]:
        # 단일 계정 호출
        subaccount = self.subaccount_repo.get(subaccount_id)
        if subaccount:
            return SubAccountResponseDTO.model_validate(subaccount)
        return None

    def update_subaccount(self, subaccount_id: str, subaccount_data: SubAccountUpdateDTO) -> Optional[SubAccountResponseDTO]:
        updated_subaccount = self.subaccount_repo.update(subaccount_id, subaccount_data)

        if updated_subaccount:
            return SubAccountResponseDTO.model_validate(updated_subaccount)
        return None

    def delete_subaccount(self, subaccount_id: str) -> bool:
        return self.subaccount_repo.delete(subaccount_id)   #YCHECK주석처리

    # def create_subaccounts_bulk(self, subaccounts_in: List[SubAccountCreateDTO]) -> BulkCreateResponseDTO:
    #     """
    #     여러 부계정을 일괄적으로 생성합니다.
    #     개별 생성의 성공/실패를 나누어 결과를 반환합니다.
    #     """
    #     successful_creations = []
    #     failed_creations = []
    #
    #     for account_dto in subaccounts_in:
    #         try:
    #             # 기존의 단일 생성 메서드를 재사용합니다.
    #             new_account = self.create_subaccount(account_dto)
    #             successful_creations.append(new_account)
    #         except ValueError as e:
    #             # 중복 아이디 등 예측된 오류(ValueError) 발생 시 실패 목록에 추가
    #             logger.warning(f"일괄 생성 중 아이디 중복: {account_dto.worker_id}, 사유: {e}")
    #             failed_creations.append(
    #                 BulkCreateErrorDetail(attempted_id=account_dto.worker_id, reason=str(e))
    #             )
    #         except Exception as e:
    #             # 그 외 예상치 못한 오류 발생 시 실패 목록에 추가
    #             logger.error(f"일괄 생성 중 예외 발생: {account_dto.worker_id}, 오류: {e}", exc_info=True)
    #             failed_creations.append(
    #                 BulkCreateErrorDetail(attempted_id=account_dto.worker_id, reason="An unexpected internal error occurred.")
    #             )
    #
    #     return BulkCreateResponseDTO(
    #         successful_creates=successful_creations,
    #         failed_creates=failed_creations
    #     )
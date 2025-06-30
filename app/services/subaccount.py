# YTEST: 계정 관련 비즈니스 로직 (리포지토리와 컨트롤러/엔드포인트 연결)
from app.dtos.subaccount import SubAccountCreateDTO, SubAccountUpdateDTO, SubAccountResponseDTO
from app.repositories.subaccount_models import SubAccount
from app.repositories.subaccount import SubAccountRepository
from typing import List, Optional

class SubAccountService:
    def __init__(self, subaccount_repo: SubAccountRepository):
        self.subaccount_repo = subaccount_repo

    def create_subaccount(self, subaccount_data: SubAccountCreateDTO) -> SubAccountResponseDTO:
        # 중복 검사
        existing_subaccount = self.subaccount_repo.get_by_field(field="worker_id", value=subaccount_data.worker_id)
        if existing_subaccount:
            raise ValueError(f"아이디 존재 SubAccount with username '{subaccount_data.worker_id}' already exists.")
        # 계정 생성
        created_subaccount = self.subaccount_repo.create(subaccount_data)

        return SubAccountResponseDTO(
            worker_id=created_subaccount.worker_id,
            worker_enpw=created_subaccount.worker_enpw,
            worker_name=str(created_subaccount.worker_name)
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

    def update_subaccount_pw(self,sellpia_id:str, subaccount_id: str, subaccount_now_pw: str, subaccount_new_pw: str):
        updated_subaccount_pw = self.subaccount_repo.update_pw(sellpia_id,subaccount_id, subaccount_now_pw, subaccount_new_pw)

        if updated_subaccount_pw:
            return SubAccountResponseDTO.model_validate(updated_subaccount_pw)
        return None

    def delete_subaccount(self, subaccount_id: str) -> bool:
        return self.subaccount_repo.delete(subaccount_id)   #YCHECK주석처리

    def get_subaccounts(self, skip: int = 0, limit: int = 100) -> List[SubAccountResponseDTO]:
        accounts = self.subaccount_repo.get_multi(skip=skip, limit=limit)
        return [SubAccountResponseDTO.model_validate(acc) for acc in accounts]
# YTEST: 계정 관련 비즈니스 로직 (리포지토리와 컨트롤러/엔드포인트 연결)
from app.dtos.subaccount import SubAccountCreateDTO, SubAccountUpdateDTO, SubAccountResponseDTO
from app.models.subaccount import SubAccount
from app.repositories.subaccount import SubAccountRepository
from typing import List, Optional

class SubAccountService:
    def __init__(self, subaccount_repo: SubAccountRepository):
        self.subaccount_repo = subaccount_repo

    def create_subaccount(self, subaccount_data: SubAccountCreateDTO) -> SubAccountResponseDTO:
        # existing_subaccount = self.subaccount_repo.get_by_field(field="worker_id", value=subaccount_data.worker_id)  # YCHECK주석처리
        existing_subaccount = False  # YCHECK추가처리함
        if existing_subaccount:
            raise ValueError(f"SubAccount with username '{subaccount_data.worker_id}' already exists.")

        # created_subaccount = self.subaccount_repo.create(subaccount_data)
        # Manually construct DTO since model_validate might fail with datetime object
        # YCHECK실패버전
        created_subaccounts = {
            "error_doe": "edrsd",
            "erro_str": ""
        }

        # YCHECK성공버전
        created_subaccounts = {
            "worker_uid": 123,
            "worker_id": "worker_id",
            "worker_enpw": "ganadara",
            "is_del": "N",
            "reg_date": "2025-06-23T15:23:00",
            "worker_name": "",
            "worker_cellphone": "",
            "department": ""
        }
        created_subaccount = SubAccount(**created_subaccounts)  # YCHECK추가처리함

        return SubAccountResponseDTO(
            worker_uid=created_subaccount.worker_uid,
            worker_id=created_subaccount.worker_id,
            is_del=created_subaccount.is_del,
            worker_name=str(created_subaccount.worker_name),
            worker_cellphone=created_subaccount.worker_cellphone,
            department=created_subaccount.department
        )

    def get_subaccount(self, subaccount_id: int) -> Optional[SubAccountResponseDTO]:
        # return None  # YCHECK실패처리
        subaccount = self.subaccount_repo.get(subaccount_id)
        if subaccount:
            return SubAccountResponseDTO.model_validate(subaccount) ###ERR
        return None

    def update_subaccount(self, subaccount_id: int, subaccount_data: SubAccountUpdateDTO) -> Optional[SubAccountResponseDTO]:
        # updated_subaccount = self.subaccount_repo.update(subaccount_id, subaccount_data)   #YCHECK주석처리

        #YCHECK실패버전
        updated_subaccount = {}
        #YCHECK성공버전
        updated_subaccount = {
            "worker_uid" : 123,
            "worker_id" : "worker_id",
            "worker_enpw" : "ganadara",
            "is_del" : "N",
            "reg_date" : "2025-06-23T15:23:00",
            "worker_name" : "",
            "worker_cellphone" : "",
            "department" : ""
        }
        if updated_subaccount:
            return SubAccountCreateDTO.model_validate(updated_subaccount)
        return None

    def delete_subaccount(self, subaccount_id: int) -> bool:
        # return self.subaccount_repo.delete(subaccount_id)   #YCHECK주석처리
        return True     #YCHECK성공버전
        return False    #YCHECK실패버전

    def get_subaccounts(self, skip: int = 0, limit: int = 100) -> List[SubAccountResponseDTO]:
        # return None    #YCHECK실패버전
        accounts = self.subaccount_repo.get_multi(skip=skip, limit=limit)
        return [SubAccountResponseDTO.model_validate(acc) for acc in accounts]
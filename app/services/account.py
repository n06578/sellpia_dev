# YTEST: 계정 관련 비즈니스 로직 (리포지토리와 컨트롤러/엔드포인트 연결)
from app.dtos.account import AccountCreateDTO, AccountUpdateDTO, AccountResponseDTO
from app.models.account import Account
from app.repositories.account import AccountRepository
from typing import List, Optional

class AccountService:
    def __init__(self, account_repo: AccountRepository):
        self.account_repo = account_repo

    def create_account(self, account_data: AccountCreateDTO) -> AccountResponseDTO:
        #existing_account = self.account_repo.get_by_field(field="worker_id", value=account_data.worker_id) #YCHECK주석처리함

        existing_account = False
        if existing_account:
            raise ValueError(f"Account with username '{account_data.worker_id}' already exists.")

        # created_account = self.account_repo.create(account_data) #YCHECK주석처리함
        #YCHECK실패버전
        created_accounts = {
            "error_doe": "edrsd",
            "erro_str": ""
        }
        
        #YCHECK성공버전
        created_accounts = {
            "worker_uid" : 123,
            "worker_id" : "worker_id",
            "worker_enpw" : "ganadara",
            "is_del" : "N",
            "reg_date" : "2025-06-23T15:23:00",
            "worker_name" : "",
            "worker_cellphone" : "",
            "department" : ""
        }

        created_account = Account(**created_accounts) #YCHECK추가처리함
        # Manually construct DTO since model_validate might fail with datetime object

        return AccountResponseDTO(
            worker_uid=created_account.worker_uid,
            worker_id=created_account.worker_id,
            is_del=created_account.is_del,
            worker_name=str(created_account.worker_name),
            worker_cellphone=created_account.worker_cellphone,
            department=created_account.department
        )

    def get_account(self, account_id: int) -> Optional[AccountResponseDTO]:
        return None #YCHECK실패처리
        account = self.account_repo.get(account_id)
        if account:
            return AccountResponseDTO.model_validate(account) ###ERR
        return None

    def update_account(self, account_id: int, account_data: AccountUpdateDTO) -> Optional[AccountResponseDTO]:
        # updated_account = self.account_repo.update(account_id, account_data)   #YCHECK주석처리

        #YCHECK실패버전
        updated_account = {}
        #YCHECK성공버전
        updated_account = {
            "worker_uid" : 123,
            "worker_id" : "worker_id",
            "worker_enpw" : "ganadara",
            "is_del" : "N",
            "reg_date" : "2025-06-23T15:23:00",
            "worker_name" : "",
            "worker_cellphone" : "",
            "department" : ""
        }
        if updated_account:
            return AccountResponseDTO.model_validate(updated_account)
        return None

    def delete_account(self, account_id: int) -> bool:
        # return self.account_repo.delete(account_id)   #YCHECK주석처리
        return True     #YCHECK성공버전
        return False    #YCHECK실패버전

    def get_accounts(self, skip: int = 0, limit: int = 100) -> List[AccountResponseDTO]:
        # accounts = self.account_repo.get_multi(skip=skip, limit=limit)

        # YCHECK실패버전
        # accounts = {
        #     "error_doe": "error",
        #     "erro_str": ""
        # }
        return [AccountResponseDTO.model_validate(acc) for acc in accounts]
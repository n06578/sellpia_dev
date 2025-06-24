# YTEST: 계정 관련 비즈니스 로직 (리포지토리와 컨트롤러/엔드포인트 연결)
from app.dtos.provider import ProviderCreateDTO, ProviderUpdateDTO, ProviderResponseDTO
from app.models.provider import Provider
from app.repositories.provider import ProviderRepository
from typing import List, Optional


class ProviderService:
    def __init__(self, provider_repo: ProviderRepository):
        self.provider_repo = provider_repo

    def create_provider(self, provider_data: ProviderCreateDTO) -> ProviderResponseDTO:
        # existing_provider = self.provider_repo.get_by_field(field="worker_id", value=provider_data.worker_id) #YCHECK주석처리함

        existing_provider = False
        if existing_provider:
            raise ValueError(f"Provider with username '{provider_data.worker_id}' already exists.")

        # created_provider = self.provider_repo.create(provider_data) #YCHECK주석처리함
        # YCHECK실패버전
        created_providers = {
            "error_doe": "edrsd",
            "erro_str": ""
        }

        # YCHECK성공버전
        created_providers = {
            "provider_uid": 123,
            "provider_id": "test_worker_01",
            "provider_pw": "testpassword123",
            "is_del": "N",
            "provider_name": "테스트 작업자",
            "provider_phone": "010-1234-5678",
            "provider_etc": "개발팀"
        }

        created_provider = Provider(**created_providers)  # YCHECK추가처리함
        # Manually construct DTO since model_validate might fail with datetime object

        print(created_provider)
        return ProviderResponseDTO(
            provider_uid=created_provider.provider_uid,
            provider_id=created_provider.provider_id,
            provider_pw=created_provider.provider_pw,
            is_del=created_provider.is_del,
            provider_name=created_provider.provider_name,
            provider_phone=created_provider.provider_phone
        )

    def get_provider(self, provider_id: int) -> Optional[ProviderResponseDTO]:
        provider = self.provider_repo.get(provider_id)
        if provider:
            return ProviderResponseDTO.model_validate(provider)  ###ERR
        return None

    def delete_provider(self, provider_id: int) -> bool:
        # return self.provider_repo.delete(provider_id)   #YCHECK주석처리
        return True  # YCHECK성공버전
        return False  # YCHECK실패버전

    def get_providers(self, skip: int = 0, limit: int = 100) -> List[ProviderResponseDTO]:
        providers = self.provider_repo.get_multi(skip=skip, limit=limit)
        return [ProviderResponseDTO.model_validate(acc) for acc in providers]
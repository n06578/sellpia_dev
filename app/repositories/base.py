# YTEST: 리포지토리 인터페이스 정의 (추상화)
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class BaseRepository(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    # YTEST: 모든 리포지토리가 구현해야 할 기본 CRUD 인터페이스
    @abstractmethod
    def create(self, obj_in: CreateSchemaType) -> ModelType:
        pass

    @abstractmethod
    def get(self, id: int) -> Optional[ModelType]:
        pass

    @abstractmethod
    def update(self, id: int, obj_in: UpdateSchemaType) -> Optional[ModelType]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

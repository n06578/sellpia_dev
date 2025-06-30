# YTEST : 계정 관련 데이터 전송 객체 (DTO) 정의
from pydantic import BaseModel, Field, EmailStr
from typing import Optional,List
from datetime import datetime

class SubAccountCreateDTO(BaseModel) :
    # worker_uid : Optional[int] = Field(..., description="작업자 로그인 ID")
    worker_id : str = Field(..., description="작업자 로그인 ID")
    worker_name : Optional[str] = Field(None, max_length=20, description="이름")
    worker_cellphone : Optional[str] = Field(None, max_length=20)


class SubAccountUpdateDTO(BaseModel) :
    # YTEST : 계정 수정 요청 시 사용할 DTO
    worker_name : Optional[str] = Field(None, max_length=20, description="이름")
    worker_cellphone : Optional[str] = Field(None, max_length=20)

class SubAccountResponseDTO(BaseModel) :
    """
    계정 정보 응답을 위한 DTO (Data Transfer Object)
    """
    worker_id : str = Field(..., description="작업자 로그인 ID")
    worker_name : Optional[str] = Field(None, max_length=20, description="이름")
    worker_cellphone : Optional[str] = Field(None, max_length=20)
    class Config :
        # 이 설정은 ORM 객체(예 : SQLAlchemy 모델)의 속성을 DTO 필드에 자동으로 매핑해줍니다.
        # Pydantic v2 이상에서는 from_attributes=True, 이전 버전에서는 orm_mode=True를 사용합니다.
        from_attributes = True

class BulkCreateErrorDetail(BaseModel):
    """일괄 생성 시 실패한 항목의 정보"""
    attempted_id: str = Field(..., description="생성 시도된 계정 ID")
    reason: str = Field(..., description="실패 사유")

class BulkCreateResponseDTO(BaseModel):
    """일괄 생성 결과 응답"""
    successful_creates: List[SubAccountResponseDTO] = Field(..., description="성공적으로 생성된 계정 목록")
    failed_creates: List[BulkCreateErrorDetail] = Field(..., description="생성에 실패한 계정 목록")
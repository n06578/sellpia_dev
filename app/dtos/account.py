# YTEST: 계정 관련 데이터 전송 객체 (DTO) 정의
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class AccountCreateDTO(BaseModel):
    # YTEST: 계정 생성 요청 시 사용할 DTO
    # 필수 정보
    worker_uid: int = Field(..., description="작업자 고유 ID (PK)")
    worker_id: str = Field(..., description="작업자 로그인 ID")
    worker_enpw: Optional[str] = Field(None, min_length=8, description="New password for the account")
    is_del: str = Field(...,  description="삭제 여부 ('N': 사용중, 'Y': 삭제됨)")
    # 선택 정보 (NULL 허용 필드)
    reg_date: Optional[datetime] = Field(None, description="계정 등록일")
    worker_name: Optional[str] = Field(None, max_length=20, description="작업자 이름")
    worker_cellphone: Optional[str] = Field(None, max_length=20, description="핸드폰 번호")
    department: Optional[str] = Field(None, max_length=200, description="부서")
    display_type: Optional[str] = Field(None, max_length=20, description="사용자 그룹")
    # act_account: Optional[str] = Field(None, description="계정 권한")
    login_ip: Optional[str] = Field(None, max_length=20, description="마지막 로그인 IP")
    login_time: Optional[datetime] = Field(None, description="마지막 로그인 시간")

class AccountUpdateDTO(BaseModel):
    # YTEST: 계정 수정 요청 시 사용할 DTO
    worker_id: Optional[str] = Field(None, min_length=3, max_length=50, description="New username for the account")
    worker_enpw: Optional[str] = Field(None, min_length=8, description="New password for the account")
    worker_name: Optional[str] = Field(None, description="New email address for the account")

class AccountResponseDTO(BaseModel):
    """
    계정 정보 응답을 위한 DTO (Data Transfer Object)
    """
    # 필수 정보
    worker_uid: int = Field(..., description="작업자 고유 ID (PK)")
    worker_id: str = Field(..., description="작업자 로그인 ID")
    worker_enpw: Optional[str] = Field(None, min_length=8, description="New password for the account")
    is_del: str = Field(...,  description="삭제 여부 ('N': 사용중, 'Y': 삭제됨)")
    reg_date: Optional[datetime] = Field(None, description="계정 등록일")

    # 선택 정보 (NULL 허용 필드)
    worker_name: Optional[str] = Field(None, max_length=20, description="작업자 이름")
    worker_cellphone: Optional[str] = Field(None, max_length=20, description="핸드폰 번호")
    department: Optional[str] = Field(None, max_length=200, description="부서")
    display_type: Optional[str] = Field(None, max_length=20, description="사용자 그룹")
    # act_account: Optional[str] = Field(None, description="계정 권한")
    login_ip: Optional[str] = Field(None, max_length=20, description="마지막 로그인 IP")
    login_time: Optional[datetime] = Field(None, description="마지막 로그인 시간")

    class Config:
        # 이 설정은 ORM 객체(예: SQLAlchemy 모델)의 속성을 DTO 필드에 자동으로 매핑해줍니다.
        # Pydantic v2 이상에서는 from_attributes=True, 이전 버전에서는 orm_mode=True를 사용합니다.
        from_attributes = True

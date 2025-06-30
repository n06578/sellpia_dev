# YTEST : 계정 관련 데이터 전송 객체 (DTO) 정의
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class SubAccountCreateDTO(BaseModel) :
    # worker_uid : Optional[int] = Field(..., description="작업자 로그인 ID")
    worker_uid: Optional[int] = Field(None)
    worker_id : str = Field(..., description="작업자 로그인 ID")
    worker_enpw : Optional[str] = Field(None, min_length=8, description="비밀번호")
    worker_name : Optional[str] = Field(None, max_length=20, description="이름")
    is_del : Optional[str] = Field(None, description="삭제 여부")
    department : Optional[str] = Field(None, max_length=200)
    worker_cellphone : Optional[str] = Field(None, max_length=20)
    display_type : Optional[str] = Field(None, max_length=20)
    act_account : Optional[str] = Field(None)
    reg_date : Optional[datetime] = Field(None)
    pw_chg_date : Optional[datetime] = Field(None)
    login_ip : Optional[str]  = Field(None)
    login_time : Optional[datetime]  = Field(None)
    quick_menu : Optional[str]  = Field(None)
    access_pos_shop_uid : Optional[str]  = Field(None)
    worker_otp : Optional[str]  = Field(None)
    kiosk_access_token : Optional[str]  = Field(None)


class SubAccountUpdateDTO(BaseModel) :
    # YTEST : 계정 수정 요청 시 사용할 DTO
    # worker_id: str = Field(..., description="작업자 로그인 ID")
    worker_name : Optional[str] = Field(None, max_length=20, description="이름")
    department : Optional[str] = Field(None, max_length=200)
    worker_cellphone : Optional[str] = Field(None, max_length=20)
    display_type : Optional[str] = Field(None, max_length=20)

class SubAccountResponseDTO(BaseModel) :
    """
    계정 정보 응답을 위한 DTO (Data Transfer Object)
    """
    worker_uid: Optional[int] = Field(None)
    worker_id : str = Field(..., description="작업자 로그인 ID")
    worker_enpw : Optional[str] = Field(None, min_length=8, description="비밀번호")
    worker_name : Optional[str] = Field(None, max_length=20, description="이름")
    is_del : Optional[str] = Field(None, description="삭제 여부")
    department : Optional[str] = Field(None, max_length=200)
    worker_cellphone : Optional[str] = Field(None, max_length=20)
    display_type : Optional[str] = Field(None, max_length=20)
    act_account : Optional[str] = Field(None)
    reg_date : Optional[datetime] = Field(None)
    pw_chg_date : Optional[datetime] = Field(None)
    class Config :
        # 이 설정은 ORM 객체(예 : SQLAlchemy 모델)의 속성을 DTO 필드에 자동으로 매핑해줍니다.
        # Pydantic v2 이상에서는 from_attributes=True, 이전 버전에서는 orm_mode=True를 사용합니다.
        from_attributes = True


class SubAccountPasswordUpdateDTO(BaseModel):
    current_password: Optional[str] = Field(None, description="비밀번호")
    new_password: Optional[str] = Field(None, description="비밀번호")
# YTEST : 계정 관련 데이터 전송 객체 (DTO) 정의
from pydantic import BaseModel, Field, EmailStr
from typing import Optional,List
from datetime import datetime

class SubAccountCreateDTO(BaseModel) :
    worker_id : str = Field(..., description="작업자 로그인 ID")
    worker_name : Optional[str] = Field(None, max_length=20, description="이름")
    worker_cellphone : Optional[str] = Field(None, max_length=20)

class SubAccountUpdateDTO(BaseModel) :
    worker_name : Optional[str] = Field(None, max_length=20, description="이름")
    worker_cellphone : Optional[str] = Field(None, max_length=20)

class SubAccountResponseDTO(BaseModel) :
    worker_id : str = Field(..., description="작업자 로그인 ID")
    worker_name : Optional[str] = Field(None, max_length=20, description="이름")
    worker_cellphone : Optional[str] = Field(None, max_length=20)
    class Config :
        from_attributes = True

#
# class BulkCreateErrorDetail(BaseModel):
#     """일괄 생성 시 실패한 항목의 정보"""
#     attempted_id: str = Field(..., description="생성 시도된 계정 ID")
#     reason: str = Field(..., description="실패 사유")
#
# class BulkCreateResponseDTO(BaseModel):
#     """일괄 생성 결과 응답"""
#     successful_creates: List[SubAccountResponseDTO] = Field(..., description="성공적으로 생성된 계정 목록")
#     failed_creates: List[BulkCreateErrorDetail] = Field(..., description="생성에 실패한 계정 목록")
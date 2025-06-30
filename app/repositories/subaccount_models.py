from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SubAccount(BaseModel):
    # DB의 'worker' 테이블 스키마와 필드명, 타입을 일치시킵니다.
    worker_uid: Optional[int] =None
    worker_id: str
    worker_enpw: Optional[str] =None
    is_del: Optional[str] =None
    reg_date: Optional[datetime]  =None # str -> datetime 으로 변경

    # NULL을 허용하는 필드는 Optional로 지정합니다.
    pw_chg_date: Optional[datetime] =None
    display_type: Optional[str] =None
    worker_name: Optional[str] =None
    worker_cellphone: Optional[str] =None
    department: Optional[str] =None
    act_account: Optional[str] =None
    quick_menu: Optional[str] =None
    access_pos_shop_uid: Optional[int] =None
    worker_otp: Optional[str] =None
    kiosk_access_token: Optional[str] =None

    class Config:
        # Pydantic V2에서는 from_attributes=True를 사용합니다.
        # 이 설정은 DB에서 읽어온 객체를 Pydantic 모델로 변환할 때 필요합니다.
        from_attributes = True
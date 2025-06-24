from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Provider(BaseModel):
    # ✅ 필수 Primary Key
    provider_uid: int

    # ✅ 나머지는 모두 Optional
    provider_name: Optional[str] = None
    provider_id: Optional[str] = None
    provider_pw: Optional[str] = None
    provider_id_key: Optional[str] = None
    provider_id_key2: Optional[str] = None
    provider_id_key3: Optional[str] = None
    provider_id_key_etc: Optional[str] = None
    auto_login_id: Optional[str] = None
    auto_login_pw: Optional[str] = None
    provider_vender: Optional[str] = None
    provider_sub_vender: Optional[str] = None
    vender_url: Optional[str] = None
    provider_phone: Optional[str] = None
    provider_mobile: Optional[str] = None
    provider_fax: Optional[str] = None
    provider_grade: Optional[str] = None
    provider_post: Optional[str] = None
    provider_address: Optional[str] = None
    provider_regno: Optional[str] = None
    provider_kind: Optional[str] = None
    provider_stock_rate: Optional[int] = None
    provider_business: Optional[str] = None
    provider_type: Optional[str] = None
    provider_ceo: Optional[str] = None
    provider_arcade: Optional[str] = None
    provider_pay: Optional[str] = None
    provider_pay_info: Optional[str] = None
    provider_sdate: Optional[datetime] = None
    provider_edate: Optional[datetime] = None
    responsible_part: Optional[str] = None
    responsible_person: Optional[str] = None
    responsible_phone: Optional[str] = None
    responsible_email: Optional[str] = None
    provider_vat: Optional[str] = None
    is_del: Optional[str] = None
    provider_bankname: Optional[str] = None
    provider_bankaccount: Optional[str] = None
    provider_banker: Optional[str] = None
    provider_memo: Optional[str] = None
    provider_memo2: Optional[str] = None
    off_allow: Optional[str] = None
    off_allow_date: Optional[datetime] = None
    use_stock_apply: Optional[str] = None
    off_shop_type: Optional[int] = None
    off_shop_type2: Optional[str] = None
    off_shop_area: Optional[int] = None
    om_connect_type: Optional[str] = None
    supply_price_rate: Optional[int] = None
    supply_price_rate_log: Optional[str] = None
    bring_prov_ord: Optional[str] = None
    provider_group_code: Optional[int] = None
    sellpocket_van: Optional[str] = None
    sellpocket_terminal_id: Optional[str] = None
    stamppang_id: Optional[str] = None
    stamppang_pw: Optional[str] = None
    provider_etc: Optional[str] = None
    sms_allow: Optional[str] = None
    sms_allowsellpia_test: Optional[str] = None
    sms_allow_num: Optional[str] = None
    sms_allow_file: Optional[str] = None
    provider_group_code2: Optional[str] = None
    service_time: Optional[str] = None
    reg_date: Optional[datetime] = None
    provider_grade_index: Optional[int] = None
    provider_delivery_use: Optional[str] = None
    provider_delivery_account: Optional[str] = None
    use_auto_api: Optional[str] = None

    class Config:
        from_attributes = True
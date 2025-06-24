# YTEST: API 버전별 라우터 정의 및 그룹화
from fastapi import APIRouter
from app.api.v1.endpoints import account, provider, subaccount

api_router = APIRouter()
# api_router.include_router(account.router, prefix="/debug", tags=["Dibug"])
api_router.include_router(account.router, prefix="/account", tags=["Account"])
api_router.include_router(provider.router, prefix="/provider", tags=["Provider"])
api_router.include_router(subaccount.router, prefix="/subaccount", tags=["Subaccount"])

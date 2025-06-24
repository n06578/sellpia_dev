# YTEST: FastAPI 애플리케이션의 메인 진입점
from fastapi import FastAPI
from app.api.v1.routers import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description=settings.PROJECT_DESCRIPTION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    # YTEST: 기본 루트 엔드포인트
    return {"message": "Welcome to FastAPI Clean Architecture API!"}

# YTEST: 추가 미들웨어, 이벤트 핸들러 등 필요 시 여기에 추가

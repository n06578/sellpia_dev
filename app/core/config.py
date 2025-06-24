# YTEST: 애플리케이션의 환경 설정 관리
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Clean Architecture API"
    API_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "Clean Architecture for FastAPI with MySQL"
    DEBUG: bool = True

    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "Nyoun003310!"
    MYSQL_ROOT_PASSWORD: str = "Nyoun003310" # YTEST: 계정 생성 시 사용할 MySQL root 계정 비밀번호
    MYSQL_DB: str = "sellpia_test" # YTEST: 초기 DB 연결 시 사용할 기본 DB

    ALLOWED_IP_RANGES: list[str] = ["127.0.0.1/32","testclient"] # YTEST: 허용할 IP 대역 목록

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

# YTEST: MySQL 데이터베이스 연결 관리
import mysql.connector
from mysql.connector import Error
import logging

# 이 모듈을 위한 로거 설정
# 실제 애플리케이션에서는 로깅 설정을 중앙에서 관리하는 것이 좋습니다.
# 예: logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MySQLConnection:
    def __init__(self, host=None, port=None, user=None, password=None, database=None):
        # YTEST: DB 연결 정보.
        # !! 중요 경고 !!
        # 프로덕션 환경에서는 아래와 같이 민감한 정보를 코드에 직접 하드코딩하는 것을 강력히 권장하지 않습니다.
        # 대신, 환경 변수나 보안 설정 파일을 통해 관리하고,
        # 예를 들어 app.core.config.settings 와 같은 설정 객체를 통해 로드하는 것이 안전합니다.
        # 이 코드는 사용자의 요청에 따라 특정 DB에 기본적으로 연결되도록 수정된 예시입니다.

        # 제공된 인자 사용, 없으면 사용자의 DB 정보로 기본값 설정
        self.host = host if host is not None else "localhost"
        self.port = port if port is not None else 3306
        self.user = user if user is not None else "root"
        self.password = password if password is not None else "Nyoun003310!"  # 사용자 제공 비밀번호
        self.database = database if database is not None else "sellpia_test"  # 사용자 제공 DB 이름

        self.connection = None
        logger.debug(
            f"MySQLConnection initialized for host={self.host}, port={self.port}, user={self.user}, db={self.database}")

    def __enter__(self):
        # YTEST: 컨텍스트 매니저 진입 시 DB 연결
        try:
            logger.debug(f"Attempting to connect to MySQL: db={self.database}, host={self.host}, user={self.user}")
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                connection_timeout=10  # 초 단위 연결 타임아웃 추가
            )
            # connect()가 성공하면 연결된 것입니다. is_connected()는 선택적 확인입니다.
            logger.info(f"Successfully connected to MySQL database: {self.database} on {self.host}")
            return self.connection
        except Error as e:
            # 연결 실패 시 상세 정보와 함께 에러 로깅
            logger.error(
                f"Error connecting to MySQL database (Host: {self.host}, Port: {self.port}, DB: {self.database}, User: {self.user}): {e}",
                exc_info=True)
            raise  # YTEST: 연결 실패 시 예외를 다시 발생시켜 호출자가 처리하도록 함

    def __exit__(self, exc_type, exc_val, exc_tb):
        # YTEST: 컨텍스트 매니저 종료 시 DB 연결 닫기
        if self.connection and self.connection.is_connected():
            try:
                self.connection.close()
                logger.info(f"MySQL connection to {self.database} on {self.host} closed.")
            except Error as e:
                logger.error(f"Error closing MySQL connection to {self.database} on {self.host}: {e}", exc_info=True)

        # 'with' 블록 내에서 예외가 발생했다면 exc_type, exc_val, exc_tb에 정보가 전달됩니다.
        # 여기서 True를 반환하면 예외가 숨겨지고, False (또는 None을 암묵적으로 반환)하면 예외가 다시 발생합니다.
        # 특별히 예외를 처리하지 않는 한, 다시 발생시키는 것이 일반적입니다.
        if exc_type:  # 'with' 블록 내에서 예외가 발생한 경우
            logger.debug(f"Exception occurred within MySQLConnection context: Type={exc_type}, Value={exc_val}")
        return False  # 'with' 블록에서 발생한 예외를 다시 발생시킴 (기본 동작)


def get_db_connection(db_name: str = None):
    """
    MySQLConnection 컨텍스트 매니저를 사용하여 DB 연결을 생성하고 제공하는 제너레이터 함수.
    FastAPI 의존성 주입에 사용될 수 있습니다.

    `db_name`이 제공되면 해당 데이터베이스에 연결합니다.
    그렇지 않으면 `MySQLConnection` 클래스에 설정된 기본 데이터베이스('sellpia_test')에 연결합니다.
    다른 연결 파라미터(host, port, user, password)는 `MySQLConnection`의 기본값을 따릅니다.
    """
    # YTEST: FastAPI 의존성 주입에 사용할 함수
    # MySQLConnection 인스턴스 생성 시 db_name을 전달합니다.
    # db_name이 None이면, MySQLConnection의 __init__에서 self.database가 'sellpia_test'로 설정됩니다.
    conn_manager = MySQLConnection(database=db_name)
    try:
        # MySQLConnection의 __enter__가 호출되어 연결을 설정하고,
        # __exit__이 호출되어 연결을 해제하는 컨텍스트 관리
        with conn_manager as conn:
            # __enter__가 성공적으로 connection 객체를 반환하면,
            # 해당 연결 객체를 FastAPI 경로 함수 등으로 전달합니다.
            yield conn
    except Error as e:
        # MySQLConnection.__enter__에서 연결 오류 발생 시 이 블록에서 처리될 수 있습니다.
        logger.error(
            f"Failed to provide DB connection via get_db_connection (target DB: '{db_name or conn_manager.database}'): {e}",
            exc_info=True)
        # FastAPI가 오류를 인지하고 적절히 응답하도록 예외를 다시 발생시킵니다.
        # 필요에 따라 특정 HTTPException으로 변환할 수도 있습니다. (예: FastAPI 사용 시)
        # from fastapi import HTTPException
        # raise HTTPException(status_code=503, detail=f"Database service unavailable: {e}")
        raise
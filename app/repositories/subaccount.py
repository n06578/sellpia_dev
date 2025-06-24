import mysql.connector
from mysql.connector import Error
from app.models.subaccount import SubAccount
from app.dtos.subaccount import SubAccountCreateDTO, SubAccountUpdateDTO
from app.repositories.base import BaseRepository
from app.core.config import settings
from app.database.connection import MySQLConnection
from app.database.triggers import TriggerQueries
from app.database.events import EventQueries
from typing import List, Optional
import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
class SubAccountRepository(BaseRepository[SubAccount, SubAccountCreateDTO, SubAccountUpdateDTO]):
    def __init__(self):
        pass

    def _is_valid_account_name(self, account_name: str) -> bool:
        # YTEST: 계정 이름 유효성 검사 (MySQL DB, User 이름 규칙 및 예약어 방지)
        if not re.match(r"^[a-zA-Z0-9_]{3,30}$", account_name):
            return False
        # YTEST: MySQL 예약어나 시스템 DB 이름과 충돌 방지 (추가 필요시)
        reserved_words = ["mysql", "information_schema", "performance_schema", "sys", "admin", "root", "user", "test"]
        if account_name.lower() in reserved_words:
            return False
        return True

    def _execute_admin_query(self, query: str, params: tuple = None, multi: bool = False):
        # YTEST: MySQL root 계정으로 관리 쿼리 실행
        try:
            with MySQLConnection(user=settings.MYSQL_USER, password=settings.MYSQL_ROOT_PASSWORD) as conn:
                if conn:
                    cursor = conn.cursor()
                    if multi:
                        # YTEST: 여러 SQL 문을 포함하는 쿼리 실행 (예: 스키마 SQL 파일)
                        for result in cursor.execute(query, params, multi=True):
                            pass  # Fetch all results to ensure execution completion
                    else:
                        cursor.execute(query, params)
                    conn.commit()
                    return cursor
        except Error as e:
            print(f"Error executing admin query: {e}")
            raise  # YTEST: 오류 발생 시 예외 다시 발생

    def _execute_account_db_query(self, db_name: str, query: str, params: tuple = None, multi: bool = False):
        # YTEST: 특정 계정 DB에 대한 쿼리 실행 (root 권한으로 해당 DB 접근)
        try:
            with MySQLConnection(database=db_name, user=settings.MYSQL_USER, password=settings.MYSQL_ROOT_PASSWORD) as conn:
                if conn:
                    cursor = conn.cursor()
                    if multi:
                        for result in cursor.execute(query, params, multi=True):
                            pass
                    else:
                        cursor.execute(query, params)
                    conn.commit()
                    return cursor
        except Error as e:
            print(f"Error executing account DB query for {db_name}: {e}")
            raise

    def create(self, obj_in: SubAccountCreateDTO) -> SubAccount:
        # YTEST: 새 계정 생성 및 MySQL DB/사용자 할당
        if not self._is_valid_account_name(obj_in.username):
            raise ValueError(f"Invalid or reserved account name: {obj_in.username}")

        # YTEST: 이미 존재하는 DB 이름 또는 사용자 이름인지 확인

        try:
            with MySQLConnection() as conn:
                if conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{obj_in.username}'")
                    if cursor.fetchone():
                        raise ValueError(f"SubAccount with username '{obj_in.username}' already exists (DB name taken).")
                    cursor.execute(f"SELECT User FROM mysql.user WHERE User = '{obj_in.username}'")
                    if cursor.fetchone():
                        raise ValueError(f"SubAccount with username '{obj_in.username}' already exists (DB user taken).")
        except Error as e:
            raise RuntimeError(f"Database check failed: {e}")

        db_name = db_user = obj_in.username
        db_password = obj_in.password  # YTEST: 실제 환경에서는 보안 강화 필요 (랜덤 비밀번호 생성, 해싱 등)

        # YTEST: MySQL DB 및 사용자 생성, 권한 부여
        self._execute_admin_query(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
        self._execute_admin_query(f"CREATE USER '{db_user}'@'localhost' IDENTIFIED BY '{db_password}';")
        self._execute_admin_query(f"GRANT ALL PRIVILEGES ON `{db_name}`.* TO '{db_user}'@'localhost';")
        self._execute_admin_query("FLUSH PRIVILEGES;")  # YTEST: 권한 변경 즉시 적용

        # YTEST: 계정 DB에 초기 스키마 적용
        with open("app/database/schemas.sql", "r") as f:
            schemas_sql_content = f.read()
        self._execute_account_db_query(db_name, schemas_sql_content, multi=True)

        # YTEST: 트리거 및 이벤트 생성
        self._execute_account_db_query(db_name, TriggerQueries.create_user_insert_log_trigger(db_name))
        self._execute_account_db_query(db_name, EventQueries.create_daily_cleanup_event(db_name))

        # YTEST: 계정 정보 (users 테이블에) 초기 삽입
        insert_initial_data_query = "INSERT INTO users (worker_id, worker_enpw) VALUES (%s, %s);"
        self._execute_account_db_query(db_name, insert_initial_data_query, params=(db_user, obj_in.email))

        return SubAccount(id=1, username=obj_in.username, password=obj_in.password, email=obj_in.email, created_at=datetime.now(), db_name=db_name, db_user=db_user, db_password=db_password)

    def get(self, id: int) -> Optional[SubAccount]:
        # YTEST: 계정 정보 조회 (현재는 더미 데이터)
        account: List[SubAccount] = []
        query = """
                    SELECT * FROM worker 
                    WHERE worker_uid = %s AND is_del != 'Y' AND display_type=''
                """
        try:
            with MySQLConnection() as conn:
                conns = conn
                if not conn:
                    logger.error(f"Failed to get DB connection for get(id={id}).")
                    return None
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query, (id,))
                result = cursor.fetchone()  # <--- fetchall() 대신 fetchone()을 사용합니다.
                cursor.close()

                if result:
                    logger.info(f"SubAccount found for worker_uid: {id}")
                    # DB에서 받은 딕셔너리로 SubAccount 모델 인스턴스를 생성하여 반환합니다.
                    return SubAccount(**result)
                else:
                    logger.warning(f"SubAccount not found for worker_uid: {id}")
                    return None
        except Error as e:
            logger.error(f"Error retrieving multiple accounts: {e}", exc_info=True)
            raise RuntimeError(f"Failed to retrieve accounts from database: {e}")

    def get_by_field(self, field: str, value: str) -> Optional[SubAccount]:
        # YTEST: 특정 필드(예: username)로 계정 정보 조회 (현재는 DB 이름 존재 여부만 확인)
        if field == "worker_uid":
            try:
                with MySQLConnection() as conn:
                    if conn:
                        cursor = conn.cursor()
                        cursor.execute(
                            f"SELECT worker_id FROM worker WHERE worker_id = '{value}'")
                        result = cursor.fetchone()  # <--- fetchall() 대신 fetchone()을 사용합니다.
                        cursor.close()
                        if result:
                            return SubAccount(**result)
            except Error as e:
                raise RuntimeError(f"Database check failed: {e}")
        return None

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[SubAccount]:
        # YTEST: 여러 계정 정보 조회 (현재는 더미 데이터)
        print("YTEST: Retrieving multiple accounts (Not implemented in DB)")
        """
                데이터베이스에서 여러 계정 정보를 조회합니다. (페이지네이션 적용)
                """
        # logger.info(f"Retrieving multiple accounts from DB with skip={skip}, limit={limit}")
        accounts: List[SubAccount] = []

        query = """
                    SELECT * FROM worker 
                    WHERE is_del != 'Y'
                    AND display_type=''
                    ORDER BY worker_uid DESC
                    LIMIT %s OFFSET %s
                """

        try:
            with MySQLConnection() as conn:
                if not conn:
                    logger.error("Failed to get database connection for get_multi.")
                    return []

                cursor = conn.cursor(dictionary=True)
                cursor.execute(query, (limit, skip))
                results = cursor.fetchall()
                cursor.close()

                for row in results:
                    # 각 row 딕셔너리를 SubAccount 모델 객체로 변환하여 리스트에 추가합니다.
                    accounts.append(SubAccount(**row))

                logger.info(f"Successfully retrieved {len(accounts)} accounts from DB.")

        except Error as e:
            logger.error(f"Error retrieving multiple accounts: {e}", exc_info=True)
            raise RuntimeError(f"Failed to retrieve accounts from database: {e}")

        return accounts

    def update(self, id: int, obj_in: SubAccountUpdateDTO) -> Optional[SubAccount]:
        # YTEST: 계정 정보 업데이트 (현재는 비밀번호 변경만 예시)
        print(f"YTEST: Updating account with ID: {id} with data: {obj_in.model_dump_json()} (Not fully implemented)")
        if obj_in.password and obj_in.username:  # YTEST: 계정 이름이 DTO에 포함되어야 함
            try:
                self._execute_admin_query(
                    f"ALTER USER '{obj_in.username}'@'localhost' IDENTIFIED BY '{obj_in.password}';")
                print(f"YTEST: Password for {obj_in.username} updated.")
            except Error as e:
                raise RuntimeError(f"Failed to update user password: {e}")
        # YTEST: 업데이트된 계정 정보를 다시 조회하여 반환 (실제로는 업데이트된 필드를 반영)
        updated_account = self.get(id)
        if updated_account and obj_in.email:
            updated_account.email = obj_in.email  # YTEST: 이메일만 로컬 업데이트 예시
        return updated_account

    def delete(self, id: int) -> bool:
        # YTEST: 계정 및 관련 DB/사용자 삭제 (현재는 더미 계정 이름 사용)
        account_to_delete_name = "test_account"  # YTEST: 실제로는 DB에서 ID를 통해 계정 이름을 조회해야 함
        # YTEST: 사용자, 이벤트, 트리거, DB 삭제
        self._execute_admin_query(f"DROP USER IF EXISTS '{account_to_delete_name}'@'localhost';")
        self._execute_account_db_query(account_to_delete_name, EventQueries.drop_daily_cleanup_event(account_to_delete_name))
        self._execute_account_db_query(account_to_delete_name, TriggerQueries.drop_user_insert_log_trigger(account_to_delete_name))
        self._execute_admin_query(f"DROP DATABASE IF EXISTS `{account_to_delete_name}`;")
        print(f"YTEST: SubAccount with ID: {id} and all associated resources deleted.")
        return True
# YTEST: 계정 리포지토리 구현 (CRUD 로직)
import mysql.connector
from mysql.connector import Error
from app.models.account import Account
from app.dtos.account import AccountCreateDTO, AccountUpdateDTO
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
class AccountRepository(BaseRepository[Account, AccountCreateDTO, AccountUpdateDTO]):
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

    def create(self, obj_in: AccountCreateDTO) -> Account:
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
                        raise ValueError(f"Account with username '{obj_in.username}' already exists (DB name taken).")
                    cursor.execute(f"SELECT User FROM mysql.user WHERE User = '{obj_in.username}'")
                    if cursor.fetchone():
                        raise ValueError(f"Account with username '{obj_in.username}' already exists (DB user taken).")
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

        return Account(id=1, username=obj_in.username, password=obj_in.password, email=obj_in.email, created_at=datetime.now(), db_name=db_name, db_user=db_user, db_password=db_password)

    def get(self, id: int) -> Optional[Account]:
        # YTEST: 계정 정보 조회 (현재는 더미 데이터)
        account: List[Account] = []
        query = """
                    SELECT * FROM worker 
                    WHERE worker_uid = %s AND is_del != 'Y' AND display_type='owner'
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
                    logger.info(f"Account found for worker_uid: {id}")
                    # DB에서 받은 딕셔너리로 Account 모델 인스턴스를 생성하여 반환합니다.
                    return Account(**result)
                else:
                    logger.warning(f"Account not found for worker_uid: {id}")
                    return None
        except Error as e:
            logger.error(f"Error retrieving multiple accounts: {e}", exc_info=True)
            raise RuntimeError(f"Failed to retrieve accounts from database: {e}")

    def get_by_field(self, field: str, value: str) -> Optional[Account]:
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
                            return Account(**result)
            except Error as e:
                raise RuntimeError(f"Database check failed: {e}")
        return None

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[Account]:
        # YTEST: 여러 계정 정보 조회 (현재는 더미 데이터)
        # print("YTEST: Retrieving multiple accounts (Not implemented in DB)")
        """
                데이터베이스에서 여러 계정 정보를 조회합니다. (페이지네이션 적용)
                """
        # logger.info(f"Retrieving multiple accounts from DB with skip={skip}, limit={limit}")
        accounts: List[Account] = []
        query = """
                    SELECT * FROM worker 
                    WHERE is_del != 'Y'
                    AND display_type='owner'
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
                    # 각 row 딕셔너리를 Account 모델 객체로 변환하여 리스트에 추가합니다.
                    accounts.append(Account(**row))

                logger.info(f"Successfully retrieved {len(accounts)} accounts from DB.")

        except Error as e:
            logger.error(f"Error retrieving multiple accounts: {e}", exc_info=True)
            raise RuntimeError(f"Failed to retrieve accounts from database: {e}")
        return accounts

    def update(self, id: int, obj_in: AccountUpdateDTO) -> Optional[Account]:
        """
        데이터베이스에서 특정 ID의 계정 정보를 업데이트합니다.
        - id: 업데이트할 계정의 worker_uid
        - obj_in: 업데이트할 데이터를 담은 DTO
        """
        # 1. DTO에서 업데이트할 필드만 동적으로 추출합니다.
        # model_dump(exclude_unset=True)는 값이 명시적으로 전달된 필드만 dict로 만듭니다.
        # 이렇게 하면 PATCH 메서드의 시맨틱(일부 필드만 업데이트)을 정확히 구현할 수 있습니다.
        update_data = obj_in.model_dump(exclude_unset=True)

        # 업데이트할 데이터가 없으면 아무 작업도 하지 않고, 현재 계정 정보를 반환합니다.
        if not update_data:
            logger.warning(f"Update called for worker_uid {id} but no data was provided.")
            return self.get(id)

        # 2. 동적으로 UPDATE 쿼리의 SET 절을 생성합니다.
        # 예: {"worker_name": "새이름", "department": "새부서"} -> "worker_name = %s, department = %s"
        set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
        query = f"UPDATE worker SET {set_clause} WHERE worker_uid = %s"
        print("query",query)
        # 쿼리에 바인딩할 파라미터들을 튜플로 만듭니다.
        params = tuple(update_data.values()) + (id,)

        logger.debug(f"Executing update query: {query} with params: {params}")

        try:
            # 3. 'get' 메서드처럼 DB에 연결하고 쿼리를 실행합니다.
            with MySQLConnection() as conn:
                if not conn:
                    logger.error(f"Failed to get DB connection for update(id={id}).")
                    return None

                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                cursor.close()

                # 4. 변경 사항이 적용되었는지 확인하고, 업데이트된 전체 객체를 반환합니다.
                if cursor.rowcount > 0:
                    logger.info(
                        f"Successfully updated account for worker_uid: {id}. Fields: {list(update_data.keys())}")
                    # 업데이트된 최신 정보를 다시 조회하여 반환하는 것이 가장 확실한 방법입니다.
                    return self.get(id)
                else:
                    # WHERE 조건에 맞는 행이 없거나, 값이 변경되지 않은 경우
                    logger.warning(
                        f"Update query executed for worker_uid: {id}, but no rows were affected. The account may not exist or the data was the same.")
                    # 계정이 존재하는지 확인 후 반환
                    return self.get(id)

        except Error as e:
            logger.error(f"Error updating account for worker_uid {id}: {e}", exc_info=True)
            raise RuntimeError(f"Failed to update account in database: {e}")

    def delete(self, id: int) -> bool:
        """
        데이터베이스에서 특정 ID의 계정을 '논리적'으로 삭제합니다 (soft delete).
        실제 행을 삭제하는 대신 'is_del' 플래그를 'Y'로 설정합니다.
        - id: 삭제할 계정의 worker_uid
        - 반환값: 성공 시 True, 실패 또는 대상 없음 시 False
        """

        return True   #YCHECK강제성공
        return False  #YCHECK강제실패

        # 이미 삭제된 행을 다시 업데이트하지 않도록 조건 추가
        query = "UPDATE worker SET is_del = 'Y' WHERE worker_uid = %s AND is_del != 'Y'"
        params = (id,)

        logger.info(f"Attempting to soft delete account with worker_uid: {id}")

        try:
            with MySQLConnection() as conn:
                if not conn:
                    logger.error(f"Failed to get DB connection for delete(id={id}).")
                    return False

                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()

                # cursor.rowcount는 쿼리에 의해 영향을 받은 행의 수를 반환합니다.
                # 1이면 성공적으로 업데이트된 것이고, 0이면 해당 ID의 계정이 없거나 이미 삭제된 상태입니다.
                rows_affected = cursor.rowcount
                cursor.close()

                if rows_affected > 0:
                    logger.info(f"Successfully soft-deleted account with worker_uid: {id}")
                    return True
                else:
                    logger.warning(f"Account with worker_uid: {id} not found or already deleted. No rows affected.")
                    return False

        except Error as e:
            logger.error(f"Error deleting account for worker_uid {id}: {e}", exc_info=True)
            # DB 에러가 발생하면 상위 계층에서 처리하도록 예외를 다시 발생시킵니다.
            raise RuntimeError(f"Failed to delete account in database: {e}")
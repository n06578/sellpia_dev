from mysql.connector import Error
from app.repositories.subaccount_models import SubAccount
from app.dtos.subaccount import SubAccountCreateDTO, SubAccountUpdateDTO
from app.repositories.base import BaseRepository
from app.database.connection import MySQLConnection
from typing import List, Optional
from datetime import datetime
import logging
import hashlib

logger = logging.getLogger(__name__)
class SubAccountRepository(BaseRepository[SubAccount, SubAccountCreateDTO, SubAccountUpdateDTO]):
    def __init__(self):
        pass

    def create(self, obj_in: SubAccountCreateDTO) -> SubAccount:
        # DB 부운영자 추가
        now = datetime.now()
        now_datetime=  now.strftime('%Y-%m-%d %H:%M:%S')
        try:
            with MySQLConnection() as conn:
                if conn:
                    insert_data = obj_in.model_dump(exclude_unset=True)
                    if not insert_data:
                        logger.warning(f"Update called for worker_uid {id} but no data was provided.")
                        return self.get(obj_in.worker_id)
                    # db 저장시 필요한 기본값 설정
                    insert_data["reg_date"] = now_datetime

                    #query 작성
                    set_clause = ", ".join([f"`{key}` = %s" for key in insert_data.keys()])
                    query = f"INSERT INTO `worker` SET {set_clause}"
                    params = tuple(insert_data.values())

                    #mysql 접속 후 query 실행
                    cursor = conn.cursor()
                    cursor.execute(query, params)
                    conn.commit()
                    cursor.close()
        except Error as e:
            raise RuntimeError(f"Database check failed: {e}")

        return SubAccount(worker_id = obj_in.worker_id,worker_name = obj_in.worker_name,worker_cellphone = obj_in.worker_cellphone)

    def get(self, id: str) -> Optional[SubAccount]: 
        # 단일 계정 조회
        logger.warning(f"?? {id}")
        query = """
                    SELECT * FROM worker 
                    WHERE worker_id = %s AND is_del = 'N' AND display_type=''
                """
        try:
            with MySQLConnection() as conn:
                if not conn:
                    logger.error(f"db 접속 실패 : get({id}).")
                    return None
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query, (id,))
                result = cursor.fetchone()  # <--- fetchall() 대신 fetchone()을 사용합니다.
                cursor.close()

                if result:
                    logger.info(f"SubAccount found for worker_uid: {id}")
                    return SubAccount(**result)
                else:
                    logger.warning(f"SubAccount not found for worker_uid: {id}")
                    return None

        except Error as e:
            logger.error(f"Error retrieving multiple accounts: {e}", exc_info=True)
            raise RuntimeError(f"Failed to retrieve accounts from database: {e}")

    def update(self, id: str, obj_in: SubAccountUpdateDTO) -> Optional[SubAccount]:
        # 계정 정보 수정
        now = datetime.now()
        now_datetime=  now.strftime('%Y-%m-%d %H:%M:%S')
        try:
            with MySQLConnection() as conn:
                if conn:
                    update_data = obj_in.model_dump(exclude_unset=True)

                    if not update_data:
                        logger.warning(f"Update called for worker_uid {id} but no data was provided.")
                        updated_subaccount = self.get(id)
                        return updated_subaccount

                    set_clause = ", ".join([f"`{key}` = %s" for key in update_data.keys()])
                    print(set_clause)
                    query = f"UPDATE `worker` SET {set_clause} WHERE `worker_id` = %s AND is_del='N'"
                    params = tuple(update_data.values()) + (id,)

                    cursor = conn.cursor()
                    cursor.execute(query, params)
                    conn.commit()
                    cursor.close()
                    updated_subaccount = self.get(id)

        except Error as e:
            raise RuntimeError(f"Database check failed: {e}")
        return updated_subaccount

    def delete(self, id: str) -> bool:
        query = "UPDATE worker SET is_del = 'Y' WHERE worker_id = %s AND is_del = 'N'"
        try:
            with MySQLConnection() as conn:
                if not conn:
                    logger.error(f"Failed to get DB connection for delete(id={id}).")
                    return False

                cursor = conn.cursor()
                cursor.execute(query, (id,))
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
        return True
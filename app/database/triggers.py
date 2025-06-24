# YTEST: MySQL 트리거 생성/삭제 쿼리 정의
class TriggerQueries:
    @staticmethod
    def create_user_insert_log_trigger(db_name: str) -> str:
        # YTEST: users 테이블에 새 레코드가 삽입될 때 로그를 남기는 트리거
        return f"""
        USE {db_name};
        CREATE TRIGGER IF NOT EXISTS trg_user_insert_log
        AFTER INSERT ON users
        FOR EACH ROW
        BEGIN
            -- INSERT INTO audit_log (table_name, action, new_data, timestamp)
            -- VALUES ('users', 'INSERT', JSON_OBJECT('id', NEW.id, 'username', NEW.username), NOW());
            -- YTEST: 실제 감사 로그 테이블이 필요하다면 주석 해제 및 수정
        END;
        """

    @staticmethod
    def drop_user_insert_log_trigger(db_name: str) -> str:
        return f"""
        USE {db_name};
        DROP TRIGGER IF EXISTS trg_user_insert_log;
        """

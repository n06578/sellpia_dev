# YTEST: MySQL 이벤트 생성/삭제 쿼리 정의
class EventQueries:
    @staticmethod
    def create_daily_cleanup_event(db_name: str) -> str:
        # YTEST: 매일 자정에 특정 테이블의 오래된 데이터를 정리하는 이벤트
        return f"""
        USE {db_name};
        SET GLOBAL event_scheduler = ON; -- YTEST: 이벤트 스케줄러 활성화 (필요시)
        CREATE EVENT IF NOT EXISTS evt_daily_cleanup
        ON SCHEDULE EVERY 1 DAY
        STARTS (CURRENT_DATE + INTERVAL 1 DAY + INTERVAL 0 HOUR) -- YTEST: 다음 날 자정부터 시작
        ON COMPLETION PRESERVE
        DO
        BEGIN
            -- DELETE FROM old_logs WHERE created_at < NOW() - INTERVAL 30 DAY;
            -- YTEST: 30일 이상된 로그 삭제 예시
            SELECT 'Daily cleanup event executed' AS message; -- YTEST: 이벤트 실행 확인용
        END;
        """

    @staticmethod
    def drop_daily_cleanup_event(db_name: str) -> str:
        return f"""
        USE {db_name};
        DROP EVENT IF EXISTS evt_daily_cleanup;
        """

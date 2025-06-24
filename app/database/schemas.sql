-- YTEST: 계정 생성 시 해당 계정의 DB에 생성될 기본 테이블 스키마
-- app/database/connection.py 에서 직접 읽어서 실행
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT DEFAULT 0
);

-- YTEST: 필요한 다른 기본 테이블들을 여기에 추가

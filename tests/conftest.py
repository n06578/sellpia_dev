import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.middlewares.ip_filter import IPFilterMiddleware

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


# $env:ENV="test"; pytest -s #success된 내용도 print 처리
# $env:ENV="test"; pytest --disable-pytest-warnings #warning 미출력 처리
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_subaccount():
    #아래로 test 데이터 생성된거 x -> services/subaccount.py의 데이터로 강제 변환됨
    subaccount_data = {
        "worker_uid": 120,
        "worker_id": "test_worker_01",
        "worker_enpw": "testpassword123",
        "is_del": "N",
        "worker_name": "테스트 작업자",
        "worker_cellphone": "010-1234-5678",
        "department": "개발팀"
    }
    response = client.post(
        "/api/v1/subaccount/",
        json=subaccount_data
    )
    print("\n🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 ")
    print(" ✅ test_create_subaccount / Status Code:", response.status_code)
    print(" ✅ Response JSON \n", response.json())
    assert response.status_code == 201


def test_read_subaccount():
    response = client.get("/api/v1/subaccount/120")

    print("\n🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 ")
    print(" ✅ test_read_subaccount / Status Code:", response.status_code)
    print(" ✅ Response JSON \n", response.json())
    assert response.status_code == 200



def test_update_subaccount():
    subaccount_data = {
        "worker_uid": 121,
        "worker_id": "test_worker_01",
        "worker_enpw": "testpassword123",
        "is_del": "N",
        "worker_name": "테스트 작업자",
        "worker_cellphone": "010-1234-5678",
        "department": "개발팀"
    }
    response = client.patch(
        "/api/v1/subaccount/121",
        json=subaccount_data
    )
    print(
        "\n🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 ")
    print(" ✅ test_update_subaccount / Status Code:", response.status_code)
    print(" ✅ Response JSON \n", response.json())
    # print("\n🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 ")
    assert response.status_code == 200

def test_delete_subaccount():
    response = client.delete("/api/v1/subaccount/121")

    print("\n🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 ")
    print(" ✅ test_delete_subaccount / Status Code:", response.status_code)
    # print("\n🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 ")
    assert response.status_code == 204
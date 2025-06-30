import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime
client = TestClient(app)
#
# def test_create_subaccount():
#     subaccount_data = {
#         "worker_id": "pytest14",
#         "worker_name": "테스트 작업자",
#         "worker_cellphone": "010-1234-5678"
#     }
#     response = client.post(
#         "/api/v1/subaccount/",
#         json=subaccount_data
#     )
#     print("\n🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 ")
#     print(" ✅ test_create_subaccount / Status Code:", response.status_code)
#     print(" ✅ Response JSON \n", response.json())
#     assert response.status_code == 201


# def test_read_subaccount():
#     response = client.get("/api/v1/subaccount/pytest14")
#
#     print("\n🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 ")
#     print(" ✅ test_read_subaccount / Status Code:", response.status_code)
#     print(" ✅ Response JSON \n", response.json())
#     assert response.status_code == 200
#
#
#
# def test_update_subaccount():
#     subaccount_data = {
#         "worker_name": "250701001테스트",
#         "worker_cellphone": "010-2222-1111",
#     }
#     response = client.patch(
#         "/api/v1/subaccount/pytest14",
#         json=subaccount_data
#     )
#     print(
#         "\n🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 ")
#     print(" ✅ test_update_subaccount / Status Code:", response.status_code)
#     print(" ✅ Response JSON \n", response.json())
#     # print("\n🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 ")
#     assert response.status_code == 200


def test_delete_subaccount():
    response = client.delete("/api/v1/subaccount/pytest14")

    print("\n🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 ")
    print(" ✅ test_delete_subaccount / Status Code:", response.status_code)
    # print("\n🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 ")
    assert response.status_code == 204



# def test_create_subaccounts_bulk():
#     subaccount_data = [
#         {
#             "worker_id": "pytest8",
#             "worker_enpw": "testpassword123",
#             "is_del": "N",
#             "worker_name": "테스트 작업자",
#             "worker_cellphone": "010-1234-5678",
#             "department": "개발팀1",
#             "act_account": "test",
#             "display_type" : "",
#         "login_ip" : "",
#             "quick_menu" : "",
#             "access_pos_shop_uid" : "",
#             "worker_otp" : "",
#             "kiosk_access_token" : ""
#         },{
#             "worker_id": "pytest9",
#             "worker_enpw": "testpassword123",
#             "is_del": "N",
#             "worker_name": "테스트 작업자",
#             "worker_cellphone": "010-1234-5678",
#             "department": "개발팀2",
#             "act_account": "test",
#             "display_type" : "",
#             "login_ip" : "",
#             "quick_menu" : "",
#             "access_pos_shop_uid" : "",
#             "worker_otp" : "",
#             "kiosk_access_token" : ""
#         },
#     ]
#     response = client.post(
#         "/api/v1/subaccount/bulk",
#         json=subaccount_data
#     )
#     print("\n🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 🟪 ")
#     print(" ✅ test_create_subaccount / Status Code:", response.status_code)
#     print(" ✅ Response JSON \n", response.json())
#     assert response.status_code == 200

# import pytest
# from fastapi.testclient import TestClient
# from app.main import app
#
# client = TestClient(app)
#
# def test_create_provider():
#     #아래로 test 데이터 생성된거 x -> services/provider.py의 데이터로 강제 변환됨
#     provider_data = {
#         "provider_uid": 1,
#         "provider_id": "test_worker_01",
#         "provider_pw": "testpassword123",
#         "is_del": "N",
#         "provider_name": "테스트 작업자",
#         "provider_phone": "010-1234-5678",
#         "provider_etc": "개발팀"
#     }
#     response = client.post(
#         "/api/v1/provider/",
#         json=provider_data
#     )
#     print("\n🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 ")
#     print(" ✅ test_create_provider / Status Code:", response.status_code)
#     print(" ✅ Response JSON \n", response.json())
#     # print("\n🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 ")
#     assert response.status_code == 201
#
# def test_delete_provider():
#     response = client.delete("/api/v1/provider/121")
#
#     print("\n🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 ")
#     print(" ✅ test_delete_provider / Status Code:", response.status_code)
#     # print("\n🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 🟦 ")
#     assert response.status_code == 204
#
#
#
#
# ###### dtos/provider.py cell 내용 변경 필요
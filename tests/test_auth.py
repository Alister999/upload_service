# from tests.conftest import client

# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy.ext.asyncio import AsyncSession
#
# pytestmark = pytest.mark.asyncio
#
# async def test_post_register(client: TestClient, test_session: AsyncSession):
#     url = '/register'
#     data = {
#         "username": "Billy",
#         "password": "12345"
#     }
#     response = client.post(url, json=data, params={"test_engine": "test"})
#
#     assert response.status_code == 200
    # assert response.json() == '{"message":"User registered successfully"}'
#
#
# def test_post_login(client):
#     new_username = "Billy"
#     new_email = "bill@icloud.com"
#     new_password = "12345"
#
#     reg_url = '/register'
#     login_url = '/login'
#     reg_data = {
#       "username": new_username,
#       "email": new_email,
#       "password": new_password
#     }
#     reg_response = client.post(reg_url, json=reg_data)
#     login_data = {
#         "email": new_email,
#         "password": new_password
#     }
#     login_response = client.post(login_url, json=login_data)
#
#     assert login_response.status_code == 200
#     assert "access_token" in login_response.json()
#     assert "refresh_token" in login_response.json()
#     assert "token_type" in login_response.json()
#
#
# def test_post_login_fail(client):
#     new_email = "bill@icloud.com"
#     new_password = "12345"
#     login_url = '/login'
#     login_data = {
#         "email": new_email,
#         "password": new_password
#     }
#     login_response = client.post(login_url, json=login_data)
#
#     assert login_response.status_code == 401
#     assert login_response.text == '{"detail":"Invalid credentials"}'
#
#
# def test_post_refresh(client):
#     new_username = "Billy"
#     new_email = "bill@icloud.com"
#     new_password = "12345"
#
#     reg_url = '/register'
#     login_url = '/login'
#     refresh_url = '/refresh'
#     reg_data = {
#       "username": new_username,
#       "email": new_email,
#       "password": new_password
#     }
#     login_data = {
#         "email": new_email,
#         "password": new_password
#     }
#     reg_response = client.post(reg_url, json=reg_data)
#     login_response = client.post(login_url, json=login_data)
#     refresh_token = login_response.json()['refresh_token']
#     refresh_data = {
#         "refresh_token": refresh_token
#     }
#     refresh_responce = client.post(refresh_url, json=refresh_data)
#
#     assert refresh_responce.status_code == 200
#     assert "access_token" in refresh_responce.json()
#     assert not "refresh_token" in refresh_responce.json()

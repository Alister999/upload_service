import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.asyncio

async def test_get_files_unauth(client: TestClient):
    url = "/files"
    response = client.get(url)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


async def test_post_files_unauth(client: TestClient):
    url = '/upload'
    data = {
        "file": ""
    }
    response = client.post(url, json=data)

    assert response.status_code == 401
    assert response.text == '{"detail":"Not authenticated"}'


async def test_put_files_unauth(client: TestClient):
    url = '/files/3fa85f64-5717-4562-b3fc-2c963f66afa6'
    data = {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "hash": "string",
      "file_name": "string",
      "url": "string"
    }
    response = client.put(url, json=data)

    assert response.status_code == 401
    assert response.text == '{"detail":"Not authenticated"}'


async def test_delete_files_unauth(client: TestClient):
    url = '/files/3fa85f64-5717-4562-b3fc-2c963f66afa6'
    response = client.delete(url)

    assert response.status_code == 401
    assert response.text == '{"detail":"Not authenticated"}'


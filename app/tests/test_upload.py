import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.asyncio

async def test_post_files_unauth(client: TestClient):
    url = '/api/v1/upload'
    data = {
        "file": ""
    }
    response = client.post(url, json=data)

    assert response.status_code == 404
    assert response.text == '{"detail":"Not Found"}'
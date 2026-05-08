from unittest.mock import MagicMock

import pytest


@pytest.mark.asyncio
async def test_health_ok(client, mock_db):
    mock_db.execute.return_value = MagicMock()

    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_health_db_unavailable(client, mock_db):
    mock_db.execute.side_effect = Exception("connection refused")

    response = await client.get("/health")

    assert response.status_code == 503
    assert response.json()["detail"]["status"] == "error"

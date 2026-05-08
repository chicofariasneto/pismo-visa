import uuid
from unittest.mock import patch

import pytest

from app.models.account import Account

EXISTING_ACCOUNT = Account(id=uuid.uuid4(), document_number="12345678900")


@pytest.mark.asyncio
async def test_create_account_returns_201(client):
    with patch(
        "app.api.v1.endpoints.accounts.account_service.create_account",
        return_value=EXISTING_ACCOUNT,
    ):
        response = await client.post(
            "/api/v1/accounts/", json={"document_number": "12345678900"}
        )

    assert response.status_code == 201
    body = response.json()
    assert body["account_id"] == str(EXISTING_ACCOUNT.id)
    assert body["document_number"] == "12345678900"


@pytest.mark.asyncio
async def test_get_account_returns_200(client):
    with patch(
        "app.api.v1.endpoints.accounts.account_service.get_account",
        return_value=EXISTING_ACCOUNT,
    ):
        response = await client.get(f"/api/v1/accounts/{EXISTING_ACCOUNT.id}")

    assert response.status_code == 200
    body = response.json()
    assert body["account_id"] == str(EXISTING_ACCOUNT.id)
    assert body["document_number"] == "12345678900"


@pytest.mark.asyncio
async def test_get_account_returns_404_when_not_found(client):
    with patch(
        "app.api.v1.endpoints.accounts.account_service.get_account", return_value=None
    ):
        response = await client.get(f"/api/v1/accounts/{uuid.uuid4()}")

    assert response.status_code == 404

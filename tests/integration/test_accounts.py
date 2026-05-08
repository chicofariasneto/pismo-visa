import uuid

import pytest


@pytest.mark.asyncio
async def test_create_account(client):
    response = await client.post(
        "/api/v1/accounts/", json={"document_number": "12345678900"}
    )

    assert response.status_code == 201
    body = response.json()
    assert body["document_number"] == "12345678900"
    assert "account_id" in body
    uuid.UUID(body["account_id"])  # validates it is a valid UUID


@pytest.mark.asyncio
async def test_get_account(client):
    create_response = await client.post(
        "/api/v1/accounts/", json={"document_number": "12345678900"}
    )
    account_id = create_response.json()["account_id"]

    response = await client.get(f"/api/v1/accounts/{account_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["account_id"] == account_id
    assert body["document_number"] == "12345678900"


@pytest.mark.asyncio
async def test_get_account_not_found(client):
    response = await client.get(f"/api/v1/accounts/{uuid.uuid4()}")

    assert response.status_code == 404

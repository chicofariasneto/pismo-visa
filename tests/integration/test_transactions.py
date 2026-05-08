import uuid
from decimal import Decimal

import pytest


@pytest.mark.asyncio
async def test_create_transaction(client):
    create_account = await client.post(
        "/api/v1/accounts/", json={"document_number": "12345678900"}
    )
    account_id = create_account.json()["account_id"]

    response = await client.post(
        "/api/v1/transactions/",
        json={"account_id": account_id, "operation_type_id": 4, "amount": "123.45"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["account_id"] == account_id
    assert body["operation_type_id"] == 4
    assert Decimal(body["amount"]) == Decimal("123.45")
    assert "id" in body
    assert "event_date" in body


@pytest.mark.asyncio
async def test_create_transaction_negative_amount(client):
    create_account = await client.post(
        "/api/v1/accounts/", json={"document_number": "98765432100"}
    )
    account_id = create_account.json()["account_id"]

    response = await client.post(
        "/api/v1/transactions/",
        json={"account_id": account_id, "operation_type_id": 1, "amount": "-100.00"},
    )

    assert response.status_code == 201
    assert Decimal(response.json()["amount"]) == Decimal("-100.00")


@pytest.mark.asyncio
async def test_create_transaction_all_operation_types(client):
    create_account = await client.post(
        "/api/v1/accounts/", json={"document_number": "11122233300"}
    )
    account_id = create_account.json()["account_id"]

    cases = [
        (1, "-50.00"),  # Normal Purchase
        (2, "-150.00"),  # Purchase with installments
        (3, "-200.00"),  # Withdrawal
        (4, "300.00"),  # Credit Voucher
    ]

    for operation_type_id, amount in cases:
        response = await client.post(
            "/api/v1/transactions/",
            json={
                "account_id": account_id,
                "operation_type_id": operation_type_id,
                "amount": amount,
            },
        )
        assert (
            response.status_code == 201
        ), f"Failed for operation_type_id={operation_type_id}"


@pytest.mark.asyncio
async def test_create_transaction_account_not_found(client):
    response = await client.post(
        "/api/v1/transactions/",
        json={
            "account_id": str(uuid.uuid4()),
            "operation_type_id": 1,
            "amount": "-50.00",
        },
    )

    assert response.status_code == 404

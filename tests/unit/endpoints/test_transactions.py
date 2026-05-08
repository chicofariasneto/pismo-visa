import uuid
from datetime import datetime
from decimal import Decimal
from unittest.mock import patch

import pytest

from app.models.transaction import Transaction

EXISTING_TRANSACTION = Transaction(
    id=uuid.uuid4(),
    account_id=uuid.uuid4(),
    operation_type_id=4,
    amount=Decimal("123.45"),
    event_date=datetime(2026, 1, 1, 12, 0, 0),
)


@pytest.mark.asyncio
async def test_create_transaction_returns_201(client):
    with patch(
        "app.api.v1.endpoints.transactions.transaction_service.create_transaction",
        return_value=EXISTING_TRANSACTION,
    ):
        response = await client.post(
            "/api/v1/transactions/",
            json={
                "account_id": str(EXISTING_TRANSACTION.account_id),
                "operation_type_id": 4,
                "amount": "123.45",
            },
        )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == str(EXISTING_TRANSACTION.id)
    assert body["account_id"] == str(EXISTING_TRANSACTION.account_id)
    assert body["operation_type_id"] == 4
    assert Decimal(body["amount"]) == Decimal("123.45")


@pytest.mark.asyncio
async def test_create_transaction_returns_404_when_account_not_found(client):
    with patch(
        "app.api.v1.endpoints.transactions.transaction_service.create_transaction",
        return_value=None,
    ):
        response = await client.post(
            "/api/v1/transactions/",
            json={
                "account_id": str(uuid.uuid4()),
                "operation_type_id": 1,
                "amount": "-50.00",
            },
        )

    assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "operation_type_id,amount",
    [
        (1, "100.00"),  # Normal Purchase with positive amount
        (2, "50.00"),  # Purchase with installments with positive amount
        (3, "200.00"),  # Withdrawal with positive amount
        (4, "-30.00"),  # Credit Voucher with negative amount
        (1, "0.00"),  # zero amount on debit operation
        (4, "0.00"),  # zero amount on credit operation
    ],
)
async def test_create_transaction_returns_422_on_invalid_amount_sign(
    client, operation_type_id, amount
):
    response = await client.post(
        "/api/v1/transactions/",
        json={
            "account_id": str(uuid.uuid4()),
            "operation_type_id": operation_type_id,
            "amount": amount,
        },
    )

    assert response.status_code == 422

import uuid
from decimal import Decimal
from unittest.mock import AsyncMock, patch

import pytest

from app.models.account import Account
from app.schemas.transaction import TransactionCreate
from app.services import transaction_service


@pytest.fixture
def db():
    return AsyncMock()


@pytest.fixture
def existing_account():
    return Account(id=uuid.uuid4(), document_number="12345678900")


@pytest.mark.asyncio
async def test_create_transaction_success(db, existing_account):
    data = TransactionCreate(
        account_id=existing_account.id,
        operation_type_id=1,
        amount=Decimal("-100.00"),
    )

    with patch(
        "app.services.transaction_service.account_service.get_account",
        return_value=existing_account,
    ):
        result = await transaction_service.create_transaction(db, data)

    db.add.assert_called_once()
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once()
    assert result.account_id == existing_account.id
    assert result.operation_type_id == 1
    assert result.amount == Decimal("-100.00")


@pytest.mark.asyncio
async def test_create_transaction_account_not_found(db):
    data = TransactionCreate(
        account_id=uuid.uuid4(),
        operation_type_id=1,
        amount=Decimal("-50.00"),
    )

    with patch(
        "app.services.transaction_service.account_service.get_account",
        return_value=None,
    ):
        result = await transaction_service.create_transaction(db, data)

    assert result is None
    db.add.assert_not_called()
    db.commit.assert_not_awaited()


@pytest.mark.parametrize(
    "operation_type_id,amount",
    [
        (1, Decimal("-50.00")),  # Normal Purchase
        (2, Decimal("-150.00")),  # Purchase with installments
        (3, Decimal("-200.00")),  # Withdrawal
        (4, Decimal("300.00")),  # Credit Voucher
    ],
)
def test_transaction_create_schema_valid_amounts(operation_type_id, amount):
    data = TransactionCreate(
        account_id=uuid.uuid4(),
        operation_type_id=operation_type_id,
        amount=amount,
    )
    assert data.amount == amount


@pytest.mark.parametrize(
    "operation_type_id,amount",
    [
        (1, Decimal("50.00")),  # Normal Purchase with positive amount
        (2, Decimal("150.00")),  # Purchase with installments with positive amount
        (3, Decimal("200.00")),  # Withdrawal with positive amount
        (4, Decimal("-300.00")),  # Credit Voucher with negative amount
        (1, Decimal("0.00")),  # zero on debit operation
        (4, Decimal("0.00")),  # zero on credit operation
    ],
)
def test_transaction_create_schema_invalid_amounts(operation_type_id, amount):
    with pytest.raises(Exception):
        TransactionCreate(
            account_id=uuid.uuid4(),
            operation_type_id=operation_type_id,
            amount=amount,
        )

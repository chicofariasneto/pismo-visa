import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.account import Account
from app.schemas.account import AccountCreate
from app.services import account_service


@pytest.fixture
def db():
    return AsyncMock()


@pytest.mark.asyncio
async def test_create_account(db):
    data = AccountCreate(document_number="12345678900")

    result = await account_service.create_account(db, data)

    db.add.assert_called_once()
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once()
    assert result.document_number == "12345678900"
    assert result.id is not None


@pytest.mark.asyncio
async def test_get_account_found(db):
    account_id = uuid.uuid4()
    account = Account(id=account_id, document_number="12345678900")
    execute_result = MagicMock()
    execute_result.scalar_one_or_none.return_value = account
    db.execute.return_value = execute_result

    result = await account_service.get_account(db, account_id)

    assert result == account


@pytest.mark.asyncio
async def test_get_account_not_found(db):
    execute_result = MagicMock()
    execute_result.scalar_one_or_none.return_value = None
    db.execute.return_value = execute_result

    result = await account_service.get_account(db, uuid.uuid4())

    assert result is None

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from app.services import account_service


async def create_transaction(
    db: AsyncSession, data: TransactionCreate
) -> Transaction | None:
    """Create a new transaction linked to an existing account.

    Verifies that the referenced account exists before inserting.

    :param db: Active async database session.
    :type db: AsyncSession
    :param data: Validated transaction creation payload.
    :type data: TransactionCreate
    :returns: The newly created transaction, or ``None`` if the account was not found.
    :rtype: Transaction or None
    """
    account = await account_service.get_account(db, data.account_id)
    if account is None:
        return None

    transaction = Transaction(
        id=uuid.uuid4(),
        account_id=data.account_id,
        operation_type_id=data.operation_type_id,
        amount=data.amount,
    )
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from app.schemas.account import AccountCreate


async def create_account(db: AsyncSession, data: AccountCreate) -> Account:
    """Create a new account and persist it to the database.

    :param db: Active async database session.
    :type db: AsyncSession
    :param data: Validated account creation payload.
    :type data: AccountCreate
    :returns: The newly created account.
    :rtype: Account
    """
    account = Account(id=uuid.uuid4(), document_number=data.document_number)
    db.add(account)
    await db.commit()
    await db.refresh(account)
    return account


async def get_account(db: AsyncSession, account_id: uuid.UUID) -> Account | None:
    """Retrieve an account by its primary key.

    :param db: Active async database session.
    :type db: AsyncSession
    :param account_id: UUID of the account to look up.
    :type account_id: uuid.UUID
    :returns: The matching account, or ``None`` if not found.
    :rtype: Account or None
    """
    result = await db.execute(select(Account).where(Account.id == account_id))
    return result.scalar_one_or_none()

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.account import AccountCreate, AccountResponse
from app.services import account_service

router = APIRouter()


@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(body: AccountCreate, db: AsyncSession = Depends(get_db)):
    """Create a new account.

    :param body: Account creation payload containing the document number.
    :type body: AccountCreate
    :param db: Injected async database session.
    :type db: AsyncSession
    :returns: The created account.
    :rtype: AccountResponse
    """
    return await account_service.create_account(db, body)


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(account_id: UUID, db: AsyncSession = Depends(get_db)):
    """Retrieve an account by ID.

    :param account_id: UUID of the account to retrieve.
    :type account_id: UUID
    :param db: Injected async database session.
    :type db: AsyncSession
    :returns: The matching account.
    :rtype: AccountResponse
    :raises HTTPException: 404 if the account does not exist.
    """
    account = await account_service.get_account(db, account_id)
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    return account

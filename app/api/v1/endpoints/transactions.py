from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services import transaction_service

router = APIRouter()


@router.post(
    "/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED
)
async def create_transaction(
    body: TransactionCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new transaction for an existing account.

    :param body: Transaction payload containing account ID, operation type and amount.
    :type body: TransactionCreate
    :param db: Injected async database session.
    :type db: AsyncSession
    :returns: The created transaction.
    :rtype: TransactionResponse
    :raises HTTPException: 404 if the referenced account does not exist.
    """
    transaction = await transaction_service.create_transaction(db, body)
    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    return transaction

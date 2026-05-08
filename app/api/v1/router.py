from fastapi import APIRouter

from app.api.v1.endpoints import accounts, transactions

router = APIRouter()

router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
router.include_router(
    transactions.router, prefix="/transactions", tags=["transactions"]
)

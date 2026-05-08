from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TransactionCreate(BaseModel):
    account_id: UUID
    operation_type_id: int
    amount: Decimal


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    account_id: UUID
    operation_type_id: int
    amount: Decimal
    event_date: datetime

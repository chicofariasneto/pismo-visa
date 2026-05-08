from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_validator

_DEBIT_OPERATIONS = {1, 2, 3}
_CREDIT_OPERATIONS = {4}


class TransactionCreate(BaseModel):
    account_id: UUID
    operation_type_id: int
    amount: Decimal

    @model_validator(mode="after")
    def validate_amount_sign(self) -> "TransactionCreate":
        """Enforce amount sign based on operation type.

        Debit operations (purchase, withdrawal) require a negative amount.
        Credit operations (credit voucher) require a positive amount.

        :raises ValueError: If the amount sign does not match the operation type.
        :returns: The validated model instance.
        :rtype: TransactionCreate
        """
        if self.operation_type_id in _DEBIT_OPERATIONS and self.amount >= 0:
            raise ValueError(
                "Amount must be negative for purchase and withdrawal operations"
            )
        if self.operation_type_id in _CREDIT_OPERATIONS and self.amount <= 0:
            raise ValueError("Amount must be positive for credit voucher operations")
        return self


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    account_id: UUID
    operation_type_id: int
    amount: Decimal
    event_date: datetime

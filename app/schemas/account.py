from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AccountCreate(BaseModel):
    document_number: str


class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    account_id: UUID = Field(validation_alias="id")
    document_number: str

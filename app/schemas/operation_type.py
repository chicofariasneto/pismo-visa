from pydantic import BaseModel, ConfigDict


class OperationTypeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str

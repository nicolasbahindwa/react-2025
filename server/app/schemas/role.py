from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

class RoleBase(BaseModel):
    name: str = Field(..., max_length=50, description="The name of the role.")
    description: Optional[str] = Field(None, max_length=255, description="A description of the role.")

class RoleCreate(RoleBase):
    pass  # You can add additional fields or validation here if needed.

class RoleResponse(RoleBase):
    id: UUID = Field(..., description="The unique identifier of the role.")

    class Config:
        orm_mode = True  # This allows Pydantic to read data from SQLAlchemy models.

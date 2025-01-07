from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
import uuid
from uuid import UUID

class PostBase(BaseModel):
  
    title: str = Field(..., min_length=1, max_length=100, description='Post Title')
    content: str = Field(..., min_length=1, description='Post Content')
    published: bool = Field(default=True, description='Publication status')
    author: str = Field(..., min_length=1, description='Publication author')
    class Config:
        from_attributes = True
        orm_mode = True 

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="Updated Post Title")
    content: Optional[str] = Field(None, min_length=1, description="Updated Post Content")
    published: Optional[bool] = Field(None, description="Updated Publication status")
    author:Optional[str] = Field(None, description="Updated Publication ")
    
    model_config = ConfigDict(extra='forbid')

class PostResponse(PostBase):
    id: UUID = Field(default_factory=uuid.uuid4)
    slug: str
    created_at: datetime
    updated_at: datetime

class PostPatch(PostUpdate):
    model_config = ConfigDict(extra='forbid')
    pass

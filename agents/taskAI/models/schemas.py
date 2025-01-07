# models/schemas.py
from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field

class Profile(BaseModel):
    """User profile schema"""
    name: Optional[str] = Field(description="The user's name", default=None)
    location: Optional[str] = Field(description="The user's location", default=None)
    job: Optional[str] = Field(description="The user's job", default=None)
    connections: list[str] = Field(description="Personal connections", default_factory=list)
    interests: list[str] = Field(description="User interests", default_factory=list)

class ToDo(BaseModel):
    """ToDo item schema"""
    task: str = Field(description="The task to be completed.")
    time_to_complete: Optional[int] = Field(description="Estimated time (minutes).")
    deadline: Optional[datetime] = Field(description="Task deadline", default=None)
    solutions: list[str] = Field(description="Actionable solutions", min_items=1, default_factory=list)
    status: Literal["not started", "in progress", "done", "archived"] = Field(
        description="Task status", default="not started"
    )

class UpdateMemory(TypedDict):
    """Decision on what memory type to update"""
    update_type: Literal["user", "todo", "instructions"]
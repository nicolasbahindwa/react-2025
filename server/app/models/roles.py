from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.models import user_roles
# Association table for the many-to-many relationship between User and Role
 
class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    
    # Relationship with users
    users = relationship("User", secondary=user_roles, back_populates="roles")

    def __repr__(self):
        return f"<Role(name={self.name})>"


    @property
    def assigned_roles(self):
        """Ensure roles are properly loaded"""
        return self.roles
    
 
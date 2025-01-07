from sqlalchemy import Column, String, Boolean, event, inspect
from sqlalchemy.sql import func
# from app.database import Base
from app.database.base_model import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates, object_session
import uuid
from slugify import slugify

class Post(BaseModel):
    __tablename__ = "posts"
    extend_existing=True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    content = Column(String, nullable=False)
    author = Column(String, nullable=False)
    published = Column(Boolean, server_default='true')

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title cannot be empty")
        return title
    
    def generate_slug(self) -> str:
        """Generate a slug from the title"""
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1

        while True:
            existing_slug = object_session(self).query(Post).filter(
                Post.slug == slug,
                Post.id != self.id,
            ).first()
            if not existing_slug:
                break
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug
    

@event.listens_for(Post, 'before_insert')
def generate_slug_on_insert(mapper, connection, target):
    if target.title:
        target.slug = target.generate_slug()

@event.listens_for(Post, 'before_update')
def update_slug_on_title_change(mapper, connection, target):
    if inspect(target).attrs.title.history.has_changes() and target.title:
        target.slug = target.generate_slug()

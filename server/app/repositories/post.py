from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate, PostPatch
from .base import BaseRepository

class PostRepository(BaseRepository[Post, PostCreate, PostUpdate,PostPatch]):
    pass
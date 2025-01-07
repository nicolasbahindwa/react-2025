from datetime import datetime
from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr


class TimestampMixin:
    """Mixin for adding created_at and updated_at timestamps to models"""

    created_at = Column(DateTime(timezone=True),
                       server_default=func.now(),
                       nullable=False,
                       comment="Timestamp when record was created")
    
    updated_at = Column(DateTime(timezone=True),
                       server_default=func.now(),
                       onupdate=func.now(),
                       nullable=False,
                       comment="Timestamp when record was last updated")
    
class TableNameMixin:
    """Mixin for adding a table name to models"""
    @declared_attr
    def __tablename__(cls) ->str:
        return cls.__name__.lower() + "s"

class ReprMixin:
    def __repr__(self) -> str:
        attrs = []
        for key in self.__mapper__.columns.keys():
            if key in ['created_at', 'updated_at']:
                continue
            value = getattr(self, key)
            attrs.append(f"{key}={value!r}")
        return f"<{self.__class__.__name__} {', '.join(attrs)}>"
    
from app.database.base import Base
from app.database.mixins import TimestampMixin,TableNameMixin, ReprMixin


class BaseModel(TimestampMixin, ReprMixin, TableNameMixin, Base):
    """
        Base model class that combines all mixins and base functionality.
        All models should inherit from this class.
    """
    __abstract__ = True
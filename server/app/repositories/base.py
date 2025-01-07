from typing import TypeVar, Generic, Type, Optional, List, Any, Dict
from uuid import UUID
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, String, or_, func
from pydantic import BaseModel
from app.database import Base
from app.exceptions.database import DatabaseError, NotFoundException, InvalidFieldException
from app.core.logging import app_logger
from app.schemas.common import PaginatedResponse
from app.database.session import managed_transaction

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
PatchSchemaType = TypeVar("PatchSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType, PatchSchemaType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db
    
    def _log_context(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Create a standard context dictionary for logging"""
        context = {
            "model": self.model.__name__,
            "operation": operation,
            **kwargs
        }
        return {k: v for k, v in context.items() if v is not None}

    async def get_all(
        self, 
        *, 
        skip: int = 0, 
        limit: int = 100, 
        order_by: Optional[List[str]] = None, 
        filters: Optional[Dict[str, Any]] = None
    ) -> PaginatedResponse[ModelType]:
        """Retrieve all records with optional filters, pagination, and ordering."""
        context = self._log_context(
            "get_all",
            skip=skip,
            limit=limit,
            order_by=order_by,
            filters=filters
        )
        
        try:
            query = select(self.model)
            
            app_logger.log_success(
                f"Initiating get_all query for {self.model.__name__}",
                extra=context
            )

            if filters:
                for field, value in filters.items():
                    query = query.filter(getattr(self.model, field) == value)

            if order_by:
                for field in order_by:
                    if field.startswith('-'):
                        query = query.order_by(getattr(self.model, field[1:]).desc())
                    else:
                        query = query.order_by(getattr(self.model, field).asc())

            # Count total items
            total_query = select(func.count()).select_from(self.model)
            if query._where_criteria:
                total_query = total_query.where(*query._where_criteria)
                
            total_result = await self.db.execute(total_query)
            total = total_result.scalar()

            # Get paginated results
            result = await self.db.execute(query.offset(skip).limit(limit))
            items = result.scalars().all()

            app_logger.log_success(
                f"Successfully retrieved {len(items)} {self.model.__name__} records",
                extra={**context, "result_count": len(items)}
            )

            return PaginatedResponse(
                items=items,
                total=total,
                page=(skip // limit) + 1,
                page_size=limit
            )

        except Exception as e:
            app_logger.log_error(
                f"Error retrieving {self.model.__name__} list: {str(e)}",
                error=e,
                extra=context
            )
            raise DatabaseError(f"Error retrieving {self.model.__name__} list: {str(e)}")

    async def get_by_id(self, id: UUID) -> Optional[ModelType]:
        """Retrieve a record by ID."""
        context = self._log_context("get_by_id", id=str(id))
        
        try:
            query = select(self.model).filter(self.model.id == id)
            result = await self.db.execute(query)
            item = result.scalar_one_or_none()
            
            app_logger.log_success(
                f"Retrieved {self.model.__name__} by ID",
                extra=context
            )
            if not item:
                raise NotFoundException(self.model.__name__, id)
                
            return item
            
        except NotFoundException:
            raise
        except Exception as e:
            app_logger.log_error(
                f"Error retrieving {self.model.__name__} by ID: {str(e)}",
                error=e,
                extra=context
            )
            raise DatabaseError(f"Error retrieving {self.model.__name__}: {str(e)}")

 
    async def get_by_any_field(
        self, 
        value: str,
        skip: int = 0,
        limit: int = 100
    ) -> PaginatedResponse[ModelType]:
        """ Search records where any string-compatible field matches the provided value.
            
            Args:
                value: Search value to match against any field
                skip: Number of records to skip
                limit: Maximum number of records to return
                
            Returns:
                PaginatedResponse containing matching model instances
                
            Raises:
                DatabaseError: If the search operation fails
            """
        context = self._log_context(
            "get_by_any_field", 
            search_value=value,
            skip=skip,
            limit=limit
        )
        
        try:
            # Build query with conditions for each string-compatible column
            query = select(self.model)
            conditions = []
            
            for column in self.model.__table__.columns:
                # Skip UUID fields and other non-string-compatible types
                if column.type.python_type not in (UUID, bool, dict, list):
                    conditions.append(
                        getattr(self.model, column.name).cast(String).ilike(f"%{value}%")
                    )
            
            if conditions:
                query = query.filter(or_(*conditions))
            
            # Count total items
            total_query = select(func.count()).select_from(self.model)
            if query._where_criteria:
                total_query = total_query.where(*query._where_criteria)
                
            total_result = await self.db.execute(total_query)
            total = total_result.scalar()
            
            # Get paginated results
            result = await self.db.execute(query.offset(skip).limit(limit))
            items = list(result.scalars().all())
            
            app_logger.log_success(
                f"Found {len(items)} matching {self.model.__name__} records",
                extra={**context, "result_count": len(items)}
            )
            
            return PaginatedResponse(
                items=items,
                total=total,
                page=(skip // limit) + 1,
                page_size=limit
            )
            
        except Exception as e:
            app_logger.log_error(
                f"Error searching {self.model.__name__} by any field: {str(e)}",
                error=e,
                extra=context
            )
            raise DatabaseError(f"Error searching {self.model.__name__}: {str(e)}")


    async def create(self, schema: CreateSchemaType) -> ModelType:
        """Create a new record."""
        async with managed_transaction(self.db):
            try:
                db_obj = self.model(**schema.model_dump())
                self.db.add(db_obj)
                await self.db.flush()
                
                context = self._log_context("create", id=str(db_obj.id))
                app_logger.log_success(
                    f"Successfully created {self.model.__name__}",
                    extra=context
                )
                
                return db_obj
                
            except Exception as e:
                app_logger.log_error(
                    f"Error creating {self.model.__name__}: {str(e)}",
                    error=e,
                    extra=self._log_context("create")
                )
                raise DatabaseError(f"Error creating {self.model.__name__}: {str(e)}")

    async def update(
        self, 
        *, 
        id: UUID, 
        schema: UpdateSchemaType, 
        auto_commit: bool = True
    ) -> ModelType:
        """Update an existing record."""
        context = self._log_context("update", id=str(id))
        
        try:
            db_obj = await self.get_by_id(id)
            obj_data = schema.model_dump(exclude_unset=True)

            for field, value in obj_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
                else:
                    raise InvalidFieldException(f"Field '{field}' is invalid for {self.model.__name__}")

            if auto_commit:
                await self.db.commit()
                await self.db.refresh(db_obj)

            app_logger.log_success(
                f"Successfully updated {self.model.__name__}",
                extra=context
            )
            
            return db_obj
            
        except Exception as e:
            app_logger.log_error(
                f"Error updating {self.model.__name__}: {str(e)}",
                error=e,
                extra=context
            )
            await self.db.rollback()
            raise DatabaseError(f"Error updating {self.model.__name__}: {str(e)}")

    async def delete(self, id: UUID) -> bool:
        """Delete a record by ID."""
        context = self._log_context("delete", id=str(id))
        
        async with managed_transaction(self.db):
            try:
                db_obj = await self.get_by_id(id)
                await self.db.delete(db_obj)
                
                app_logger.log_success(
                    f"Successfully deleted {self.model.__name__}",
                    extra=context
                )
                
                return True
                
            except NotFoundException:
                raise
            except Exception as e:
                app_logger.log_error(
                    f"Error deleting {self.model.__name__}: {str(e)}",
                    error=e,
                    extra=context
                )
                raise DatabaseError(f"Error deleting {self.model.__name__}: {str(e)}")

    async def patch(
        self, 
        *, 
        id: UUID, 
        schema: PatchSchemaType, 
        auto_commit: bool = True
    ) -> ModelType:
        """Partially update an existing record."""
        context = self._log_context("patch", id=str(id))
        
        try:
            db_obj = await self.get_by_id(id)
            obj_data = schema.model_dump(exclude_unset=True, exclude_none=True)

            for field, value in obj_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
                else:
                    raise InvalidFieldException(f"Field '{field}' is invalid for {self.model.__name__}")

            if auto_commit:
                await self.db.commit()
                await self.db.refresh(db_obj)

            app_logger.log_success(
                f"Successfully patched {self.model.__name__}",
                extra=context
            )
            
            return db_obj
            
        except Exception as e:
            app_logger.log_error(
                f"Error patching {self.model.__name__}: {str(e)}",
                error=e,
                extra=context
            )
            await self.db.rollback()
            raise DatabaseError(f"Error patching {self.model.__name__}: {str(e)}")

    async def bulk_create(self, schemas: List[CreateSchemaType]) -> List[ModelType]:
        """Create multiple records in bulk."""
        context = self._log_context("bulk_create")
        
        async with managed_transaction(self.db):
            try:
                db_objs = [self.model(**schema.model_dump()) for schema in schemas]
                self.db.add_all(db_objs)
                await self.db.flush()
                
                app_logger.log_success(
                    f"Successfully bulk created {len(db_objs)} {self.model.__name__} records",
                    extra=context
                )
                
                return db_objs
                
            except Exception as e:
                app_logger.log_error(
                    f"Error bulk creating {self.model.__name__}: {str(e)}",
                    error=e,
                    extra=context
                )
                raise DatabaseError(f"Error bulk creating {self.model.__name__}: {str(e)}")
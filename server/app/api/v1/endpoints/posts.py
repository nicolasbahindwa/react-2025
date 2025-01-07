from fastapi import APIRouter, Depends, HTTPException, status,Request, Query
from uuid import UUID
from app.dependencies import get_post_repository
from app.schemas.post import PostCreate, PostUpdate, PostResponse, PostPatch
from app.repositories.post import PostRepository
from app.exceptions.database import (
    DatabaseError,
    NotFoundException,
    InvalidFieldException,
    InvalidDataException,
    DatabaseCommitException,
    UpdateFailedException
)
from typing import List, Optional
from app.schemas.common import PaginatedResponse
 
from app.models.users import User
 
router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={
        404: {"description": "Not found"},
        400: {"description": "Bad request or database error"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"}
    },
)

@router.get(
    "/",
    response_model=PaginatedResponse[PostResponse],
    summary="Get all posts with pagination and filtering options",
    description="Retrieve a paginated list of posts with optional filtering and ordering."
)
 
async def get_posts(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=100, description="Number of records to return"),
    order_by: Optional[List[str]] = Query(
        default=None,
        description="Order by fields (prefix with - for descending)",
        example=["created_at", "-title"]
    ),
   
    published: Optional[bool] = Query(
        default=None,
        description="Filter by publication status"
    ),
    repo: PostRepository = Depends(get_post_repository),
    # current_user: User = Depends(get_current_user),
   
) -> PaginatedResponse[PostResponse]:
    """
    Get paginated list of posts with optional filtering and ordering.
    
    - Use skip and limit for pagination
    - Use order_by for sorting (prefix field with - for descending order)
    - Use published=true/false to filter by publication status
    """
    
    try:
        filters = {}
        if published is not None:
            filters["published"] = published
            
        return await repo.get_all(
            skip=skip,
            limit=limit,
            order_by=order_by,
            filters=filters
        )
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get(
    "/search/",
    response_model=PaginatedResponse[PostResponse],
    summary="Search posts by any field",
    description="Search posts where any text field matches the query string"
)
async def search_posts(
    q: str = Query(..., min_length=1, description="Search query string"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    repo: PostRepository = Depends(get_post_repository)
) -> PaginatedResponse[PostResponse]:
    """
    Search posts by any field containing the query string.
    Returns paginated results.
    """
    try:
        result = await repo.get_by_any_field(q, skip=skip, limit=limit)
        if result.total == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No posts found matching query: {q}"
            )
        return result
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.post(
    "/",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new post",
    description="Create a new blog post with the provided data"
)
async def create_post(
    post: PostCreate,
    repo: PostRepository = Depends(get_post_repository)
) -> PostResponse:
    """Create a new post with the provided data."""
    try:
        return await repo.create(post)
    except InvalidDataException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get(
    "/{post_id}",
    response_model=PostResponse,
    summary="Get post by ID",
    description="Retrieve a specific post by its UUID"
)
async def get_post(
    post_id: UUID,
    repo: PostRepository = Depends(get_post_repository)
) -> PostResponse:
    """Get a specific post by its ID."""
    try:
        post = await repo.get_by_id(post_id)
        if not post:
            raise NotFoundException("Post", post_id)
        return post
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except DatabaseCommitException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to commit post creation: " + str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.put(
    "/{post_id}",
    response_model=PostResponse,
    summary="Update a post",
    description="Update an existing post by ID"
)
async def update_post(
    post_id: UUID,
    post_update: PostUpdate,
    repo: PostRepository = Depends(get_post_repository)
) -> PostResponse:
    """Update a post."""
    try:
        updated_post = await repo.update(id=post_id, schema=post_update)
        return updated_post
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except InvalidFieldException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except UpdateFailedException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update post: " + str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.patch(
    "/{post_id}",
    response_model=PostResponse,
    summary="Partially update post",
    description="Update specific fields of an existing post"
)
async def patch_post(
    post_id: UUID,
    post_update: PostPatch,
    repo: PostRepository = Depends(get_post_repository)
) -> PostResponse:
    """Partially update an existing post."""
    try:
        return await repo.patch(id=post_id, schema=post_update)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except InvalidFieldException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except UpdateFailedException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update post: " + str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete post",
    description="Delete an existing post by ID"
)
async def delete_post(
    post_id: UUID,
    repo: PostRepository = Depends(get_post_repository)
):
    """Delete a post by ID."""
    try:
        await repo.delete(post_id)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
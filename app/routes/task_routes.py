from fastapi import APIRouter, HTTPException, Request, status
from typing import List
from app.models import TaskCreate, TaskUpdate, TaskResponse
from app.database import db

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(request: Request, task_data: TaskCreate):
    """
    Create a new task for the authenticated user.
    
    The user_id comes from the JWT token (verified by middleware).
    """
    user_id = request.state.user_id
    
    task = db.create_task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description
    )
    
    return TaskResponse(
        id=task["id"],
        title=task["title"],
        description=task["description"],
        completed=task["completed"],
        user_id=task["user_id"],
        created_at=task["created_at"],
        updated_at=task["updated_at"]
    )

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(request: Request):
    """
    Get all tasks for the authenticated user.
    
    Different users see different tasks because the user_id
    is extracted from the token on EVERY request.
    """
    user_id = request.state.user_id
    
    tasks = db.get_user_tasks(user_id)
    
    return [
        TaskResponse(
            id=task["id"],
            title=task["title"],
            description=task["description"],
            completed=task["completed"],
            user_id=task["user_id"],
            created_at=task["created_at"],
            updated_at=task["updated_at"]
        )
        for task in tasks
    ]

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(request: Request, task_id: int):
    """
    Get a specific task if it belongs to the authenticated user.
    """
    user_id = request.state.user_id
    
    task = db.get_task(task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return TaskResponse(
        id=task["id"],
        title=task["title"],
        description=task["description"],
        completed=task["completed"],
        user_id=task["user_id"],
        created_at=task["created_at"],
        updated_at=task["updated_at"]
    )

@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(request: Request, task_id: int, task_data: TaskUpdate):
    """
    Update a task (partial update - PATCH method).
    """
    user_id = request.state.user_id
    
    updates = task_data.dict(exclude_unset=True)
    
    task = db.update_task(task_id, user_id, updates)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return TaskResponse(
        id=task["id"],
        title=task["title"],
        description=task["description"],
        completed=task["completed"],
        user_id=task["user_id"],
        created_at=task["created_at"],
        updated_at=task["updated_at"]
    )

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(request: Request, task_id: int):
    """
    Delete a task.
    
    Returns 204 No Content (no response body) as per HTTP standard.
    """
    user_id = request.state.user_id
    
    deleted = db.delete_task(task_id, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return None
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models import Todo, TodoCreate
from ..auth import get_current_user
from ..database import (
    todos_collection,
    get_user_todos,
    create_user_todo
)
from bson import ObjectId

router = APIRouter()

@router.get("/", response_model=List[Todo])
async def get_todos(current_user = Depends(get_current_user)):
    todos = await get_user_todos(current_user["username"])
    return todos

@router.post("/", response_model=Todo)
async def create_todo(todo: TodoCreate, current_user = Depends(get_current_user)):
    todo_dict = todo.dict()
    return await create_user_todo(current_user["username"], todo_dict)

@router.put("/{todo_id}/toggle", response_model=Todo)
async def toggle_todo(todo_id: str, current_user = Depends(get_current_user)):
    todo = todos_collection.find_one(
        {"_id": ObjectId(todo_id), "username": current_user["username"]}
    )
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    new_status = not todo["completed"]
    todos_collection.update_one(
        {"_id": ObjectId(todo_id)},
        {"$set": {"completed": new_status}}
    )
    return {**todo, "id": str(todo["_id"]), "completed": new_status}

@router.post("/{list_id}", response_model=Todo)
async def create_todo(
    list_id: str, 
    todo: TodoCreate, 
    current_user = Depends(get_current_user)
):
    todo_dict = todo.dict()
    todo_dict["list_id"] = list_id
    return await create_user_todo(current_user["username"], todo_dict)

@router.get("/{list_id}", response_model=List[Todo])
async def get_todos(list_id: str, current_user = Depends(get_current_user)):
    return await get_list_todos(list_id, current_user["username"]) 
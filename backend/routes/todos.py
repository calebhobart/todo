from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models import Todo, TodoCreate
from ..auth import get_current_user
from ..database import todos_collection
from bson import ObjectId

router = APIRouter()

@router.get("/", response_model=List[Todo])
async def get_todos(current_user: User = Depends(get_current_user)):
    todos = todos_collection.find({"username": current_user.username})
    return [{**todo, "id": str(todo["_id"])} for todo in todos]

@router.post("/", response_model=Todo)
async def create_todo(todo: TodoCreate, current_user: User = Depends(get_current_user)):
    todo_dict = todo.dict()
    todo_dict["username"] = current_user.username
    result = todos_collection.insert_one(todo_dict)
    return {**todo_dict, "id": str(result.inserted_id)}

@router.put("/{todo_id}/toggle", response_model=Todo)
async def toggle_todo(todo_id: str, current_user: User = Depends(get_current_user)):
    todo = todos_collection.find_one(
        {"_id": ObjectId(todo_id), "username": current_user.username}
    )
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    new_status = not todo["completed"]
    todos_collection.update_one(
        {"_id": ObjectId(todo_id)},
        {"$set": {"completed": new_status}}
    )
    return {**todo, "id": str(todo["_id"]), "completed": new_status} 
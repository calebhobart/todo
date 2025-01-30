from fastapi import APIRouter, Depends, HTTPException
from typing import List as ListType
from ..models import List, ListCreate
from ..auth import get_current_user
from ..database import create_list, get_user_lists
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=List)
async def create_new_list(list_data: ListCreate, current_user = Depends(get_current_user)):
    return await create_list(current_user["username"], list_data.dict())

@router.get("/", response_model=ListType[List])
async def get_lists(current_user = Depends(get_current_user)):
    return await get_user_lists(current_user["username"]) 
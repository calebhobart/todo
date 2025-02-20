from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class ListBase(BaseModel):
    name: str
    description: Optional[str] = None

class ListCreate(ListBase):
    pass

class List(ListBase):
    id: str
    user_id: str
    created_at: datetime

class TodoBase(BaseModel):
    title: str
    completed: bool = False
    list_id: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class Todo(TodoCreate):
    id: str
    username: str
    created_at: datetime 
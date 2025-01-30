from pymongo import MongoClient
from dotenv import load_dotenv
import os
from .utils import verify_password
from bson import ObjectId
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI'))
db = client['todo_app']
users_collection = db['users']
todos_collection = db['todos']
lists_collection = db['lists']

# Index setup
lists_collection.create_index([("user_id", 1)])
todos_collection.create_index([("list_id", 1)])
todos_collection.create_index([("user_id", 1)])

# List operations
async def create_list(user_id: str, list_data: dict):
    list_data["user_id"] = user_id
    list_data["created_at"] = datetime.utcnow()
    result = lists_collection.insert_one(list_data)
    return {**list_data, "id": str(result.inserted_id)}

async def get_user_lists(user_id: str):
    cursor = lists_collection.find({"user_id": user_id})
    return [{**list_doc, "id": str(list_doc["_id"])} for list_doc in cursor]

async def create_list(user_id: str, list_data: dict):
    list_data["user_id"] = user_id
    list_data["created_at"] = datetime.utcnow()
    result = lists_collection.insert_one(list_data)
    return {**list_data, "id": str(result.inserted_id)}

async def get_user_lists(user_id: str):
    cursor = lists_collection.find({"user_id": user_id})
    return [{**list_doc, "id": str(list_doc["_id"])} for list_doc in cursor]

# Todo operations
async def create_todo(user_id: str, list_id: str, todo_data: dict):
    todo_data["user_id"] = user_id
    todo_data["list_id"] = list_id
    todo_data["created_at"] = datetime.utcnow()
    result = todos_collection.insert_one(todo_data)
    return {**todo_data, "id": str(result.inserted_id)}

async def get_list_todos(list_id: str, user_id: str):
    cursor = todos_collection.find({
        "list_id": list_id,
        "user_id": user_id
    })
    return [{**todo, "id": str(todo["_id"])} for todo in cursor]

# Database helper functions
async def get_user(username: str):
    return users_collection.find_one({"username": username})

async def get_user_todos(username: str):
    cursor = todos_collection.find({"username": username})
    return [{**todo, "id": str(todo["_id"])} for todo in cursor]

async def create_user_todo(username: str, todo_data: dict):
    todo_data["username"] = username
    result = todos_collection.insert_one(todo_data)
    return {**todo_data, "id": str(result.inserted_id)}

async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user
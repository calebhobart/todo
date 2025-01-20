import streamlit as st
import pymongo
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize MongoDB connection
client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = client['todo_app']
users_collection = db['users']
todos_collection = db['todos']

def load_todos():
    """Load todos from MongoDB for the current user"""
    user_todos = todos_collection.find_one({'username': st.session_state.username})
    if user_todos:
        return user_todos.get('todos', []), user_todos.get('completed', [])
    return [], []

def save_todos():
    """Save todos to MongoDB for the current user"""
    todos_collection.update_one(
        {'username': st.session_state.username},
        {
            '$set': {
                'todos': st.session_state.todos,
                'completed': st.session_state.completed
            }
        },
        upsert=True
    ) 
# Streamlit Todo App

A simple todo application built with Streamlit featuring user authentication and MongoDB storage.

## Features
- User authentication and login system
- Individual todo lists for each user
- Add todo items
- Mark items as complete/incomplete 
- Persistent storage in MongoDB
- Clean and simple interface
- Secure password hashing
- Session management with cookies

## Setup
1. Clone this repository
2. Install requirements: `pip install -r requirements.txt`
3. Create a `.env` file with your MongoDB connection string:
   ```
   MONGODB_URI=your_mongodb_connection_string
   ```
4. Configure users in `config.yaml`:
   ```yaml
   credentials:
     usernames:
       username:
         email: user@email.com
         password: hashed_password
         roles:
           - viewer
   ```
5. Run the app: `streamlit run todo.py`

## Authentication
- Users must log in to access their todo lists
- Passwords are securely hashed
- Session cookies maintain login state
- User configuration stored in config.yaml

## Storage
- Todo items stored in MongoDB
- Each user has their own todo list
- Changes persist between sessions

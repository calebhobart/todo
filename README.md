# Streamlit Todo App

A feature-rich todo application built with Streamlit featuring user authentication and MongoDB storage.

## Features
- Quick access todo list for non-authenticated users
- User authentication and registration system
- Individual todo lists for each user
- Add todo items
- Mark items as complete/incomplete 
- Persistent storage in MongoDB
- Clean and simple interface
- Secure password hashing
- Session management with cookies

## Project Structure
```
your_project/
├── app.py           # Main Streamlit app
├── auth.py          # Authentication related code
├── database.py      # MongoDB functions
├── components.py    # UI components like show_todo_list
├── config.yaml      # Configuration file
└── utils.py         # Utility functions
```

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
   cookie:
     expiry_days: 30
     key: your_key_here
     name: cookie
   ```
5. Run the app: `streamlit run app.py`

## Usage
1. **Quick Todo List**
   - Available immediately without login
   - Changes persist during session
   - Perfect for quick tasks

2. **User Account**
   - Sign up with email and password
   - Secure authentication
   - Persistent todo storage

3. **Todo Management**
   - Add new todos
   - Mark todos as complete/incomplete
   - See completed items with strikethrough

## Authentication
- Users must log in to access their saved todo lists
- Passwords are securely hashed
- Session cookies maintain login state
- User configuration stored in config.yaml

## Storage
- Todo items stored in MongoDB
- Each user has their own todo list
- Changes persist between sessions
- Default todos stored in session state

## Development
Built with:
- Streamlit
- MongoDB
- Python-dotenv
- PyYAML
- Streamlit-Authenticator

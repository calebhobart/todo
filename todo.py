import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pymongo
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize MongoDB connection
client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = client['todo_app']
users_collection = db['users']
todos_collection = db['todos']

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

# Authenticate users
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Initialize authentication status at the top of your script, after imports
if 'authentication_status' not in st.session_state:
    st.session_state.authentication_status = None

# Initialize default todos
if 'default_todos' not in st.session_state:
    st.session_state.default_todos = []
    st.session_state.default_completed = []

# Initialize user details at the top of your script
if 'name' not in st.session_state:
    st.session_state.name = None
if 'username' not in st.session_state:
    st.session_state.username = None

# After your imports and before authentication, initialize default session state
if 'default_todos' not in st.session_state:
    st.session_state.default_todos = []
    st.session_state.default_completed = []

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

# After the tabs but before authentication checks
def show_todo_list(todos_list=None, completed_list=None, save_function=None):
    """Reusable function to show todo list"""
    # Create a unique form key based on whether it's the default or authenticated list
    form_key = "default_todo_form" if save_function is None else "auth_todo_form"
    
    with st.form(key=form_key):
        todo_input = st.text_input("Enter a todo item:")
        submit_button = st.form_submit_button("Add Todo")
        
        if submit_button and todo_input:
            todos_list.append(todo_input)
            completed_list.append(False)
            if save_function:
                save_function()

    for i, todo in enumerate(todos_list):
        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            checked = st.checkbox(
                f"Complete todo item {i+1}",
                key=f"todo_{i}_{id(todos_list)}", # unique key for each list
                value=completed_list[i],
                on_change=lambda i=i: handle_checkbox_change(i, todos_list, completed_list, save_function),
                label_visibility="collapsed"
            )
        with col2:
            if completed_list[i]:
                st.markdown(f"~~{todo}~~")
            else:
                st.write(todo)

def handle_checkbox_change(index, todos_list, completed_list, save_function=None):
    completed_list[index] = not completed_list[index]
    if save_function:
        save_function()

def save_config(config):
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

# Add signup tab before authentication code
if not st.session_state.authentication_status:
    # Show tabs for login/signup with Todo List as default (index=0)
    default_list_tab, signup_tab, login_tab = st.tabs(["Todo List", "Sign Up", "Login"])
    
    with default_list_tab:
        st.write("### Quick Todo List")
        st.write("Note: Sign up or log in to save your todos!")
        show_todo_list(
            st.session_state.default_todos,
            st.session_state.default_completed
        )
    
    with signup_tab:
        st.subheader("Create an Account")
        with st.form("signup_form"):
            new_username = st.text_input("Username*")
            new_name = st.text_input("Full Name*")
            new_email = st.text_input("Email*")
            new_password = st.text_input("Password*", type="password")
            new_password_confirm = st.text_input("Confirm Password*", type="password")
            
            signup_button = st.form_submit_button("Sign Up")
            
            if signup_button:
                if not (new_username and new_name and new_email and new_password):
                    st.error("Please fill out all fields")
                elif new_password != new_password_confirm:
                    st.error("Passwords do not match")
                elif new_username in config['credentials']['usernames']:
                    st.error("Username already exists")
                else:
                    # Hash the password
                    hashed_password = stauth.Hasher([new_password]).generate()[0]
                    
                    # Add new user to config
                    config['credentials']['usernames'][new_username] = {
                        'email': new_email,
                        'name': new_name,
                        'password': hashed_password
                    }
                    
                    # Save updated config
                    save_config(config)
                    
                    st.success("Account created successfully! Please log in.")

    with login_tab:
        authenticator.login()
            # name = st.session_state['name']
            # authentication_status = st.session_state['authentication_status']
            # username = st.session_state['username']

        if st.session_state.authentication_status is False:
            st.error('Username/password is incorrect')
        elif st.session_state.authentication_status is None:
            st.warning('Please enter your username and password')
else:
    # User is logged in
    authenticator.logout('Logout', 'sidebar')
    st.write(f'Welcome *{st.session_state.name}*')
    
    # Initialize authenticated user's todos
    if 'todos' not in st.session_state:
        todos, completed = load_todos()
        st.session_state.todos = todos
        st.session_state.completed = completed
    
    show_todo_list(
        st.session_state.todos, 
        st.session_state.completed,
        save_todos
    )

with open('config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)

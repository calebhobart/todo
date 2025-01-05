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

try:
    authenticator.login()
except Exception as e:
    st.error(e)

# if st.session_state['authentication_status']:
#     authenticator.logout()
#     st.write(f'Welcome *{st.session_state["name"]}*')
#     st.title('Some content')
# elif st.session_state['authentication_status'] is False:
#     st.error('Username/password is incorrect')
# elif st.session_state['authentication_status'] is None:
#     st.warning('Please enter your username and password')

if st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')
else:
    # User is logged in
    authenticator.logout('Logout', 'sidebar')
    st.write(f'Welcome *{st.session_state["name"]}*')

    # Load todos for current user
    def load_todos():
        user_todos = todos_collection.find_one({'username': st.session_state["name"]})
        if user_todos:
            return user_todos.get('todos', []), user_todos.get('completed', [])
        return [], []

    def save_todos():
        todos_collection.update_one(
            {'username': st.session_state["name"]},
            {
                '$set': {
                    'todos': st.session_state.todos,
                    'completed': st.session_state.completed
                }
            },
            upsert=True
        )

    # Initialize session state
    if 'todos' not in st.session_state:
        todos, completed = load_todos()
        st.session_state.todos = todos
        st.session_state.completed = completed

    # Todo input form
    with st.form(key="todo_form"):
        todo_input = st.text_input("Enter a todo item:")
        submit_button = st.form_submit_button("Add Todo")
        
        if submit_button and todo_input:
            st.session_state.todos.append(todo_input)
            st.session_state.completed.append(False)
            save_todos()

    # Create a callback function to handle checkbox changes
    def handle_checkbox_change(index):
        st.session_state.completed[index] = not st.session_state.completed[index]
        save_todos()

    # Display todos
    for i, todo in enumerate(st.session_state.todos):
        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            st.checkbox(
                f"Complete todo item {i+1}",
                key=f"todo_{i}", 
                value=st.session_state.completed[i],
                on_change=handle_checkbox_change,
                args=(i,),
                label_visibility="collapsed"
            )
        with col2:
            if st.session_state.completed[i]:
                st.markdown(f"~~{todo}~~")
            else:
                st.write(todo)

    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

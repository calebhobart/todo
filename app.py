import streamlit as st
from auth import init_auth, save_config
from database import load_todos, save_todos
from components import show_todo_list
import streamlit_authenticator as stauth

# Initialize session state
if 'authentication_status' not in st.session_state:
    st.session_state.authentication_status = None
if 'name' not in st.session_state:
    st.session_state.name = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'default_todos' not in st.session_state:
    st.session_state.default_todos = []
    st.session_state.default_completed = []

# Initialize authentication
authenticator, config = init_auth()

# Main app logic
if not st.session_state.authentication_status:
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
        
        if st.session_state.authentication_status is False:
            st.error('Username/password is incorrect')
        elif st.session_state.authentication_status is None:
            st.warning('Please enter your username and password')

else:
    authenticator.logout('Logout', 'sidebar')
    st.write(f'Welcome *{st.session_state.name}*')
    
    if 'todos' not in st.session_state:
        todos, completed = load_todos()
        st.session_state.todos = todos
        st.session_state.completed = completed
    
    show_todo_list(
        st.session_state.todos, 
        st.session_state.completed,
        save_todos
    ) 
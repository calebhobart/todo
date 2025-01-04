import streamlit as st
from streamlit_extras.stodo import to_do
import json
import os

def save_todos():
    """Save todos and their states to a JSON file"""
    data = {
        'todos': st.session_state.todos,
        'completed': st.session_state.completed
    }
    with open('todos.json', 'w') as f:
        json.dump(data, f)

def load_todos():
    """Load todos and their states from JSON file"""
    if os.path.exists('todos.json'):
        with open('todos.json', 'r') as f:
            data = json.load(f)
            return data.get('todos', []), data.get('completed', [])
    return [], []

st.title("Todo App")

st.write("This is a simple todo app built with Streamlit.")

st.write("Write your todo items in the box below and click on the 'Add' button to add them to the list.")
# Create a form for the todo input
with st.form(key="todo_form"):
    todo_input = st.text_input("Enter a todo item:")
    submit_button = st.form_submit_button("Add Todo")
    
    if submit_button and todo_input:  # Only add if there's text entered
        st.session_state.todos.append(todo_input)
        st.session_state.completed.append(False)  # Initialize as not completed
        save_todos()  # Save after adding new todo

# Initialize todo list in session state if it doesn't exist
if 'todos' not in st.session_state:
    # Load saved todos when initializing
    todos, completed = load_todos()
    st.session_state.todos = todos
    st.session_state.completed = completed

# Create a callback function to handle checkbox changes
def handle_checkbox_change(index):
    st.session_state.completed[index] = not st.session_state.completed[index]
    save_todos()  # Save after updating completion status

# Display all todos with checkboxes
for i, todo in enumerate(st.session_state.todos):
    col1, col2 = st.columns([0.1, 0.9])  # Create two columns for better layout
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

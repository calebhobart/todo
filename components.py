import streamlit as st

def show_todo_list(todos_list=None, completed_list=None, save_function=None):
    """Reusable function to show todo list"""
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
            st.checkbox(
                f"Complete todo item {i+1}",
                key=f"todo_{i}_{id(todos_list)}",
                value=completed_list[i],
                on_change=handle_checkbox_change,
                args=(i, todos_list, completed_list, save_function),
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
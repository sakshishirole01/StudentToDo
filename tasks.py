from dash import Output, Input, State, ctx, html, dcc
import json
from data_handler import load_data, save_data
from subjects import subject_page  # Import subject page layout
from home import home_layout

# ✅ Update Navbar when subjects are added
def update_navbar(n_clicks, subject_name):
    todo_data = load_data()
    if subject_name and subject_name not in todo_data:
        todo_data[subject_name] = []
        save_data(todo_data)

    return [
        html.Button(subject, id={"type": "subject-btn", "index": subject}, n_clicks=0, className="navbar-button",
                                style={
                                    "display": "block",
                                    "width": "90%",
                                    "margin": "5px auto",
                                    "padding": "10px",
                                    "border": "1px solid #ccc",
                                    "background-color": "#B0E0E6",  # Light blue
                                    "text-align": "left",
                                    "cursor": "pointer"
                                })
                    for subject in todo_data
    ]

# ✅ Navigate to subject page when a subject button is clicked
def navigate_to_subject(n_clicks):
    triggered_id = ctx.triggered_id  # Get ID of the clicked button
    if not triggered_id or triggered_id["index"] is None:
        return "/"

    selected_subject = triggered_id["index"]
    return f"/subject/{selected_subject}"  # Redirect to subject page URL

# ✅ Callback to update the main content based on URL
def update_page(pathname):
    if pathname.startswith("/subject/"):
        subject_name = pathname.split("/")[-1]
        return subject_page(subject_name)  # Load the subject page layout
    return home_layout()  # Default home page if no subject is selected

# ✅ Add task to the selected subject
def add_task(n_clicks, task_name, pathname):
    subject_name = pathname.split("/")[-1]
    todo_data = load_data()
    if task_name and subject_name in todo_data:
        todo_data[subject_name].append(task_name)
        save_data(todo_data)
    return [html.Li(task) for task in todo_data.get(subject_name, [])]

# ✅ Handle "Back to Home" Button Click
def go_home(n_clicks):
    return "/"


from dash import Dash, html, dcc, Input, Output, State, ctx, ALL
import json

import dash
from data_handler import load_data, load_subject_tasks, save_subject_tasks
from home import home_layout
from tasks import add_task, navigate_to_subject, update_navbar, update_page, go_home

# Initialize the Dash app
app = Dash(__name__, suppress_callback_exceptions=True)

valid_paths = {"/"}  # Start with home as a valid path
subjects = load_data()  # Load subject names
valid_paths.update({f"/subject/{subject}" for subject in subjects})  # Add subject paths


# Load subject names for the navbar
subjects = load_data()

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),  # URL handling
    html.Div(id="page-content", children=update_page("/"))  # Default to home page
])


# ✅ Callback to update the page content based on the URL
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    prevent_initial_call=True  # Prevent running on initial load
)
def display_page(pathname):
    if pathname is None or pathname not in valid_paths:  # Ensure a valid path
        return update_page("/")  # Redirect to home
    return update_page(pathname)


# ✅ Callback to update the navbar when a new subject is added
@app.callback(
    Output("navbar", "children"),
    Input("add-subject-btn", "n_clicks"),
    State("subject-input", "value"),
    prevent_initial_call=True
)
def update_nav(n_clicks, subject_name):
    return update_navbar(n_clicks, subject_name)

@app.callback(
    Output("url", "pathname"),
    [
        Input({"type": "subject-btn", "index": ALL}, "n_clicks"),
        Input("back-home-btn", "n_clicks")
    ],
    prevent_initial_call=True
)
def route_or_home(n_clicks_subjects, n_clicks_home):
    triggered_id = ctx.triggered_id  # Get which button was clicked

    if triggered_id == "back-home-btn":
        return go_home(n_clicks_home)  # Redirect to home

    # Check if any subject button was clicked
    if isinstance(n_clicks_subjects, list):
        for i, clicks in enumerate(n_clicks_subjects):
            if clicks:  # If button was clicked
                return navigate_to_subject(n_clicks_subjects)

    return dash.no_update  # No button was clicked, do nothing



# # ✅ Callback to update the URL when a subject is clicked
# @app.callback(
#     Output("url", "pathname"),
#     Input({"type": "subject-btn", "index": ALL}, "n_clicks"),
#     prevent_initial_call=True
# )
# def route_to_subject(n_clicks):
#     return navigate_to_subject(n_clicks)

# ✅ Callback to add tasks to a subject
@app.callback(
    Output("task-list", "children"),
    Input("add-task-btn", "n_clicks"),
    State("task-name-input", "value"),
    State("url", "pathname"),
    prevent_initial_call=True
)
def add_new_task(n_clicks, task_name, pathname):
    return add_task(n_clicks, task_name, pathname)

# # ✅ Callback to navigate back to the home page
# @app.callback(
#     Output("url", "pathname"),
#     Input("back-home-btn", "n_clicks"),
#     prevent_initial_call=True
# )
# def back_to_home(n_clicks):
#     return go_home(n_clicks)


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_hot_reload=False)

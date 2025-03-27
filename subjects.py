from dash import html, dcc, Input, Output, State, callback, ALL, ctx
import json

import dash
from data_handler import load_data, load_subject_tasks, save_subject_tasks  # Ensure these handle JSON properly


def subject_page(subject_name):
    # Load subject data
    todo_data = load_data()  # Loads all subjects for navbar
    tasks = load_subject_tasks(subject_name)  # Load tasks for the selected subject
    ongoing_tasks = tasks.get("ongoing", [])
    completed_tasks = tasks.get("completed", [])

    return html.Div(id = "page-container", children=[
        # Heading (Full Width)
        html.Div([
            html.H1(f"Subject: {subject_name}", style={
                "text-align": "center",
                "padding": "20px",
                "background": "#87CEFA",  # Light blue background
                "border-bottom": "2px solid #ccc"
            })
        ], style={"width": "100%"}),

        # Flexbox container for Navbar + Subject Content
        html.Div(style={"display": "flex"}, children=[  
            # Navbar on the Left
            html.Div([
                html.H3("Subjects", style={
                    "text-align": "center",
                    "padding": "10px",
                    "border-bottom": "2px solid #ccc",
                    "background": "#4682B4",
                    "color": "white"
                }),
                html.Div(id="navbar", children=[
                    html.Button(subject, id={"type": "subject-btn", "index": subject}, n_clicks=0, className="navbar-button",
                                style={
                                    "display": "block",
                                    "width": "90%",
                                    "margin": "5px auto",
                                    "padding": "10px",
                                    "border": "1px solid #ccc",
                                    "background-color": "#B0E0E6",
                                    "text-align": "left",
                                    "cursor": "pointer"
                                })
                    for subject in todo_data
                ])
            ], style={
                "width": "250px",
                "border-right": "2px solid #ccc",
                "background": "#f0f8ff",
                "padding": "10px"
            }),

            # Subject Content on the Right
            html.Div([
                html.H2(f"Tasks for {subject_name}", style={"text-align": "center"}),

                # Task input area
                html.Label("Enter a new task:"),
                dcc.Input(id="task-input", type="text", placeholder="New task"),
                html.Button("Add Task", id="add-task-btn", n_clicks=0),
                html.Br(),

                # **Two Lists Side-by-Side (with Drag-and-Drop)**
                html.Div(style={"display": "flex", "justify-content": "space-between"}, children=[

                    # **Ongoing Tasks**
                    html.Div([
                        html.H3("Ongoing Tasks", style={"text-align": "center"}),

                        html.Ul(id="ongoing-tasks", children=[
                            html.Li(
                                html.Button(
                                    task,  
                                    id={"type": "task", "index": task},  
                                    n_clicks=0,  # Track clicks
                                    style={
                                        "cursor": "pointer",
                                        "border": "2px solid #333",  # Dark border
                                        "background": "#f9f9f3",  # Light gray background
                                        "text-align": "left",
                                        "font-size": "16px",
                                        "color": "#333",
                                        "padding": "10px",
                                        "width": "100%",  # Ensures same width
                                        "display": "block",
                                        "transition": "all 0.2s ease-in-out"  # Smooth transition for hover effect
                                    },
                                    className="task-button"
                                ),
                                style={
                                    "list-style-type": "none",  # No bullet points
                                    "margin-bottom": "8px",
                                }
                            ) for task in ongoing_tasks
                        ], style={
                            "padding": "10px",
                            "border": "1px solid #FFEFD5",
                            "min-height": "150px",
                            "background": "#FFEFD5",
                            "width": "75%",
                            "display": "block"
                        })

                    ], style={"width": "48%", "border": "2px solid #333", "padding": "10px"}),

                    # **Completed Tasks**
                    html.Div([
                        html.H3("Completed Tasks", style={"text-align": "center"}),

                        html.Ul(id="completed-tasks", children=[
                            html.Li(
                                html.Button(
                                    task,  
                                    id={"type": "completed-task", "index": task},  
                                    n_clicks=0,  # Track clicks
                                    style={
                                        "cursor": "pointer",
                                        "border": "2px solid #2e8b57",  # Dark green border
                                        "background": "#E6FFE6",  # Light green background
                                        "text-align": "left",
                                        "font-size": "16px",
                                        "color": "#2e8b57",  # Dark green text
                                        "padding": "10px",
                                        "width": "100%",  # Ensures same width
                                        "display": "block",
                                        "transition": "all 0.2s ease-in-out"  # Smooth transition for hover effect
                                    },
                                    className="completed-task-button"
                                ),
                                style={
                                    "list-style-type": "none",  # No bullet points
                                    "margin-bottom": "8px",
                                }
                            ) for task in completed_tasks
                        ], style={
                            "padding": "10px",
                            "border": "1px solid #2e8b57",
                            "min-height": "150px",
                            "background": "#D0F0C0",
                            "width": "75%",
                            "display": "block"
                        })

                    ], style={"width": "48%", "border": "2px solid #2e8b57", "padding": "10px"})

                ]),

                html.Br(),
                html.Button("Back to Home", id="back-home-btn"),

                # Hidden Modal Popup (Initially Hidden)
                html.Div(id="task-popup", style={"display": "none"}, children=[
                    html.Div([
                        html.H3("Task Options"),
                        html.P(id="selected-task-name"),
                        html.Button("Task Completed", id="complete-task-btn"),
                        html.Button("Delete Task", id="delete-task-btn"),
                        html.Button("Close", id="close-popup-btn")
                    ], style={
                        "position": "fixed", "top": "50%", "left": "50%", "transform": "translate(-50%, -50%)",
                        "background": "white", "padding": "20px", "border": "2px solid black"
                    })
                ]),

                # Hidden Completed Task Popup (Initially Hidden)
                html.Div(id="completed-task-popup", style={"display": "none"}, children=[
                    html.Div([
                        html.H3("Completed Task Options"),
                        html.P(id="selected-completed-task-name"),
                        html.Button("Task Ongoing", id="ongoing-task-btn"),
                        html.Button("Remove Task", id="remove-task-btn"),
                        html.Button("Close", id="close-completed-popup-btn")
                    ], id= "popup-content",  )
                ]),

                # Store selected completed task
                dcc.Store(id="selected-completed-task", data=""),
                dcc.Store(id="mouse-position", data={}),

                # Store clicked task
                dcc.Store(id="selected-task", data=""),
                dcc.Store(id="task-store", data={"ongoing": ongoing_tasks, "completed": completed_tasks})

            ], style={
                "flex-grow": "1",
                "padding": "20px"
            })

        ])
    ])

# ------------------ CALLBACKS ------------------
from dash import Output, Input, State, ctx, html, dcc, callback
import json
import os
from data_handler import load_data, save_subject_tasks  # ✅ Correct import

# ✅ Callback to handle adding a new task
@callback(
    Output("task-store", "data"),  # Update task storage
    Input("add-task-btn", "n_clicks"),  # Trigger on button click
    State("task-input", "value"),  # Get task input
    State("task-store", "data"),  # Get current task data
    State("url", "pathname"),  # Extract subject name
    prevent_initial_call=True
)
def add_task(n_clicks, task_text, task_data, pathname):
    if not task_text:
        raise PreventUpdate  # No input, no update

    subject_name = pathname.split("/")[-1]  # Extract subject name
    task_data["ongoing"].append(task_text)  # Append task to list
    save_subject_tasks(subject_name, task_data)  # Save to file

    return task_data  # Updated tasks will trigger UI refresh elsewhere

@callback(
    Output("ongoing-tasks", "children"),
    Input("task-store", "data"),
)
def update_task_list(task_data):
    return [
        html.Li(
            html.Button(
                task,  
                id={"type": "task", "index": task},  
                n_clicks=0,  # Track clicks
                style={
                    "cursor": "pointer",
                    "border": "2px solid #333",  # Dark border
                    "background": "#f9f9f3",  # Light gray background
                    "text-align": "left",
                    "font-size": "16px",
                    "color": "#333",
                    "padding": "10px",
                    "width": "100%",  # Ensures same width
                    "display": "block",
                    "transition": "all 0.2s ease-in-out"  # Smooth transition for hover effect
                },
                className="task-button"
            ),
            style={
                "list-style-type": "none",  # No bullet points
                "margin-bottom": "8px",
            }
        ) for task in task_data["ongoing"]
    ]

from dash.exceptions import PreventUpdate
import dash
from dash import Output, Input, State, ctx, html, callback, MATCH, ALL
from dash.exceptions import PreventUpdate


# ✅ Callback to show the popup only when a task is clicked
@callback(
    Output("task-popup", "style", allow_duplicate=True),  
    Output("selected-task", "data"),  
    Output("selected-task-name", "children"),  
    Input({"type": "task", "index": ALL}, "n_clicks"),  # ✅ Task button clicks
    State({"type": "task", "index": ALL}, "id"),  
    prevent_initial_call=True
)
def show_task_popup(n_clicks, task_ids):
    if not n_clicks or all(click == 0 or click is None for click in n_clicks):
        raise PreventUpdate  # ✅ No valid click, do nothing

    # ✅ Find which task button was clicked
    triggered = ctx.triggered_id
    if isinstance(triggered, dict) and "index" in triggered:
        selected_task = triggered["index"]
        return {"display": "block"}, selected_task, f"Selected Task: {selected_task}"

    raise PreventUpdate  # ✅ Prevent unnecessary updates

# ✅ Close popup when "Close" button is clicked
@callback(
    Output("task-popup", "style", allow_duplicate=True),
    Input("close-popup-btn", "n_clicks"),
    prevent_initial_call=True
)
def hide_popup(n_clicks):
    if n_clicks:
        return {"display": "none"}  # ✅ Hide the popup
    raise PreventUpdate  # ✅ Prevent unnecessary updates

@callback(
    Output("url", "pathname", allow_duplicate=True),  # This will trigger a page reload
    Output("task-popup", "style", allow_duplicate=True),  
    Input("complete-task-btn", "n_clicks"),  
    Input("delete-task-btn", "n_clicks"),  
    State("selected-task", "data"),  
    State("task-store", "data"),  
    State("url", "pathname"),  
    prevent_initial_call=True
)
def handle_task_action(complete_clicks, delete_clicks, selected_task, task_data, pathname):
    if not selected_task:
        raise PreventUpdate  # No task selected, do nothing

    subject_name = pathname.split("/")[-1]  

    # ✅ Update tasks based on button clicked
    if ctx.triggered_id == "complete-task-btn" and selected_task in task_data["ongoing"]:
        task_data["ongoing"].remove(selected_task)
        task_data["completed"].append(selected_task)

    elif ctx.triggered_id == "delete-task-btn" and selected_task in task_data["ongoing"]:
        task_data["ongoing"].remove(selected_task)

    # ✅ Save updated task list
    save_subject_tasks(subject_name, task_data)

    # ✅ Refresh the page by updating the URL (forces subject_page to be called again)
    return f"/subject/{subject_name}", {"display": "none"}  # Hide popup after action


# ------------------------

# Completed
# 
# ✅ Callback to show popup for completed tasks
@callback(
    Output("completed-task-popup", "style", allow_duplicate=True),  
    Output("selected-completed-task", "data"),  
    Output("selected-completed-task-name", "children"),  
    Input({"type": "completed-task", "index": ALL}, "n_clicks"),  
    State({"type": "completed-task", "index": ALL}, "id"),  
    prevent_initial_call=True
)
def show_completed_task_popup(n_clicks, task_ids):
    if not n_clicks or all(click == 0 or click is None for click in n_clicks):
        raise PreventUpdate  

    # ✅ Find which task was clicked
    triggered = ctx.triggered_id
    if isinstance(triggered, dict) and "index" in triggered:
        selected_task = triggered["index"]

        # ✅ Position popup on the right side of the screen
        popup_style = {
            "display": "block",
            "position": "fixed",
            "top": "50%",  # Center vertically
            "right": "10px",  # Align to the right side
            "transform": "translateY(-50%)",  # Center vertically
            "width": "300px",  # Same size as ongoing task popup
            "background": "white",
            "padding": "20px",
            "border": "2px solid black",
            "z-index": "1000",  
            "box-shadow": "2px 2px 10px rgba(0,0,0,0.3)"
        }


        return popup_style, selected_task, f"Selected Task: {selected_task}"

    raise PreventUpdate  


# ✅ Close popup when "Close" button is clicked
@callback(
    Output("completed-task-popup", "style", allow_duplicate=True),
    Input("close-completed-popup-btn", "n_clicks"),
    prevent_initial_call=True
)
def hide_completed_popup(n_clicks):
    if n_clicks:
        return {"display": "none"}  # ✅ Hide popup
    raise PreventUpdate  


# ✅ Handle completed task actions (Move back to Ongoing or Remove)
@callback(
    Output("url", "pathname", allow_duplicate=True),  
    Output("completed-task-popup", "style", allow_duplicate=True),  
    Input("ongoing-task-btn", "n_clicks"),  
    Input("remove-task-btn", "n_clicks"),  
    State("selected-completed-task", "data"),  
    State("task-store", "data"),  
    State("url", "pathname"),  
    prevent_initial_call=True
)
def handle_completed_task_action(ongoing_clicks, remove_clicks, selected_task, task_data, pathname):
    if not selected_task:
        raise PreventUpdate  

    subject_name = pathname.split("/")[-1]  

    # ✅ Move back to Ongoing
    if ctx.triggered_id == "ongoing-task-btn" and selected_task in task_data["completed"]:
        task_data["completed"].remove(selected_task)
        task_data["ongoing"].append(selected_task)

    # ✅ Remove Task
    elif ctx.triggered_id == "remove-task-btn" and selected_task in task_data["completed"]:
        task_data["completed"].remove(selected_task)

    # ✅ Save updates
    save_subject_tasks(subject_name, task_data)

    return f"/subject/{subject_name}", {"display": "none"}  # Hide popup after action

from dash import html, dcc
from data_handler import load_data, save_data

def home_layout(selected_subject=None):
    todo_data = load_data()

    return html.Div(children=[
        # Heading
        html.Div([
            html.H1("Welcome to your To-Do List!", style={
                "text-align": "center",
                "padding": "20px",
                "background": "#87CEFA",
                "border-bottom": "2px solid #ccc"
            })
        ], style={"width": "100%"}),

        # Flexbox container for Navbar + Main Content
        html.Div(style={"display": "flex"}, children=[  
            # Sidebar (Subjects)
            html.Div([
                html.H3("Subjects", style={
                    "text-align": "center",
                    "padding": "10px",
                    "border-bottom": "2px solid #ccc",
                    "background": "#4682B4",
                    "color": "white"
                }),
                html.Div(id="navbar", children=[
                html.Div([
                    html.Button(subject,  
                        id={"type": "subject-btn", "index": subject},  
                        n_clicks=0,  
                        className="navbar-button",
                        style={
                            "display": "inline-block",
                            "width": "80%",
                            "margin": "5px 0",
                            "padding": "8px",
                            "border": "1px solid #ccc",
                            "background-color": "#B0E0E6",
                            "text-align": "left",
                            "cursor": "pointer"
                        }
                    ),
                    html.Button("❌",  
                        id={"type": "delete-subject-btn", "index": subject},  
                        n_clicks=0,  
                        className="delete-button",
                        style={
                            "display": "inline-block",
                            "margin-left": "5px",
                            "padding": "5px",
                            "border": "none",
                            "background": "red",
                            "color": "white",
                            "cursor": "pointer",
                            "font-size": "14px"
                        }
                    )
                ], style={"display": "flex", "align-items": "center"})
                for subject in todo_data
            ])

            ], style={
                "width": "250px",
                "border-right": "2px solid #ccc",
                "background": "#f0f8ff",
                "padding": "10px"
            }),

           # Subject Popup (Appears when clicking ❌)
            html.Div(id="subject-popup", style={"display": "none"}, children=[
                html.Div([
                    html.P(id="popup-subject-name", style={"font-weight": "bold"}),
                    html.Button("Delete Subject", id="delete-subject-btn",  style={"margin-right": "10px"}),
                    html.Button("Close", id="close-popup-btn"),
                ], style={
                    "position": "fixed",
                    "top": "50%",
                    "left": "20%",
                    "transform": "translate(-50%, -50%)",
                    "width": "300px",
                    "background": "white",
                    "padding": "15px",
                    "border": "2px solid black",
                    "box-shadow": "2px 2px 10px rgba(0,0,0,0.3)",
                    "z-index": "1000"
                })
            ]),

            # Main Content
            html.Div([
                html.Label("Enter subjects for this semester:"),
                dcc.Input(id="subject-input", type="text", placeholder="Subject Name"),
                html.Button("Add Subject", id="add-subject-btn", n_clicks=0),
                dcc.Store(id="selected-subject"),  
                html.Br(),
                html.Br(),
                html.Button("Back to Home", id="back-home-btn"),
            ], style={
                "flex-grow": "1",
                "padding": "20px"
            })
        ]),

    ])


from dash import Input, Output, State, callback, ctx, ALL
from dash.exceptions import PreventUpdate
import json
import dash

@callback(
    Output("subject-popup", "style", allow_duplicate=True),
    Output("popup-subject-name", "children", allow_duplicate=True),
    Input({"type": "delete-subject-btn", "index": ALL}, "n_clicks"),
    State({"type": "delete-subject-btn", "index": ALL}, "id"),
    prevent_initial_call=True
)
def show_subject_popup(n_clicks, button_ids):
    ctx = dash.ctx
    if not ctx.triggered:
        raise PreventUpdate

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    subject_name = json.loads(button_id)["index"]

    popup_style = {
        "display": "block",
        "position": "fixed",
        "top": "50%",
        "left": "50%",
        "transform": "translate(-50%, -50%)",
        "background": "white",
        "padding": "15px",
        "border": "2px solid black",
        "z-index": "1000",
        "box-shadow": "2px 2px 10px rgba(0,0,0,0.3)"
    }

    return popup_style, f"Subject: {subject_name}"

@callback(
    Output("subject-popup", "style"),
    Input("close-popup-btn", "n_clicks"),
    prevent_initial_call=True
)
def close_subject_popup(n_clicks):
    return {"display": "none"}


@callback(
    Output("navbar", "children", allow_duplicate=True),
    Output("subject-popup", "style", allow_duplicate=True),
    Input("delete-subject-btn", "n_clicks"),
    State("popup-subject-name", "children"),
    prevent_initial_call=True
)
def delete_subject(n_clicks, subject_text):
    if not subject_text.startswith("Subject: "):
        raise PreventUpdate
    
    subject_name = subject_text.replace("Subject: ", "")

    todo_data = load_data()
    if subject_name in todo_data:
        del todo_data[subject_name]
        save_data(todo_data)  

    updated_navbar = [
        html.Div([
            html.Button(subj, id={"type": "subject-btn", "index": subj}, n_clicks=0, className="navbar-button",
                        style={
                            "display": "inline-block",
                            "width": "80%",
                            "margin": "5px 0",
                            "padding": "8px",
                            "border": "1px solid #ccc",
                            "background-color": "#B0E0E6",
                            "text-align": "left",
                            "cursor": "pointer"
                        }),
            html.Button("❌", id={"type": "delete-subject-btn", "index": subj}, n_clicks=0, className="delete-button",
                        style={
                            "display": "inline-block",
                            "margin-left": "5px",
                            "padding": "5px",
                            "border": "none",
                            "background": "red",
                            "color": "white",
                            "cursor": "pointer",
                            "font-size": "14px"
                        })
        ], style={"display": "flex", "align-items": "center"})
        for subj in todo_data
    ]

    return updated_navbar, {}  # Hide popup after deletion



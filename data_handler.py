
import json
import os

# Path to JSON file
DATA_FILE = "todo_data.json"


def load_data():
    """Load todo data from JSON, ensuring it returns a dictionary."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                if not isinstance(data, dict):  # ✅ Ensure it's a dictionary
                    data = {}  
                return data
            except json.JSONDecodeError:
                return {}  # Return empty dictionary if JSON is corrupted
    return {}  # Return empty dictionary if file doesn't exist




def load_subject_tasks(subject_name):
    """
    Load tasks for a specific subject, ensuring a dictionary structure.
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)

                # ✅ Check if `data` is a list (wrong format)
                if isinstance(data, list):
                    print("⚠️ Warning: Incorrect JSON format. Resetting data.")
                    data = {}  # Reset to empty dictionary
                
                elif not isinstance(data, dict):  # Ensure it's a dictionary
                    data = {}

            except json.JSONDecodeError:
                data = {}  # Return empty dictionary if JSON is corrupted
    else:
        data = {}  # Return empty dictionary if file doesn't exist

    # ✅ Ensure subject tasks are in dictionary format
    return data.get(subject_name, {"ongoing": [], "completed": []})


def save_subject_tasks(subject_name, tasks):
    """
    Save tasks for a specific subject into the JSON file.
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                if not isinstance(data, dict):  # ✅ Ensure data is a dictionary
                    data = {}
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # ✅ Ensure tasks are stored correctly
    if not isinstance(tasks, dict):
        tasks = {"ongoing": [], "completed": []}

    # ✅ Store subject tasks in the correct format
    data[subject_name] = tasks

    # Save back to file
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)



def save_data(todo_data):
    """
    Ensure that the data is saved as a dictionary, not a list.
    """
    # ✅ If todo_data is not a dictionary, reset it
    if not isinstance(todo_data, dict):
        print("⚠️ Warning: Incorrect format detected. Resetting data.")
        todo_data = {}

    # ✅ Ensure all subjects have a dictionary structure
    for subject, tasks in todo_data.items():
        if not isinstance(tasks, dict):  # If tasks are not a dict, fix it
            todo_data[subject] = {"ongoing": [], "completed": []}

    # ✅ Save to JSON file
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(todo_data, f, indent=4)

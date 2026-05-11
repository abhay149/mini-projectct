import json
import os
from datetime import datetime


def load_json(file_path):
    """Load JSON safely"""
    try:
        if not os.path.exists(file_path):
            return []

        with open(file_path, "r") as f:
            return json.load(f)
    except:
        return []


def save_json(file_path, data):
    """Save JSON safely"""
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def append_json(file_path, new_data):
    """Append data to JSON file"""
    data = load_json(file_path)
    data.append(new_data)
    save_json(file_path, data)


def get_timestamp():
    """Return current timestamp"""
    return str(datetime.now())


def clean_text(text):
    """Basic text cleaning"""
    return text.lower().strip()
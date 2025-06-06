# src/utils.py

import os
from datetime import datetime

def ensure_output_dir(path="output"):
    """Create output directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)

def get_timestamped_filename(prefix="email_analysis", extension="xlsx"):
    """Generate a timestamped filename."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    return f"{prefix}_{timestamp}.{extension}"

def flatten_list_to_string(items):
    """Convert list items to newline-separated string."""
    return "\n".join(items) if isinstance(items, list) else str(items)

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M")

def create_run_output_folder(base="output", timestamp=None):
    if not timestamp:
        timestamp = get_timestamp()
    path = os.path.join(base, timestamp)
    os.makedirs(path, exist_ok=True)
    return path

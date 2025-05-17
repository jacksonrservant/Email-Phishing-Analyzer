# src/report_generator.py

import pandas as pd
import os
from datetime import datetime

def export_to_excel(parsed_data, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    
    # Format list values (like URLs or warnings) for Excel
    formatted_data = {}
    for key, value in parsed_data.items():
        if isinstance(value, list):
            formatted_data[key] = "\n".join(value) if value else "None"
        else:
            formatted_data[key] = value if value else "None"

    df = pd.DataFrame.from_dict(formatted_data, orient='index', columns=['Value'])

    filename = f"email_analysis_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.xlsx"
    filepath = os.path.join(output_dir, filename)

    df.to_excel(filepath, engine='openpyxl')

    print(f"[✓] Report saved to {filepath}")

import pandas as pd
import os
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl import load_workbook
from src.utils import flatten_list_to_string, ensure_output_dir

def export_to_excel(parsed_data, output_dir, timestamp):
    ensure_output_dir(output_dir)

    # Build summary section
    summary = parsed_data.get("summary", {})
    summary_lines = {
        "threat_level": summary.get("threat_level", "N/A"),
        "recommendation": summary.get("recommendation", "N/A"),
        "reason": summary.get("reason", "N/A")
    }

    # Combine summary with rest of data, excluding nested summary field
    flattened_data = {
        key: value for key, value in parsed_data.items()
        if key != "summary"
    }
    combined_data = {**summary_lines, **flattened_data}

    # Format all values
    formatted_data = {
        key: flatten_list_to_string(value)
        for key, value in combined_data.items()
    }

    # Convert to DataFrame and save
    df = pd.DataFrame.from_dict(formatted_data, orient='index', columns=['Value'])
    filename = f"email_analysis_{timestamp}.xlsx"
    filepath = os.path.join(output_dir, filename)
    df.to_excel(filepath, engine='openpyxl')

    # Load workbook to apply formatting
    wb = load_workbook(filepath)
    ws = wb.active

    # Define styles
    header_font = Font(bold=True)
    wrap_alignment = Alignment(wrap_text=True, vertical='top')
    border_style = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # Apply styles to all cells
    for row in ws.iter_rows():
        for cell in row:
            cell.alignment = wrap_alignment
            cell.border = border_style
            if cell.row == 1:
                cell.font = header_font

    # Auto-adjust column widths
    for column in ws.columns:
        max_length = 0
        col_letter = get_column_letter(column[0].column)
        for cell in column:
            try:
                length = len(str(cell.value))
                if length > max_length:
                    max_length = length
            except:
                pass
        ws.column_dimensions[col_letter].width = min(max_length + 2, 100)

    wb.save(filepath)
    print(f"[✓] Excel report saved to {filepath}")





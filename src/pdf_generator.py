# src/pdf_generator.py

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime
import os

def export_to_pdf(parsed_data, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    filename = f"email_analysis_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.pdf"
    filepath = os.path.join(output_dir, filename)

    c = canvas.Canvas(filepath, pagesize=LETTER)
    width, height = LETTER

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1 * inch, height - 1 * inch, "Phishing Email Analysis Report")

    # Metadata
    c.setFont("Helvetica", 10)
    c.drawString(1 * inch, height - 1.3 * inch, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Layout
    y = height - 1.6 * inch
    line_height = 12
    max_width = width - 1.5 * inch

    def draw_wrapped_text(label, text, y_pos):
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1 * inch, y_pos, f"{label}:")
        y_pos -= line_height

        c.setFont("Helvetica", 10)
        for line in split_text(text, max_width, c):
            c.drawString(1.2 * inch, y_pos, line)
            y_pos -= line_height
        return y_pos - line_height

    def split_text(text, max_width, canvas_obj):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if canvas_obj.stringWidth(test_line, "Helvetica", 10) < max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines

    # Fields to include
    fields_to_show = [
        ("Threat Level", parsed_data.get("summary", {}).get("threat_level", "N/A")),
        ("Recommendation", parsed_data.get("summary", {}).get("recommendation", "N/A")),
        ("Reason", parsed_data.get("summary", {}).get("reason", "N/A")),
        ("From", parsed_data.get("from", "N/A")),
        ("To", parsed_data.get("to", "N/A")),
        ("Subject", parsed_data.get("subject", "N/A")),
        ("Date", parsed_data.get("date", "N/A")),
        ("Body Snippet", parsed_data.get("body_snippet", "N/A")),
        ("URLs Found", "\n".join(parsed_data.get("urls_found", []))),
        ("Phishing Warnings", "\n".join(parsed_data.get("phishing_warnings", []))),
        ("URL Analysis", "\n".join(parsed_data.get("url_analysis", [])))
    ]

    for label, value in fields_to_show:
        if y < 1 * inch:
            c.showPage()
            y = height - 1 * inch
        y = draw_wrapped_text(label, str(value), y)

    c.save()
    print(f"[✓] PDF report saved to {filepath}")

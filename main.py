import os
import json
import email
from email import policy
from email.parser import BytesParser
import xlsxwriter
from fpdf import FPDF
from datetime import datetime

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_eml_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)
        return msg
    except Exception as e:
        print(f"[!] Failed to load EML file: {e}")
        return None

def extract_email_metadata(msg):
    return {
        'From': msg['From'],
        'To': msg['To'],
        'Subject': msg['Subject'],
        'Date': msg['Date'],
        'Reply-To': msg['Reply-To'],
        'Return-Path': msg['Return-Path'],
        'Received-SPF': msg['Received-SPF'],
        'Authentication-Results': msg['Authentication-Results'],
    }

def extract_auth_results(auth_header):
    results = {'SPF': None, 'DKIM': None, 'DMARC': None}
    if not auth_header:
        return results

    value_lower = auth_header.lower()
    if 'spf=' in value_lower:
        results['SPF'] = value_lower.split('spf=')[1].split()[0]
    if 'dkim=' in value_lower:
        results['DKIM'] = value_lower.split('dkim=')[1].split()[0]
    if 'dmarc=' in value_lower:
        results['DMARC'] = value_lower.split('dmarc=')[1].split()[0]

    return results

def analyze_phishing_indicators(msg):
    indicators = []

    from_addr = msg.get('From', '')
    reply_to = msg.get('Reply-To', '')

    if reply_to and reply_to != from_addr:
        indicators.append("Reply-To address does not match From address.")

    payload = msg.get_body(preferencelist=('plain', 'html'))
    if payload:
        content = payload.get_content()
        if 'http://' in content or 'https://' in content:
            indicators.append("Contains suspicious links.")
        if 'bit.ly' in content or 'tinyurl' in content:
            indicators.append("Contains shortened URLs.")
        if 'password' in content.lower() or 'verify account' in content.lower():
            indicators.append("Contains language asking for credentials.")

    return indicators

def export_to_json(metadata, auth_results, indicators, verdict, export_path):
    output = {
        "metadata": metadata,
        "auth_results": auth_results,
        "indicators": indicators,
        "verdict": verdict
    }
    with open(export_path, "w") as f:
        json.dump(output, f, indent=4)

def export_to_excel(metadata, auth_results, indicators, verdict, export_path):
    workbook = xlsxwriter.Workbook(export_path)
    worksheet = workbook.add_worksheet("Phishing Analysis")

    bold = workbook.add_format({'bold': True})
    row = 0

    worksheet.write(row, 0, "Metadata", bold)
    row += 1
    for key, value in metadata.items():
        worksheet.write(row, 0, key)
        worksheet.write(row, 1, value or "None")
        row += 1

    row += 1
    worksheet.write(row, 0, "Authentication Results", bold)
    row += 1
    for key, value in auth_results.items():
        worksheet.write(row, 0, key)
        worksheet.write(row, 1, value or "Not found")
        row += 1

    row += 1
    worksheet.write(row, 0, "Phishing Indicators", bold)
    for ind in indicators:
        row += 1
        worksheet.write(row, 0, f"- {ind}")
    if not indicators:
        row += 1
        worksheet.write(row, 0, "None found")

    row += 2
    worksheet.write(row, 0, "Verdict", bold)
    worksheet.write(row, 1, verdict)

    workbook.close()

def export_to_pdf(metadata, auth_results, indicators, verdict, export_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    def write_section(title, lines):
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, txt=title, ln=True)
        pdf.set_font("Arial", size=12)
        for line in lines:
            pdf.multi_cell(0, 10, txt=line)

    write_section("Email Metadata", [f"{k}: {v or 'None'}" for k, v in metadata.items()])
    write_section("Authentication Results", [f"{k}: {v or 'Not found'}" for k, v in auth_results.items()])
    write_section("Phishing Indicators", [f"- {ind}" for ind in indicators] if indicators else ["None found"])
    write_section("Verdict", [verdict])

    pdf.output(export_path)

def print_analysis_report(file_path, metadata, auth_results, indicators, verdict):
    print(f"\n📨 Analyzing: {file_path}")
    print("\n--- Email Metadata ---")
    for key, value in metadata.items():
        print(f"{key}: {value}")

    print("\n--- Authentication Results ---")
    for method, result in auth_results.items():
        print(f"{method}: {result if result else 'Not found'}")

    print("\n--- Phishing Indicators ---")
    if indicators:
        for ind in indicators:
            print(f"[!] {ind}")
    else:
        print("[✓] No strong phishing indicators found.")

    print("\n--- Verdict ---")
    print(f"{'⚠️  Suspicious email detected.' if '!' in verdict else '✅ Email appears safe.'}")

def main():
    input_path = "input_samples/suspicious_email.eml"
    msg = load_eml_file(input_path)

    if not msg:
        return

    metadata = extract_email_metadata(msg)
    auth_results = extract_auth_results(metadata.get('Authentication-Results', ''))
    indicators = analyze_phishing_indicators(msg)
    verdict = "⚠️  Suspicious email detected. Proceed with caution." if indicators or any(v != 'pass' for v in auth_results.values() if v) else "✅ Email appears safe."

    print_analysis_report(input_path, metadata, auth_results, indicators, verdict)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"{OUTPUT_DIR}/phishing_analysis_{timestamp}"

    export_to_json(metadata, auth_results, indicators, verdict, base_filename + ".json")
    export_to_excel(metadata, auth_results, indicators, verdict, base_filename + ".xlsx")
    export_to_pdf(metadata, auth_results, indicators, verdict, base_filename + ".pdf")

    print(f"\n[+] Reports exported to '{OUTPUT_DIR}/'")

if __name__ == "__main__":
    main()






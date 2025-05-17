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
        worksheet.write(row, 1, value





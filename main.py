# main.py

import argparse
import json
import os

from src.email_parser import parse_email
from src.analyzer import analyze, generate_summary
from src.url_checker import analyze_urls
from src.report_generator import export_to_excel
from src.utils import ensure_output_dir, get_timestamped_filename
from src.pdf_generator import export_to_pdf

def main():
    parser = argparse.ArgumentParser(
        description="PhishSleuth - Analyze .eml files for phishing indicators"
    )
    parser.add_argument("email_file", help="Path to the .eml email file")
    args = parser.parse_args()

    print(f"[+] Parsing email file: {args.email_file}")
    parsed_data = parse_email(args.email_file)

    print("[+] Analyzing email content for phishing indicators...")
    parsed_data = analyze(parsed_data)

    print("[+] Checking URLs for suspicious patterns...")
    url_analysis = analyze_urls(parsed_data.get("urls_found", []))
    parsed_data["url_analysis"] = [
        f"{item['url']} — {'; '.join(item['reasons'])}" if item["suspicious"]
        else f"{item['url']} — clean"
        for item in url_analysis
    ]

    print("[+] Generating summary assessment...")
    parsed_data["summary"] = generate_summary(parsed_data)

    print("[+] Exporting Excel report...")
    export_to_excel(parsed_data)

    print("[+] Saving JSON report...")
    ensure_output_dir("output")
    json_path = os.path.join("output", get_timestamped_filename(extension="json"))
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, indent=2)
        print(f"[✓] JSON report saved to {json_path}")

    print("[+] Exporting PDF report...")
    export_to_pdf(parsed_data)


    print("[✓] Analysis complete.")

if __name__ == "__main__":
    main()



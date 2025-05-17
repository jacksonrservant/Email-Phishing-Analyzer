# main.py

import argparse
import json
import os
from src.email_parser import parse_email
from src.analyzer import analyze
from src.url_checker import analyze_urls
from src.report_generator import export_to_excel
from src.utils import ensure_output_dir, get_timestamped_filename

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

    print("[+] Exporting Excel report...")
    export_to_excel(parsed_data)

    print("[+] Saving JSON report...")
    ensure_output_dir("output")
    json_path = os.path.join("output", get_timestamped_filename(extension="json"))
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, indent=2)
        print(f"[✓] JSON report saved to {json_path}")

    print("[✓] Analysis complete.")

if __name__ == "__main__":
    main()

# main.py

import argparse
from src.email_parser import parse_email
from src.report_generator import export_to_excel

def main():
    parser = argparse.ArgumentParser(
        description="Analyze .eml files for phishing indicators"
    )
    parser.add_argument("email_file", help="Path to the .eml email file")
    args = parser.parse_args()

    print(f"[+] Parsing email file: {args.email_file}")
    parsed_data = parse_email(args.email_file)

    print("[+] Exporting analysis report...")
    export_to_excel(parsed_data)

    print("[✓] Analysis complete.")

if __name__ == "__main__":
    main()

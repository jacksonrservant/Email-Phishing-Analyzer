# web_interface.py

import streamlit as st
import os
import tempfile
from src.email_parser import parse_email
from src.analyzer import analyze, generate_summary
from src.url_checker import analyze_urls
from src.report_generator import export_to_excel
from src.pdf_generator import export_to_pdf
from src.utils import get_timestamp, create_run_output_folder

st.set_page_config(page_title="Phishing Email Analyzer", layout="wide")

st.title("Phishing Email Analyzer")
st.markdown("Upload a `.eml` file to analyze it for phishing indicators and generate reports.")

uploaded_file = st.file_uploader("Drag and drop or click to upload a .eml file", type="eml")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".eml") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    st.success(" File uploaded successfully!")

    st.write(" Running analysis...")

    parsed_data = parse_email(tmp_file_path)
    parsed_data = analyze(parsed_data)
    url_analysis = analyze_urls(parsed_data.get("urls_found", []))
    parsed_data["url_analysis"] = [
        f"{item['url']} — {'; '.join(item['reasons'])}" if item["suspicious"]
        else f"{item['url']} — clean"
        for item in url_analysis
    ]
    parsed_data["summary"] = generate_summary(parsed_data)

    timestamp = get_timestamp()
    output_dir = create_run_output_folder(timestamp=timestamp)

    export_to_excel(parsed_data, output_dir=output_dir, timestamp=timestamp)

    json_path = os.path.join(output_dir, f"email_analysis_{timestamp}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump(parsed_data, f, indent=2)

    export_to_pdf(parsed_data, output_dir=output_dir, timestamp=timestamp)

    st.success(" Analysis complete!")

    st.subheader(" Download Reports")
    with open(json_path, "rb") as f:
        st.download_button("📄 Download JSON", f, file_name=os.path.basename(json_path))
    with open(os.path.join(output_dir, f"email_analysis_{timestamp}.xlsx"), "rb") as f:
        st.download_button("📊 Download Excel", f, file_name=f"email_analysis_{timestamp}.xlsx")
    with open(os.path.join(output_dir, f"email_analysis_{timestamp}.pdf"), "rb") as f:
        st.download_button("📘 Download PDF", f, file_name=f"email_analysis_{timestamp}.pdf")

    st.subheader(" Threat Summary")
    st.markdown(f"**Threat Level:** {parsed_data['summary']['threat_level']}")
    st.markdown(f"**Recommendation:** {parsed_data['summary']['recommendation']}")
    st.markdown(f"**Reason:** {parsed_data['summary']['reason']}")

import pandas as pd
import streamlit as st

from toolkit.formatting import dataframe_to_html_table, fmt_ci, fmt_float, fmt_int, word_compatible_html
from toolkit.parsers import parse_multiple_moa
from toolkit.ui import ToolInfo, configure_page, render_download_block, render_parse_report, render_tool_header, render_verification_box, render_workflow

configure_page("Outcomes Table Generator", "🧮")
render_tool_header(ToolInfo(title="Outcomes Table Generator", icon="🧮", purpose="Create a manuscript-ready outcome table from one or more TriNetX Measures of Association exports.", use_when="You need Table 2-style outcome counts, risks, effect estimates, confidence intervals, and p-values.", primary_input="TriNetX Measures of Association CSV files.", outputs="Editable table, CSV, HTML, and Word-compatible HTML."))
render_workflow()

uploads = st.file_uploader("Upload one or more MOA CSV files", type=["csv", "txt"], accept_multiple_files=True)
st.sidebar.header("Formatting")
table_title = st.sidebar.text_input("Table title", "Table 2. Outcomes by Cohort")
estimate = st.sidebar.selectbox("Primary estimate", ["Risk Ratio", "Odds Ratio"])
digits = st.sidebar.slider("Decimal places", 2, 4, 2)

if not uploads:
    st.info("Upload MOA files to begin.")
    st.stop()

parsed = parse_multiple_moa(uploads)
render_parse_report(parsed.report)
source = parsed.data.copy()
prefix = "RR" if estimate == "Risk Ratio" else "OR"

table = pd.DataFrame({
    "Outcome": source["Outcome"],
    "Cohort 1 Events/N": source["Cohort 1 Events"].map(fmt_int) + "/" + source["Cohort 1 N"].map(fmt_int),
    "Cohort 1 Risk": source["Cohort 1 Risk"].map(lambda x: fmt_float(float(x) * 100, digits) + "%" if pd.notna(x) else ""),
    "Cohort 2 Events/N": source["Cohort 2 Events"].map(fmt_int) + "/" + source["Cohort 2 N"].map(fmt_int),
    "Cohort 2 Risk": source["Cohort 2 Risk"].map(lambda x: fmt_float(float(x) * 100, digits) + "%" if pd.notna(x) else ""),
    estimate + " (95% CI)": [fmt_ci(a, b, c, digits) for a, b, c in zip(source[estimate], source[f"{prefix} Lower CI"], source[f"{prefix} Upper CI"])],
    "p": source[f"{prefix} p"].map(lambda x: "<.001" if pd.notna(x) and x < 0.001 else (fmt_float(x, 3) if pd.notna(x) else "")),
})

st.subheader("1. Edit final table")
edited = st.data_editor(table, num_rows="dynamic", use_container_width=True)

render_download_block()
html = dataframe_to_html_table(edited, table_title)
st.download_button("Download CSV", data=edited.to_csv(index=False).encode("utf-8"), file_name="trinetx_outcomes_table.csv", mime="text/csv")
st.download_button("Download HTML", data=html.encode("utf-8"), file_name="trinetx_outcomes_table.html", mime="text/html")
st.download_button("Download Word-compatible HTML", data=word_compatible_html(html, table_title).encode("utf-8"), file_name="trinetx_outcomes_table.doc", mime="application/msword")
render_verification_box()

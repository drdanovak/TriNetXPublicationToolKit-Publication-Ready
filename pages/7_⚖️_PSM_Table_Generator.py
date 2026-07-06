import pandas as pd
import streamlit as st

from toolkit.formatting import dataframe_to_html_table, fmt_float, fmt_int, word_compatible_html
from toolkit.parsers import parse_baseline
from toolkit.ui import ToolInfo, configure_page, render_download_block, render_parse_report, render_tool_header, render_verification_box, render_workflow

configure_page("PSM Table Generator", "⚖️")
render_tool_header(ToolInfo(title="PSM Table Generator", icon="⚖️", purpose="Create a manuscript-ready baseline table before and after propensity score matching.", use_when="You need a Table 1 that reports baseline covariates, counts/percentages, and SMDs.", primary_input="TriNetX Baseline Patient Characteristics CSV.", outputs="Editable table, CSV, HTML, and Word-compatible HTML."))
render_workflow()

upload = st.file_uploader("Upload Baseline Patient Characteristics CSV", type=["csv", "txt"])
st.sidebar.header("Formatting")
table_title = st.sidebar.text_input("Table title", "Table 1. Baseline Characteristics Before and After Propensity Score Matching")
digits = st.sidebar.slider("SMD decimal places", 2, 4, 3)

if upload is None:
    st.info("Upload a baseline characteristics export to begin.")
    st.stop()

try:
    result = parse_baseline(upload.getvalue(), upload.name)
except Exception as exc:
    st.error(str(exc))
    st.stop()

render_parse_report(result.report)
df = result.data.copy()
name_col = "Characteristic Name"
cat_col = "Category"
before_smd = result.report.get("before_smd_column")
after_smd = result.report.get("after_smd_column")
count_cols = [c for c in df.columns if "patients" in c.lower() or "count" in c.lower() or "cohort" in c.lower()]

st.subheader("1. Select display columns")
selected_cols = st.multiselect("Columns to include", df.columns.tolist(), default=[c for c in [name_col, cat_col] + count_cols + [before_smd, after_smd] if c in df.columns])
if not selected_cols:
    st.stop()

table = df[selected_cols].copy()
for col in table.columns:
    if "smd" in col.lower() or "standardized mean difference" in col.lower():
        table[col] = pd.to_numeric(table[col], errors="coerce").map(lambda x: fmt_float(x, digits))
    elif pd.api.types.is_numeric_dtype(table[col]):
        table[col] = table[col].map(fmt_int)

st.subheader("2. Edit final table")
edited = st.data_editor(table, num_rows="dynamic", use_container_width=True)

render_download_block()
html = dataframe_to_html_table(edited, table_title)
st.download_button("Download CSV", data=edited.to_csv(index=False).encode("utf-8"), file_name="trinetx_psm_table.csv", mime="text/csv")
st.download_button("Download HTML", data=html.encode("utf-8"), file_name="trinetx_psm_table.html", mime="text/html")
st.download_button("Download Word-compatible HTML", data=word_compatible_html(html, table_title).encode("utf-8"), file_name="trinetx_psm_table.doc", mime="application/msword")
render_verification_box()

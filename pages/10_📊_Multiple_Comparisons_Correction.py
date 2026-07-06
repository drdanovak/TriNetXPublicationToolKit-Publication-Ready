import pandas as pd
import streamlit as st

from toolkit.parsers import parse_multiple_moa
from toolkit.stats import apply_multiple_comparison_methods
from toolkit.ui import ToolInfo, configure_page, render_download_block, render_parse_report, render_tool_header, render_verification_box, render_workflow

configure_page("Multiple Comparisons Correction", "📊")
render_tool_header(ToolInfo(title="Multiple Comparisons Correction", icon="📊", purpose="Apply standard multiplicity corrections to p-values from multiple tested TriNetX outcomes.", use_when="You have several outcomes, subgroups, or comparator tests and need a transparent correction table.", primary_input="MOA files or manual p-value table.", outputs="Adjusted p-value table and CSV report."))
render_workflow(["Define the family of tests before interpreting results.", "Upload MOA files or enter p-values manually.", "Review extracted p-values and edit labels.", "Compare unadjusted and adjusted results.", "Download the correction table and report the chosen method."])

st.sidebar.header("Input")
mode = st.sidebar.radio("Input mode", ["TriNetX MOA files", "Manual p-value table"])
st.sidebar.header("Analysis settings")
alpha = st.sidebar.number_input("Alpha", min_value=0.0001, max_value=0.5, value=0.05, step=0.01)
p_source = st.sidebar.selectbox("P-value source from MOA", ["RR p", "OR p", "RD p"])

if mode == "TriNetX MOA files":
    uploads = st.file_uploader("Upload MOA CSV files", type=["csv", "txt"], accept_multiple_files=True)
    if uploads:
        parsed = parse_multiple_moa(uploads)
        render_parse_report(parsed.report)
        base = pd.DataFrame({"Test": parsed.data["Outcome"], "p": parsed.data[p_source]})
    else:
        base = pd.DataFrame(columns=["Test", "p"])
else:
    base = pd.DataFrame({"Test": ["Outcome 1", "Outcome 2", "Outcome 3"], "p": [0.01, 0.04, 0.20]})

st.subheader("1. Confirm p-values")
edited = st.data_editor(base, num_rows="dynamic", use_container_width=True)
edited["p"] = pd.to_numeric(edited["p"], errors="coerce")
valid = edited.dropna(subset=["Test", "p"]).copy()
valid = valid[(valid["p"] >= 0) & (valid["p"] <= 1)]

st.subheader("2. Adjusted p-values")
if valid.empty:
    st.info("Enter at least one valid p-value.")
else:
    adjusted = apply_multiple_comparison_methods(valid["p"].tolist(), alpha=alpha)
    out = valid.copy()
    for method, values in adjusted.items():
        out[f"{method} adjusted p"] = values["adjusted_p"]
        out[f"{method} significant"] = values["reject"]
    st.dataframe(out, hide_index=True, use_container_width=True)
    render_download_block()
    st.download_button("Download correction table CSV", data=out.to_csv(index=False).encode("utf-8"), file_name="trinetx_multiple_comparisons.csv", mime="text/csv")

render_verification_box()

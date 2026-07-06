import io

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from toolkit.parsers import parse_multiple_moa
from toolkit.ui import ToolInfo, configure_page, render_download_block, render_parse_report, render_tool_header, render_verification_box, render_workflow

configure_page("Two-Cohort Outcome Bar Graphs", "📊")
render_tool_header(ToolInfo(title="Two-Cohort Outcome Bar Graphs", icon="📊", purpose="Plot absolute outcome risks for two cohorts using a colorblind-friendly default design.", use_when="You want a figure that complements relative estimates with absolute risks.", primary_input="TriNetX MOA files or manual risk table.", outputs="Editable risk table, CSV, and 300 DPI PNG."))
render_workflow()

st.sidebar.header("Input")
mode = st.sidebar.radio("Input mode", ["TriNetX MOA files", "Manual risk table"])
st.sidebar.header("Labels")
cohort1_label = st.sidebar.text_input("Cohort 1 label", "Cohort 1")
cohort2_label = st.sidebar.text_input("Cohort 2 label", "Cohort 2")
st.sidebar.header("Formatting")
plot_title = st.sidebar.text_input("Plot title", "Outcome Risk by Cohort")
y_label = st.sidebar.text_input("Y-axis label", "Risk (%)")
orientation = st.sidebar.radio("Orientation", ["Vertical", "Horizontal"])
fig_width = st.sidebar.slider("Figure width", 6, 14, 9)
fig_height = st.sidebar.slider("Figure height", 4, 12, 6)

if mode == "TriNetX MOA files":
    uploads = st.file_uploader("Upload MOA CSV files", type=["csv", "txt"], accept_multiple_files=True)
    if uploads:
        parsed = parse_multiple_moa(uploads)
        render_parse_report(parsed.report)
        base = pd.DataFrame({"Outcome": parsed.data["Outcome"], "Cohort 1 Risk": parsed.data["Cohort 1 Risk"], "Cohort 2 Risk": parsed.data["Cohort 2 Risk"]})
    else:
        base = pd.DataFrame(columns=["Outcome", "Cohort 1 Risk", "Cohort 2 Risk"])
else:
    base = pd.DataFrame({"Outcome": ["Example outcome"], "Cohort 1 Risk": [0.10], "Cohort 2 Risk": [0.15]})

st.subheader("1. Confirm or edit risks")
st.caption("Enter risks as proportions. Example: 0.15 will display as 15 percent.")
edited = st.data_editor(base, num_rows="dynamic", use_container_width=True)
for col in ["Cohort 1 Risk", "Cohort 2 Risk"]:
    edited[col] = pd.to_numeric(edited[col], errors="coerce")
valid = edited.dropna(subset=["Outcome", "Cohort 1 Risk", "Cohort 2 Risk"]).copy()

st.subheader("2. Preview graph")
if valid.empty:
    st.info("Enter at least one valid outcome and two risks.")
else:
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    y1 = valid["Cohort 1 Risk"] * 100
    y2 = valid["Cohort 2 Risk"] * 100
    x = np.arange(len(valid))
    width = 0.38
    if orientation == "Vertical":
        ax.bar(x - width / 2, y1, width, label=cohort1_label)
        ax.bar(x + width / 2, y2, width, label=cohort2_label)
        ax.set_xticks(x)
        ax.set_xticklabels(valid["Outcome"], rotation=45, ha="right")
        ax.set_ylabel(y_label)
    else:
        ax.barh(x - width / 2, y1, width, label=cohort1_label)
        ax.barh(x + width / 2, y2, width, label=cohort2_label)
        ax.set_yticks(x)
        ax.set_yticklabels(valid["Outcome"])
        ax.set_xlabel(y_label)
        ax.invert_yaxis()
    ax.set_title(plot_title)
    ax.legend()
    fig.tight_layout()
    st.pyplot(fig)
    render_download_block()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    st.download_button("Download PNG", data=buf.getvalue(), file_name="trinetx_two_cohort_bar_graph.png", mime="image/png")

st.download_button("Download risk table CSV", data=edited.to_csv(index=False).encode("utf-8"), file_name="trinetx_two_cohort_risk_table.csv", mime="text/csv")
render_verification_box()

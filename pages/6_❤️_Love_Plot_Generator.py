import io

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from toolkit.parsers import parse_baseline
from toolkit.ui import ToolInfo, configure_page, render_download_block, render_parse_report, render_tool_header, render_verification_box, render_workflow

configure_page("Love Plot Generator", "❤️")
render_tool_header(ToolInfo(title="Love Plot Generator", icon="❤️", purpose="Visualize standardized mean differences before and after matching.", use_when="You need to evaluate and communicate covariate balance after propensity score matching.", primary_input="TriNetX Baseline Patient Characteristics CSV.", outputs="Balance diagnostics table, CSV, and 300 DPI PNG Love plot."))
render_workflow()

upload = st.file_uploader("Upload Baseline Patient Characteristics CSV", type=["csv", "txt"])
st.sidebar.header("Analysis settings")
threshold = st.sidebar.number_input("SMD threshold", min_value=0.0, value=0.10, step=0.01)
max_rows = st.sidebar.slider("Maximum covariates to display", 5, 80, 30)
st.sidebar.header("Formatting")
plot_title = st.sidebar.text_input("Plot title", "Covariate Balance Before and After Matching")
fig_width = st.sidebar.slider("Figure width", 6, 14, 9)
row_height = st.sidebar.slider("Height per covariate", 0.25, 0.7, 0.4)

if upload is None:
    st.info("Upload a baseline characteristics export to begin.")
    st.stop()

try:
    result = parse_baseline(upload.getvalue(), upload.name)
except Exception as exc:
    st.error(str(exc))
    st.stop()

render_parse_report(result.report)
df = result.data
before_col = result.report.get("before_smd_column")
after_col = result.report.get("after_smd_column")
if not before_col or not after_col:
    st.error("Before and after SMD columns are required for Love plot generation.")
    st.stop()

work = df[["Characteristic Name", "Category", before_col, after_col]].copy()
work[before_col] = pd.to_numeric(work[before_col], errors="coerce").abs()
work[after_col] = pd.to_numeric(work[after_col], errors="coerce").abs()
work = work.dropna(subset=[before_col, after_col])
work["Display Label"] = work["Characteristic Name"].astype(str) + ": " + work["Category"].astype(str)
work = work.sort_values(after_col, ascending=False).head(max_rows)
work["Balanced After Matching"] = work[after_col] < threshold

st.subheader("1. Balance diagnostics")
st.dataframe(work, hide_index=True, use_container_width=True)

st.subheader("2. Love plot")
fig, ax = plt.subplots(figsize=(fig_width, max(3, len(work) * row_height)))
y = range(len(work))
ax.scatter(work[before_col], y, label="Before matching")
ax.scatter(work[after_col], y, label="After matching")
ax.axvline(threshold, linestyle="--", linewidth=1)
ax.set_yticks(list(y))
ax.set_yticklabels(work["Display Label"])
ax.invert_yaxis()
ax.set_xlabel("Absolute standardized mean difference")
ax.set_title(plot_title)
ax.legend()
fig.tight_layout()
st.pyplot(fig)

render_download_block()
buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
st.download_button("Download PNG", data=buf.getvalue(), file_name="trinetx_love_plot.png", mime="image/png")
st.download_button("Download balance table CSV", data=work.to_csv(index=False).encode("utf-8"), file_name="trinetx_love_plot_balance_table.csv", mime="text/csv")
render_verification_box()

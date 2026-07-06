import io

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from toolkit.parsers import parse_multiple_moa
from toolkit.ui import ToolInfo, configure_page, render_download_block, render_parse_report, render_tool_header, render_verification_box, render_workflow

configure_page("Forest Plot Generator", "🌲")
render_tool_header(ToolInfo(title="Forest Plot Generator", icon="🌲", purpose="Create publication-ready forest plots from TriNetX MOA exports or an edited estimate table.", use_when="You want to visualize RR, OR, or HR estimates across outcomes or subgroups.", primary_input="TriNetX MOA files or manual estimate table.", outputs="Editable estimate table, CSV, and 300 DPI PNG."))
render_workflow()

st.sidebar.header("Input")
mode = st.sidebar.radio("Input mode", ["TriNetX MOA files", "Manual estimate table"])
st.sidebar.header("Analysis settings")
estimate_type = st.sidebar.selectbox("Estimate", ["Risk Ratio", "Odds Ratio", "Hazard Ratio"])
st.sidebar.header("Formatting")
plot_title = st.sidebar.text_input("Plot title", f"{estimate_type} Forest Plot")
x_label = st.sidebar.text_input("X-axis label", estimate_type)
fig_width = st.sidebar.slider("Figure width", 6, 14, 9)
row_height = st.sidebar.slider("Height per row", 0.3, 0.8, 0.45)
show_grid = st.sidebar.checkbox("Show grid", value=True)

if mode == "TriNetX MOA files":
    uploads = st.file_uploader("Upload MOA CSV files", type=["csv", "txt"], accept_multiple_files=True)
    if uploads:
        parsed = parse_multiple_moa(uploads)
        render_parse_report(parsed.report)
        prefix = {"Risk Ratio": "RR", "Odds Ratio": "OR", "Hazard Ratio": "HR"}[estimate_type]
        if estimate_type == "Hazard Ratio":
            st.warning("MOA files usually provide RR/OR. Use manual mode for hazard ratios from Kaplan-Meier exports.")
        base = pd.DataFrame({
            "Label": parsed.data["Outcome"],
            "Estimate": parsed.data.get(f"{prefix.replace('HR','RR')}" if prefix == "HR" else estimate_type, np.nan),
            "Lower CI": parsed.data.get(f"{prefix} Lower CI", np.nan),
            "Upper CI": parsed.data.get(f"{prefix} Upper CI", np.nan),
            "p": parsed.data.get(f"{prefix} p", np.nan),
        })
    else:
        base = pd.DataFrame(columns=["Label", "Estimate", "Lower CI", "Upper CI", "p"])
else:
    base = pd.DataFrame({"Label": ["Example outcome"], "Estimate": [0.76], "Lower CI": [0.60], "Upper CI": [0.95], "p": [0.017]})

st.subheader("1. Confirm or edit estimates")
edited = st.data_editor(base, num_rows="dynamic", use_container_width=True)
for col in ["Estimate", "Lower CI", "Upper CI", "p"]:
    edited[col] = pd.to_numeric(edited[col], errors="coerce")
valid = edited.dropna(subset=["Estimate", "Lower CI", "Upper CI"]).copy()
valid = valid[(valid["Estimate"] > 0) & (valid["Lower CI"] > 0) & (valid["Upper CI"] > 0)]

st.subheader("2. Preview forest plot")
if valid.empty:
    st.info("Enter at least one valid positive estimate and CI.")
else:
    y = np.arange(len(valid))
    fig, ax = plt.subplots(figsize=(fig_width, max(3, len(valid) * row_height)))
    ax.errorbar(valid["Estimate"], y, xerr=[valid["Estimate"] - valid["Lower CI"], valid["Upper CI"] - valid["Estimate"]], fmt="o", capsize=3)
    ax.axvline(1.0, linestyle="--", linewidth=1)
    ax.set_xscale("log")
    ax.set_yticks(y)
    ax.set_yticklabels(valid["Label"])
    ax.invert_yaxis()
    ax.set_xlabel(x_label)
    ax.set_title(plot_title)
    if show_grid:
        ax.grid(True, axis="x", linestyle=":")
    fig.tight_layout()
    st.pyplot(fig)
    render_download_block()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    st.download_button("Download PNG", data=buf.getvalue(), file_name="trinetx_forest_plot.png", mime="image/png")

st.download_button("Download estimate table CSV", data=edited.to_csv(index=False).encode("utf-8"), file_name="trinetx_forest_plot_estimates.csv", mime="text/csv")
render_verification_box()

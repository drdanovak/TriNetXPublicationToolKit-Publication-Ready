import io

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from toolkit.stats import ratio_to_log_effect
from toolkit.ui import ToolInfo, configure_page, render_download_block, render_tool_header, render_verification_box, render_workflow

configure_page("Effect Size Calculator", "📐")
render_tool_header(
    ToolInfo(
        title="Effect Size Calculator",
        icon="📐",
        purpose="Convert ratio estimates into approximate standardized log-ratio summaries and optionally draw a ratio-scale forest plot.",
        use_when="You have risk ratios, odds ratios, or hazard ratios and want a compact interpretive table or simple forest plot.",
        primary_input="Manual table with outcome, ratio, lower CI, upper CI, and optional p-value.",
        outputs="CSV table and 300 DPI PNG forest plot.",
    )
)
render_workflow()

st.sidebar.header("Input")
ratio_type = st.sidebar.selectbox("Ratio type", ["Risk Ratio", "Odds Ratio", "Hazard Ratio"])
st.sidebar.header("Formatting")
plot_scale = st.sidebar.radio("Forest plot scale", ["Ratio scale", "Standardized log-ratio scale"], index=0)
show_grid = st.sidebar.checkbox("Show grid", value=True)
fig_width = st.sidebar.slider("Figure width", 6, 14, 9)
row_height = st.sidebar.slider("Height per row", 0.3, 0.8, 0.45)

st.subheader("1. Add or edit estimates")
default_df = pd.DataFrame(
    {
        "Outcome": ["Example outcome"],
        "Ratio": [0.76],
        "Lower CI": [0.60],
        "Upper CI": [0.95],
        "p": [0.017],
    }
)
edited = st.data_editor(default_df, num_rows="dynamic", use_container_width=True)

work = edited.copy()
for col in ["Ratio", "Lower CI", "Upper CI", "p"]:
    work[col] = pd.to_numeric(work[col], errors="coerce")
work = work[work["Outcome"].astype(str).str.strip() != ""].copy()
work["Approx standardized log-ratio"] = work["Ratio"].apply(ratio_to_log_effect)
work["Approx lower"] = work["Lower CI"].apply(ratio_to_log_effect)
work["Approx upper"] = work["Upper CI"].apply(ratio_to_log_effect)

st.subheader("2. Review calculated table")
st.dataframe(work, hide_index=True, use_container_width=True)
st.caption("The standardized log-ratio is an interpretive aid. Primary TriNetX results should remain the original RR, OR, or HR with confidence intervals.")

st.subheader("3. Preview forest plot")
if work.empty:
    st.info("Enter at least one row to generate a plot.")
else:
    valid = work.dropna(subset=["Ratio", "Lower CI", "Upper CI"]).copy()
    if valid.empty:
        st.warning("A forest plot requires point estimates and confidence intervals.")
    else:
        if plot_scale == "Ratio scale":
            x = valid["Ratio"]
            lo = valid["Lower CI"]
            hi = valid["Upper CI"]
            null = 1.0
            xlabel = ratio_type
        else:
            x = valid["Approx standardized log-ratio"]
            lo = valid["Approx lower"]
            hi = valid["Approx upper"]
            null = 0.0
            xlabel = "Approx standardized log-ratio"

        y = np.arange(len(valid))
        fig, ax = plt.subplots(figsize=(fig_width, max(3, len(valid) * row_height)))
        ax.errorbar(x, y, xerr=[x - lo, hi - x], fmt="o", capsize=3)
        ax.axvline(null, linestyle="--", linewidth=1)
        ax.set_yticks(y)
        ax.set_yticklabels(valid["Outcome"])
        ax.invert_yaxis()
        ax.set_xlabel(xlabel)
        ax.set_title(f"{ratio_type} Forest Plot")
        if plot_scale == "Ratio scale":
            ax.set_xscale("log")
        if show_grid:
            ax.grid(True, axis="x", linestyle=":")
        fig.tight_layout()
        st.pyplot(fig)

        render_download_block()
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
        st.download_button("Download PNG", data=buf.getvalue(), file_name="trinetx_effect_size_forest_plot.png", mime="image/png")

csv_bytes = work.to_csv(index=False).encode("utf-8")
st.download_button("Download calculated table CSV", data=csv_bytes, file_name="trinetx_effect_size_table.csv", mime="text/csv")
render_verification_box()

import io

import matplotlib.pyplot as plt
import streamlit as st

from toolkit.parsers import parse_km
from toolkit.ui import ToolInfo, configure_page, render_download_block, render_parse_report, render_tool_header, render_verification_box, render_workflow

configure_page("Kaplan-Meier Curve Maker", "📉")
render_tool_header(ToolInfo(title="Kaplan-Meier Curve Maker", icon="📉", purpose="Create a publication-ready time-to-event curve from a TriNetX Kaplan-Meier export.", use_when="You need a clean survival or event-free probability figure with editable labels and parser warnings.", primary_input="TriNetX Kaplan-Meier CSV export.", outputs="300 DPI PNG curve and parsed data CSV."))
render_workflow()

st.sidebar.header("Input")
upload = st.file_uploader("Upload TriNetX Kaplan-Meier CSV", type=["csv", "txt"])
st.sidebar.header("Labels")
label1 = st.sidebar.text_input("Cohort 1 label", "Cohort 1")
label2 = st.sidebar.text_input("Cohort 2 label", "Cohort 2")
plot_title = st.sidebar.text_input("Plot title", "Kaplan-Meier Curve")
x_label = st.sidebar.text_input("X-axis label", "Time (Days)")
y_label = st.sidebar.text_input("Y-axis label", "Survival Probability")
st.sidebar.header("Formatting")
show_grid = st.sidebar.checkbox("Show grid", value=True)
fig_width = st.sidebar.slider("Figure width", 6, 14, 9)
fig_height = st.sidebar.slider("Figure height", 4, 10, 6)
y_min = st.sidebar.number_input("Y-axis minimum", value=0.0, min_value=0.0, max_value=1.5)
y_max = st.sidebar.number_input("Y-axis maximum", value=1.05, min_value=0.0, max_value=1.5)

if upload is None:
    st.info("Upload a Kaplan-Meier export to begin.")
    st.stop()

try:
    result = parse_km(upload.getvalue(), upload.name)
except Exception as exc:
    st.error(str(exc))
    st.stop()

render_parse_report(result.report)
df = result.data
time_col = result.report["time_column"]
surv1, surv2 = result.report["survival_columns"][:2]

st.subheader("1. Confirm parsed data")
st.dataframe(df.head(20), hide_index=True, use_container_width=True)

max_days = st.sidebar.number_input("Maximum days to display", min_value=0.0, value=float(df[time_col].max()))
plot_df = df[df[time_col] <= max_days].copy()

st.subheader("2. Preview curve")
fig, ax = plt.subplots(figsize=(fig_width, fig_height))
ax.step(plot_df[time_col], plot_df[surv1], where="post", label=label1)
ax.step(plot_df[time_col], plot_df[surv2], where="post", label=label2)
ax.set_title(plot_title)
ax.set_xlabel(x_label)
ax.set_ylabel(y_label)
ax.set_ylim(y_min, y_max)
ax.legend()
if show_grid:
    ax.grid(True, linestyle=":")
fig.tight_layout()
st.pyplot(fig)

render_download_block()
buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
st.download_button("Download PNG", data=buf.getvalue(), file_name="trinetx_kaplan_meier_curve.png", mime="image/png")
st.download_button("Download parsed data CSV", data=df.to_csv(index=False).encode("utf-8"), file_name="trinetx_km_parsed_data.csv", mime="text/csv")
render_verification_box()

import numpy as np
import pandas as pd
import streamlit as st

from toolkit.parsers import parse_multiple_moa
from toolkit.stats import cohens_h, e_value_from_rr, nnt_nnh_from_rd, risk_difference, risk_ratio_from_risks, two_proportion_power
from toolkit.ui import ToolInfo, configure_page, render_download_block, render_parse_report, render_tool_header, render_verification_box, render_workflow

configure_page("Power, E-value, and NNT/NNH", "🎯")
render_tool_header(
    ToolInfo(
        title="Power, E-value, and NNT/NNH",
        icon="🎯",
        purpose="Separate statistical power, E-value sensitivity, absolute clinical impact, and standardized risk-difference magnitude.",
        use_when="You want to contextualize outcome comparisons after reviewing the primary TriNetX outputs.",
        primary_input="TriNetX MOA files or manual Group 1 and Group 2 risk table.",
        outputs="Metric cards and downloadable CSV interpretation table.",
    )
)
render_workflow()

st.sidebar.header("Input")
mode = st.sidebar.radio("Input mode", ["TriNetX MOA files", "Manual risk table"])
st.sidebar.header("Analysis settings")
alpha = st.sidebar.number_input("Alpha", min_value=0.0001, max_value=0.5, value=0.05, step=0.01)
two_sided = st.sidebar.checkbox("Two-sided power calculation", value=True)
treated_group = st.sidebar.radio("Treated/exposed group", ["Cohort 1", "Cohort 2"], index=0)
adverse = st.sidebar.radio("Outcome interpretation", ["Adverse event", "Beneficial event"], index=0) == "Adverse event"

if mode == "TriNetX MOA files":
    uploads = st.file_uploader("Upload one or more TriNetX MOA CSV files", type=["csv", "txt"], accept_multiple_files=True)
    if uploads:
        parsed = parse_multiple_moa(uploads)
        render_parse_report(parsed.report)
        base = parsed.data.rename(columns={"Cohort 1 N": "Group 1 N", "Cohort 2 N": "Group 2 N", "Cohort 1 Risk": "Risk 1", "Cohort 2 Risk": "Risk 2"})
        base = base[["Outcome", "Group 1 N", "Group 2 N", "Risk 1", "Risk 2"]]
    else:
        base = pd.DataFrame(columns=["Outcome", "Group 1 N", "Group 2 N", "Risk 1", "Risk 2"])
else:
    base = pd.DataFrame({"Outcome": ["Example outcome"], "Group 1 N": [1000], "Group 2 N": [1000], "Risk 1": [0.10], "Risk 2": [0.15]})

st.subheader("1. Confirm or edit risks")
st.caption("Enter risks as proportions, not percentages. Example: enter 0.12 for 12 percent.")
edited = st.data_editor(base, num_rows="dynamic", use_container_width=True)

rows = []
for _, row in edited.iterrows():
    outcome = str(row.get("Outcome", "Outcome")).strip() or "Outcome"
    try:
        n1 = int(float(row.get("Group 1 N")))
        n2 = int(float(row.get("Group 2 N")))
        p1 = float(row.get("Risk 1"))
        p2 = float(row.get("Risk 2"))
    except Exception:
        continue
    if treated_group == "Cohort 1":
        pt, pc = p1, p2
    else:
        pt, pc = p2, p1
    rr = risk_ratio_from_risks(pt, pc)
    rd = risk_difference(pt, pc)
    nnt_label, nnt_value = nnt_nnh_from_rd(rd, adverse_outcome=adverse)
    rows.append({
        "Outcome": outcome,
        "Treated/Exposed": treated_group,
        "Treated Risk": pt,
        "Comparison Risk": pc,
        "Power": two_proportion_power(n1, n2, p1, p2, alpha=alpha, two_sided=two_sided),
        "Risk Ratio": rr,
        "E-value": e_value_from_rr(rr),
        "Risk Difference": rd,
        "NNT/NNH Label": nnt_label,
        "NNT/NNH": nnt_value,
        "Cohen h": cohens_h(pt, pc),
    })

summary = pd.DataFrame(rows)
st.subheader("2. Review metrics")
if summary.empty:
    st.info("No valid rows are available yet.")
else:
    selected = st.selectbox("Select outcome for metric cards", summary["Outcome"].tolist())
    r = summary[summary["Outcome"] == selected].iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Power", "" if pd.isna(r["Power"]) else f"{100 * r['Power']:.1f}%")
    c2.metric("E-value", "" if pd.isna(r["E-value"]) else f"{r['E-value']:.2f}")
    c3.metric(r["NNT/NNH Label"], "∞" if np.isinf(r["NNT/NNH"]) else f"{r['NNT/NNH']:.1f}")
    c4.metric("Cohen h", "" if pd.isna(r["Cohen h"]) else f"{r['Cohen h']:.3f}")
    st.dataframe(summary, hide_index=True, use_container_width=True)
    render_download_block()
    st.download_button("Download interpretation CSV", data=summary.to_csv(index=False).encode("utf-8"), file_name="trinetx_power_evalue_nnt_summary.csv", mime="text/csv")

render_verification_box()

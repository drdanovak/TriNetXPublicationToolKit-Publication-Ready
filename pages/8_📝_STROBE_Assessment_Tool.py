import pandas as pd
import streamlit as st

from toolkit.ui import ToolInfo, configure_page, render_download_block, render_tool_header, render_verification_box, render_workflow

configure_page("STROBE Assessment Tool", "📝")
render_tool_header(ToolInfo(title="STROBE Assessment Tool", icon="📝", purpose="Assess reporting completeness for observational studies using a TriNetX-oriented STROBE checklist.", use_when="You are preparing a manuscript, abstract, poster, or internal methods review.", primary_input="Reviewer judgment based on the draft manuscript and TriNetX study materials.", outputs="Checklist score, gap table, and CSV report."))
render_workflow(["Review each reporting domain.", "Mark each item as complete, partial, not addressed, or not applicable.", "Add reviewer notes for missing methods details.", "Download the checklist and revise the manuscript.", "Reassess before submission."])

items = [
    ("Title/Abstract", "Study design is indicated and the TriNetX data source is named."),
    ("Background", "Scientific rationale and real-world evidence gap are clear."),
    ("Objectives", "Primary exposure, comparator, outcomes, and hypothesis are explicit."),
    ("Setting", "TriNetX network, extraction date, study period, and follow-up window are reported."),
    ("Participants", "Inclusion criteria, exclusions, index date, and washout period are reproducible."),
    ("Variables", "Exposure, comparator, outcomes, covariates, and code sets are defined."),
    ("Bias", "Residual confounding, selection bias, misclassification, and immortal time risks are discussed."),
    ("Study Size", "Cohort sizes before and after matching are reported."),
    ("Quantitative Variables", "Categorization of labs, diagnoses, medications, and continuous variables is explained."),
    ("Statistical Methods", "Matching, balance diagnostics, effect estimates, CI, p-values, and multiplicity plan are described."),
    ("Results: Participants", "Flow from initial query to matched analytic cohorts is reported."),
    ("Results: Descriptive", "Baseline table and post-match SMDs are reported."),
    ("Results: Outcome Data", "Outcome counts, risks, time windows, and missingness are reported."),
    ("Results: Main Results", "Effect estimates are reported with confidence intervals and clinically interpretable absolute risks."),
    ("Discussion", "Interpretation is consistent with observational design and avoids causal overclaiming."),
    ("Limitations", "TriNetX-specific limitations are explicit."),
    ("Funding/Ethics", "Funding, IRB status, data-use constraints, and conflicts are disclosed."),
]

rows = []
st.subheader("1. Complete checklist")
for domain, prompt in items:
    cols = st.columns([1.3, 2.7, 1.4, 2.6])
    cols[0].markdown(f"**{domain}**")
    cols[1].write(prompt)
    status = cols[2].selectbox("Status", ["Complete", "Partial", "Not addressed", "Not applicable"], key=domain)
    note = cols[3].text_input("Notes", key=f"note_{domain}")
    rows.append({"Domain": domain, "Item": prompt, "Status": status, "Notes": note})

report = pd.DataFrame(rows)
scoreable = report[report["Status"] != "Not applicable"]
score = (scoreable["Status"].eq("Complete").sum() + 0.5 * scoreable["Status"].eq("Partial").sum()) / max(len(scoreable), 1)

st.subheader("2. Summary")
st.metric("Checklist completeness", f"{100 * score:.1f}%")
st.dataframe(report, hide_index=True, use_container_width=True)
render_download_block()
st.download_button("Download STROBE review CSV", data=report.to_csv(index=False).encode("utf-8"), file_name="trinetx_strobe_assessment.csv", mime="text/csv")
render_verification_box()

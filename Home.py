import pandas as pd
import streamlit as st

from toolkit.ui import configure_page, inject_common_css, render_verification_box, render_workflow

configure_page("TriNetX Publication Toolkit", "📚")
inject_common_css()

st.title("📚 TriNetX Publication Toolkit")
st.caption("A unified publication workflow for converting TriNetX exports into manuscript-ready outputs.")

st.markdown(
    """
This publication-ready version standardizes the interface, parsing, documentation, and export conventions across the toolkit. Use the sidebar to open an individual tool. Start by identifying the output you need, upload the correct TriNetX export, confirm the parsed data, edit labels, preview the output, and verify the final artifact against the original export.
"""
)

st.info(
    "Keep raw TriNetX exports unchanged. Use the toolkit to create cleaned, labeled, publication-facing copies for manuscripts, posters, supplements, and internal methods review."
)

chooser = pd.DataFrame(
    [
        ["Create a Table 1 before and after propensity score matching", "7. PSM Table Generator", "Baseline Patient Characteristics CSV"],
        ["Assess covariate balance after matching", "6. Love Plot Generator", "Baseline Patient Characteristics CSV"],
        ["Create a Table 2-style outcomes table", "9. Outcomes Table Generator", "MOA or Kaplan-Meier CSV"],
        ["Create a forest plot of RR, OR, or HR estimates", "4. Forest Plot Generator", "MOA or prepared estimate table"],
        ["Graph absolute risks for two cohorts", "5. Two-Cohort Outcome Bar Graphs", "MOA CSV or manual risk table"],
        ["Create a Kaplan-Meier survival curve", "3. Kaplan-Meier Curve Maker", "Kaplan-Meier CSV"],
        ["Convert ratios into approximate standardized effect summaries", "1. Effect Size Calculator", "Manual ratio, CI, and p-value entry"],
        ["Estimate power, E-values, risk differences, and NNT/NNH", "2. Power, E-value, and NNT/NNH", "MOA CSV or manual risk table"],
        ["Correct p-values across many tested outcomes", "10. Multiple Comparisons Correction Tool", "MOA CSV or manual p-value table"],
        ["Check STROBE reporting completeness", "8. STROBE Assessment Tool", "Manuscript draft and reviewer judgment"],
    ],
    columns=["Goal", "Use this tool", "Primary input"],
)

st.markdown("### Quick tool chooser")
st.dataframe(chooser, hide_index=True, use_container_width=True)

render_workflow()

st.markdown("### Export guide")
exports = pd.DataFrame(
    [
        ["Baseline Patient Characteristics CSV", "Table 1 and balance diagnostics", "PSM Table Generator; Love Plot Generator"],
        ["Measures of Association CSV", "Risks, RR/OR, p-values, bar graphs, outcome tables, multiplicity corrections", "Outcomes Table; Forest Plot; Bar Graphs; Multiple Comparisons; Power/E-value/NNT"],
        ["Kaplan-Meier CSV", "Survival curves, HRs, log-rank p-values, time-to-event summaries", "Kaplan-Meier Curve; Outcomes Table; Forest Plot"],
        ["Prepared manual table", "Curated values from other reviewed analyses", "Effect Size; Forest Plot; Multiple Comparisons"],
    ],
    columns=["TriNetX export", "Use for", "Compatible tools"],
)
st.table(exports)

st.markdown("### Common troubleshooting checks")
st.write("Upload fails or fields are blank: confirm that the file contains expected section labels such as Cohort Statistics, Risk Difference, Risk Ratio, Hazard Ratio, Log-Rank Test, or Characteristic ID.")
st.write("Cohort direction seems reversed: check whether Cohort 1 or Cohort 2 is the exposure group before interpreting ratios, risk differences, E-values, or NNT/NNH.")
st.write("Figure is too crowded: shorten labels, add section headers, reduce displayed rows, or increase figure size.")

render_verification_box()

st.markdown("### Suggested methods language")
st.write(
    "Figures and tables were prepared from TriNetX Analytics exports using the TriNetX Publication Toolkit, a Streamlit-based set of utilities for formatting real-world data outputs into manuscript-ready tables, plots, and reporting diagnostics."
)

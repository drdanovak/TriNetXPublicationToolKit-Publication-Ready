from __future__ import annotations

from pathlib import Path
from typing import Dict

import streamlit as st

STANDARD_STEPS = [
    "Upload the required TriNetX export in the main page area, or use manual entry when the tool explicitly supports it.",
    "Confirm that the detected fields, parsed rows, cohort direction, and warnings match the original export.",
    "Configure cohort labels, outcome labels, statistic type, ordering, plot/table formatting, and manuscript options.",
    "Preview the generated table, diagnostic, graph, or checklist inside Streamlit before downloading.",
    "Export the manuscript-ready CSV, PNG, HTML, DOCX, or Word-compatible output supported by the tool.",
    "Verify every downloaded value against the original TriNetX export before using it in a manuscript, poster, or supplement.",
]

TOOL_GUIDANCE: Dict[str, Dict[str, str]] = {
    "Home.py": {
        "tool": "Toolkit home",
        "purpose": "Choose the correct TriNetX publication tool and identify the export needed for each manuscript-facing output.",
        "input": "No data upload is needed on the home page.",
        "manual": "Not applicable.",
        "output": "Navigation guidance, export guidance, and workflow instructions.",
    },
    "Effect_Size_Calculator": {
        "tool": "Ratio Effect Size and Forest Plot Tool",
        "purpose": "Convert ratio estimates into approximate standardized effect-size summaries and forest-plot-ready rows.",
        "input": "Manual entry of risk ratios, odds ratios, hazard ratios, confidence intervals, and p-values from reviewed outputs.",
        "manual": "Supported. Enter one row per outcome, subgroup, or sensitivity analysis.",
        "output": "Approximate standardized effect summaries and forest-plot-ready tables.",
    },
    "Power & Sample Size Adequacy Calculator": {
        "tool": "Outcome Interpretation Tool",
        "purpose": "Contextualize TriNetX outcome comparisons with power, E-values, absolute risk differences, and NNT/NNH.",
        "input": "TriNetX Measures of Association CSV or manual event/risk inputs, depending on the selected mode.",
        "manual": "Supported. Use manual mode when the export format is unavailable or when checking a single contrast.",
        "output": "Power, E-value, absolute risk difference, NNT/NNH, and interpretive summaries.",
    },
    "Kaplan_Meier_Curve_Maker": {
        "tool": "Kaplan-Meier Curve Generator",
        "purpose": "Create publication-ready time-to-event curves from TriNetX Kaplan-Meier exports.",
        "input": "TriNetX Kaplan-Meier CSV export.",
        "manual": "Not supported. Use the exported KM table to preserve time points and cohort survival probabilities.",
        "output": "Publication-ready Kaplan-Meier figure and image download.",
    },
    "Forest_Plot_Generator": {
        "tool": "Effect Estimate Forest Plot Generator",
        "purpose": "Generate forest plots for RR, OR, HR, or other ratio estimates across outcomes, cohorts, or subgroups.",
        "input": "TriNetX Measures of Association files, Kaplan-Meier summaries, or manual estimates depending on selected input mode.",
        "manual": "Supported for curated estimates, subgroup summaries, or estimates drawn from several source files.",
        "output": "Forest plot and editable estimate table.",
    },
    "Two-Cohort Outcome Bar Graphs": {
        "tool": "Two-Cohort Outcome Bar Chart Generator",
        "purpose": "Visualize absolute outcome risks for two cohorts to complement relative effect estimates.",
        "input": "TriNetX Measures of Association CSV or manual cohort risk table, depending on selected mode.",
        "manual": "Supported. Enter absolute risks as proportions or percentages according to the on-page instructions.",
        "output": "Two-cohort absolute-risk graph and source table.",
    },
    "Love_Plot_Generator": {
        "tool": "Covariate Balance Love Plot Generator",
        "purpose": "Evaluate and communicate covariate balance before and after propensity score matching.",
        "input": "TriNetX Baseline Patient Characteristics CSV with before/after standardized mean differences.",
        "manual": "Not primary. Upload the baseline export, then edit ordering, grouping, display labels, and plot settings in the interface.",
        "output": "Love plot, balance metrics, sample-retention diagnostics, variance-ratio diagnostics, and narrative balance summary.",
    },
    "PSM_Table_Generator": {
        "tool": "Baseline Table 1 Generator",
        "purpose": "Create a journal-style Table 1 from TriNetX baseline characteristics before and after propensity score matching.",
        "input": "TriNetX Baseline Patient Characteristics CSV.",
        "manual": "Not primary. Upload the baseline export, then edit labels, sections, ordering, and final table text inside the app.",
        "output": "Journal-style Table 1 with before/after matching columns and DOCX/HTML/CSV exports.",
    },
    "STROBE_Assessment_Tool": {
        "tool": "STROBE Reporting Checklist",
        "purpose": "Assess reporting completeness for observational TriNetX studies before submission.",
        "input": "Manual checklist review based on the manuscript draft, methods notes, and TriNetX study design.",
        "manual": "Supported. Mark each item and add comments for revision.",
        "output": "STROBE completeness score and checklist export.",
    },
    "Outcomes_Table_Generator": {
        "tool": "Outcomes Table Generator",
        "purpose": "Convert TriNetX outcome exports into manuscript-ready outcome tables with counts, risks, estimates, CIs, and p-values.",
        "input": "TriNetX Measures of Association and/or Kaplan-Meier CSV exports, depending on selected options.",
        "manual": "Limited. Upload is preferred; use in-app editing to clean labels and final table wording.",
        "output": "Manuscript-ready outcome table with counts, risks, estimates, confidence intervals, and p-values.",
    },
    "Multiple_Comparison_Calculator": {
        "tool": "Multiple Comparisons Correction Tool",
        "purpose": "Apply transparent multiplicity corrections to families of TriNetX outcome p-values.",
        "input": "TriNetX Measures of Association CSV files or manually entered p-values.",
        "manual": "Supported. Use manual entry when p-values come from several exports or a prespecified outcome family.",
        "output": "Adjusted p-value table using Bonferroni, Holm, and false-discovery-rate approaches.",
    },
}


def _guidance_for_path(path_like: str) -> Dict[str, str]:
    name = Path(path_like).name
    for key, value in TOOL_GUIDANCE.items():
        if key == name or key in name:
            return value
    return {
        "tool": name.replace("_", " ").replace(".py", ""),
        "purpose": "Create a publication-facing table, figure, diagnostic, or reporting aid from TriNetX outputs.",
        "input": "Use the main page upload area to upload the appropriate TriNetX export or enter values manually when supported.",
        "manual": "See the tool-specific controls for manual-entry availability.",
        "output": "Download the generated table, figure, or diagnostic output and verify it against the source export.",
    }


def render_standard_tool_instructions(path_like: str) -> None:
    """Render a visible, shared instruction block near the top of every app page.

    Streamlit rebuilds the page on every interaction, so this function must render
    every run. Do not gate this behind session_state; otherwise the instructions
    appear once and then disappear after the next widget interaction or rerun.
    """
    guidance = _guidance_for_path(path_like)
    st.markdown("### Purpose")
    st.info(guidance["purpose"])
    st.markdown("### How to use this tool")
    st.markdown(f"**Input:** {guidance['input']}")
    st.markdown(f"**Manual entry:** {guidance['manual']}")
    st.markdown(f"**Output:** {guidance['output']}")
    with st.expander("Step-by-step workflow", expanded=False):
        for idx, step in enumerate(STANDARD_STEPS, start=1):
            st.markdown(f"{idx}. {step}")
    st.caption(
        "Upload controls are standardized to appear in the main page area. Preserve the raw TriNetX export and verify every manuscript-facing value against the source export."
    )

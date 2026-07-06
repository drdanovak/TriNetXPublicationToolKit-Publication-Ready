from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import streamlit as st

STANDARD_STEPS = [
    "Input: upload the matching TriNetX export or use the manual-entry table when the tool supports manual entry.",
    "Confirm: review detected fields, parsed rows, cohort direction, and any warnings before interpreting output.",
    "Configure: set cohort labels, outcome labels, statistic type, ordering, plot/table formatting, and manuscript options.",
    "Preview: inspect the generated table, diagnostic, graph, or checklist inside Streamlit before downloading.",
    "Export: download manuscript-ready CSV, PNG, HTML, DOCX, or Word-compatible output as supported by the tool.",
    "Verify: compare downloaded values against the original TriNetX export before using the result in a manuscript or poster.",
]

TOOL_GUIDANCE: Dict[str, Dict[str, str]] = {
    "Home.py": {
        "tool": "Toolkit home",
        "input": "No data upload. Use this page to choose the correct tool and TriNetX export.",
        "manual": "Not applicable.",
        "output": "Navigation guidance and workflow instructions.",
    },
    "Effect_Size_Calculator": {
        "tool": "Effect Size Calculator",
        "input": "Manual entry of ratios, confidence intervals, and p-values from reviewed TriNetX outputs or manuscripts.",
        "manual": "Supported. Enter one row per outcome or subgroup.",
        "output": "Approximate standardized effect summaries and forest-plot-ready tables.",
    },
    "Power & Sample Size Adequacy Calculator": {
        "tool": "Power, E-value, and NNT/NNH Tool",
        "input": "TriNetX Measures of Association CSV or manual event/risk inputs, depending on the selected mode.",
        "manual": "Supported. Use manual mode when the export format is unavailable or when checking a single contrast.",
        "output": "Power, E-value, absolute risk difference, NNT/NNH, and interpretive summaries.",
    },
    "Kaplan_Meier_Curve_Maker": {
        "tool": "Kaplan-Meier Curve Maker",
        "input": "TriNetX Kaplan-Meier CSV export.",
        "manual": "Not supported. Use the exported KM table to preserve time points and cohort survival probabilities.",
        "output": "Publication-ready Kaplan-Meier figure and image download.",
    },
    "Forest_Plot_Generator": {
        "tool": "Forest Plot Generator",
        "input": "TriNetX Measures of Association files, Kaplan-Meier summaries, or manual estimates depending on selected input mode.",
        "manual": "Supported for curated estimates. Use manual mode for estimates from heterogeneous sources or edited subgroup labels.",
        "output": "Forest plot and editable estimate table.",
    },
    "Two-Cohort Outcome Bar Graphs": {
        "tool": "Two-Cohort Outcome Bar Graphs",
        "input": "TriNetX Measures of Association CSV or manual cohort risk table, depending on selected mode.",
        "manual": "Supported. Enter absolute risks as proportions or percentages according to the on-page instructions.",
        "output": "Two-cohort absolute-risk graph and source table.",
    },
    "Love_Plot_Generator": {
        "tool": "Love Plot Generator",
        "input": "TriNetX Baseline Patient Characteristics CSV with before/after standardized mean differences.",
        "manual": "Not primary. Use the uploaded baseline export; then edit ordering, grouping, display labels, and plot settings in the interface.",
        "output": "Love plot, balance metrics, sample-retention diagnostics, variance-ratio diagnostics, and narrative balance summary.",
    },
    "PSM_Table_Generator": {
        "tool": "PSM Table Generator",
        "input": "TriNetX Baseline Patient Characteristics CSV.",
        "manual": "Not primary. Use the uploaded baseline export; then edit labels, sections, ordering, and final table text inside the app.",
        "output": "Journal-style Table 1 with before/after matching columns and DOCX/HTML/CSV exports.",
    },
    "STROBE_Assessment_Tool": {
        "tool": "STROBE Assessment Tool",
        "input": "Manual checklist review based on the manuscript draft, methods notes, and TriNetX study design.",
        "manual": "Supported. Mark each item and add comments for revision.",
        "output": "STROBE completeness score and checklist export.",
    },
    "Outcomes_Table_Generator": {
        "tool": "Outcomes Table Generator",
        "input": "TriNetX Measures of Association and/or Kaplan-Meier CSV exports, depending on selected options.",
        "manual": "Limited. Upload is preferred; use in-app editing to clean labels and final table wording.",
        "output": "Manuscript-ready outcome table with counts, risks, estimates, confidence intervals, and p-values.",
    },
    "Multiple_Comparison_Calculator": {
        "tool": "Multiple Comparisons Correction Tool",
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
        "input": "Use the input area to upload the appropriate TriNetX export or enter values manually when supported.",
        "manual": "See the tool-specific controls for manual-entry availability.",
        "output": "Download the generated table, figure, or diagnostic output and verify it against the source export.",
    }


def render_standard_tool_instructions(path_like: str) -> None:
    """Render a non-destructive, shared instruction block near the top of every app page."""
    guidance = _guidance_for_path(path_like)
    with st.expander("Standard toolkit instructions", expanded=False):
        st.markdown(f"**Tool:** {guidance['tool']}")
        st.markdown(f"**Input standard:** {guidance['input']}")
        st.markdown(f"**Manual-entry standard:** {guidance['manual']}")
        st.markdown(f"**Expected output:** {guidance['output']}")
        st.markdown("**Shared workflow:**")
        for idx, step in enumerate(STANDARD_STEPS, start=1):
            st.markdown(f"{idx}. {step}")
        st.info("For all tools: preserve the raw TriNetX export, edit only derived outputs, and verify every manuscript-facing value against the source export.")

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import pandas as pd
import streamlit as st


@dataclass(frozen=True)
class ToolInfo:
    title: str
    icon: str
    purpose: str
    use_when: str
    primary_input: str
    outputs: str
    caution: str = "Verify all generated outputs against the original TriNetX export before manuscript submission."


DEFAULT_WORKFLOW = [
    "Upload or enter data.",
    "Confirm detected export type, fields, and parse warnings.",
    "Edit labels, cohort names, row order, sections, and settings.",
    "Preview the table, figure, or diagnostic output.",
    "Download the output in the appropriate manuscript-ready format.",
    "Verify the final output against the original TriNetX export.",
]


def configure_page(title: str, icon: str = "📚", layout: str = "wide") -> None:
    st.set_page_config(page_title=title, page_icon=icon, layout=layout, initial_sidebar_state="expanded")


def inject_common_css() -> None:
    st.markdown(
        """
<style>
.block-container {padding-top: 2rem; padding-bottom: 3rem;}
.tool-card {border: 1px solid #d0d7de; border-radius: 16px; padding: 1rem 1.1rem; background: #f8fafc; margin-bottom: .8rem;}
.tool-card b {color: #111827;}
.verify-box {border-left: 5px solid #8b5cf6; background: #f5f3ff; padding: .85rem 1rem; border-radius: 8px;}
.small-note {font-size: .9rem; color: #475569;}
</style>
        """,
        unsafe_allow_html=True,
    )


def render_tool_header(info: ToolInfo) -> None:
    inject_common_css()
    st.title(f"{info.icon} {info.title}")
    st.caption(info.purpose)
    st.markdown(
        f"""
<div class="tool-card">
<b>Use when:</b> {info.use_when}<br>
<b>Primary input:</b> {info.primary_input}<br>
<b>Outputs:</b> {info.outputs}
</div>
        """,
        unsafe_allow_html=True,
    )
    st.info(info.caution)


def render_workflow(steps: Sequence[str] | None = None) -> None:
    steps = list(steps or DEFAULT_WORKFLOW)
    st.markdown("### Standard workflow")
    for i, step in enumerate(steps, start=1):
        st.write(f"{i}. {step}")


def render_parse_report(report: dict | None) -> None:
    if not report:
        return
    status = report.get("status", "Parsed")
    warnings = report.get("warnings", []) or []
    with st.expander("Parse report", expanded=bool(warnings)):
        st.write({k: v for k, v in report.items() if k != "warnings"})
        if warnings:
            for warning in warnings:
                st.warning(warning)
        else:
            st.success(status)


def render_download_block(title: str = "Download outputs") -> None:
    st.markdown(f"### {title}")
    st.caption("Download files use explicit names and should be verified against the source TriNetX export.")


def render_verification_box() -> None:
    st.markdown(
        """
<div class="verify-box">
<b>Verification reminder:</b> Compare final counts, risks, effect estimates, confidence intervals, p-values, and labels against the original TriNetX export before adding the output to a manuscript, poster, or supplement.
</div>
        """,
        unsafe_allow_html=True,
    )


def show_dataframe(df: pd.DataFrame, height: int | None = None) -> None:
    st.dataframe(df, hide_index=True, use_container_width=True, height=height)


def sidebar_standard_sections(include_analysis: bool = True) -> None:
    st.sidebar.markdown("## Input")
    st.sidebar.caption("Upload the source export or enter values manually.")
    if include_analysis:
        st.sidebar.markdown("## Analysis settings")
    st.sidebar.markdown("## Formatting")
    st.sidebar.caption("Use consistent labels and export settings across toolkit pages.")

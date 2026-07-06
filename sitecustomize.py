"""Runtime interface standardization for the TriNetX Publication Toolkit.

Python imports this module automatically when the repository root is on sys.path.
It keeps the original app logic, parsers, downloads, and settings in place while
normalizing Streamlit-facing tool names and moving sidebar upload widgets into
the main page area.
"""

from __future__ import annotations

import inspect
from pathlib import Path
from typing import Any

TITLE_REPLACEMENTS = {
    "Novak's TriNetX Effect Size Calculator and Forest Plot Generator": "Ratio Effect Size and Forest Plot Tool",
    "TriNetX Effect Size Calculator and Forest Plot Generator": "Ratio Effect Size and Forest Plot Tool",
    "Novak’s TriNetX Effect Size Calculator and Forest Plot Generator": "Ratio Effect Size and Forest Plot Tool",
    "TriNetX Outcomes: Power, E-value, NNT/NNH, and Standardized Effect Size": "Outcome Interpretation Tool",
    "Novak's TriNetX Kaplan-Meier Survival Curve Viewer": "Kaplan-Meier Curve Generator",
    "TriNetX Kaplan-Meier Survival Curve Viewer": "Kaplan-Meier Curve Generator",
    "🌲 Novak's TriNetX Forest Plot Generator": "Effect Estimate Forest Plot Generator",
    "Novak's TriNetX Forest Plot Generator": "Effect Estimate Forest Plot Generator",
    "TriNetX Forest Plot Generator": "Effect Estimate Forest Plot Generator",
    "2-Cohort Outcome Bar Chart": "Two-Cohort Outcome Bar Chart Generator",
    "Two-Cohort Outcome Bar Chart": "Two-Cohort Outcome Bar Chart Generator",
    "TriNetX Love Plot Generator": "Covariate Balance Love Plot Generator",
    "TriNetX Table 1 Generator": "Baseline Table 1 Generator",
    "TriNetX Baseline Patient Characteristics → Journal-Style Table 1": "Baseline Table 1 Generator",
    "STROBE Self-Assessment": "STROBE Reporting Checklist",
    "📝 STROBE Self-Assessment Tool for TriNetX Projects": "STROBE Reporting Checklist",
    "Novak's TriNetX Outcomes Table 2 Generator": "Outcomes Table Generator",
    "TriNetX Outcomes Table 2 Generator": "Outcomes Table Generator",
    "TriNetX Multiple Comparisons Correction Tool": "Multiple Comparisons Correction Tool",
}


def _standardize_title_text(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    cleaned = value.replace("Novak's ", "").replace("Novak’s ", "")
    cleaned = TITLE_REPLACEMENTS.get(value, TITLE_REPLACEMENTS.get(cleaned, cleaned))
    return cleaned


def _find_calling_app_file() -> str:
    for frame in inspect.stack():
        path = Path(frame.filename)
        if path.name == "Home.py" or path.parent.name == "pages":
            return str(path)
    return "Home.py"


def _patch_streamlit_names() -> None:
    try:
        import streamlit as st
    except Exception:
        return

    if not getattr(st, "_trinetx_standard_title_patched", False):
        original_title = st.title

        def standardized_title(body, *args, **kwargs):
            return original_title(_standardize_title_text(body), *args, **kwargs)

        st.title = standardized_title
        st._trinetx_standard_title_patched = True

    if not getattr(st, "_trinetx_standard_page_config_patched", False):
        original_set_page_config = st.set_page_config

        def standardized_set_page_config(*args, **kwargs):
            if "page_title" in kwargs:
                kwargs["page_title"] = _standardize_title_text(kwargs["page_title"])
            return original_set_page_config(*args, **kwargs)

        st.set_page_config = standardized_set_page_config
        st._trinetx_standard_page_config_patched = True


def _patch_sidebar_uploaders() -> None:
    try:
        import streamlit as st
    except Exception:
        return

    if getattr(st, "_trinetx_standard_upload_patched", False):
        return

    try:
        original_sidebar_file_uploader = st.sidebar.file_uploader
    except Exception:
        return

    def main_area_file_uploader(label, *args, **kwargs):
        try:
            app_file = _find_calling_app_file()
            key = "_trinetx_upload_header_rendered_" + Path(app_file).name + "_" + str(label)
            if not st.session_state.get(key, False):
                st.markdown("### Upload source file")
                st.caption(
                    "Uploads are standardized in the main page area so users can start every tool from the same location. "
                    "Sidebar controls remain reserved for configuration and formatting options."
                )
                st.session_state[key] = True
            return st.file_uploader(label, *args, **kwargs)
        except Exception:
            return original_sidebar_file_uploader(label, *args, **kwargs)

    try:
        st.sidebar.file_uploader = main_area_file_uploader
        st._trinetx_standard_upload_patched = True
    except Exception:
        pass


_patch_streamlit_names()
_patch_sidebar_uploaders()

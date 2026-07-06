"""Runtime interface standardization for the TriNetX Publication Toolkit.

Python imports this module automatically when the repository root is on sys.path.
It adds a shared purpose/instruction header after the first Streamlit title on each page
and redirects sidebar upload widgets into the main page area. This preserves the
original app logic, parsers, downloads, and settings while standardizing the user
experience across tools.
"""

from __future__ import annotations

import inspect
from pathlib import Path


def _find_calling_app_file() -> str:
    for frame in inspect.stack():
        path = Path(frame.filename)
        if path.name == "Home.py" or path.parent.name == "pages":
            return str(path)
    return "Home.py"


def _patch_streamlit_title() -> None:
    try:
        import streamlit as st
    except Exception:
        return

    if getattr(st, "_trinetx_standard_title_patched", False):
        return

    original_title = st.title

    def standardized_title(*args, **kwargs):
        result = original_title(*args, **kwargs)
        try:
            from toolkit.interface_guidance import render_standard_tool_instructions

            app_file = _find_calling_app_file()
            key = "_trinetx_standard_instructions_rendered_" + Path(app_file).name
            if not st.session_state.get(key, False):
                render_standard_tool_instructions(app_file)
                st.session_state[key] = True
        except Exception:
            # Never allow shared guidance to interfere with the original tools.
            pass
        return result

    st.title = standardized_title
    st._trinetx_standard_title_patched = True


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
                st.caption("Uploads are standardized in the main page area so users can start every tool from the same location. Sidebar controls remain reserved for configuration and formatting options.")
                st.session_state[key] = True
            return st.file_uploader(label, *args, **kwargs)
        except Exception:
            return original_sidebar_file_uploader(label, *args, **kwargs)

    try:
        st.sidebar.file_uploader = main_area_file_uploader
        st._trinetx_standard_upload_patched = True
    except Exception:
        pass


_patch_streamlit_title()
_patch_sidebar_uploaders()

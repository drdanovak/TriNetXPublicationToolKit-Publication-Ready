"""Runtime interface standardization for the TriNetX Publication Toolkit.

Python imports this module automatically when the repository root is on sys.path.
It adds a shared instruction expander after the first Streamlit title on each page
without changing the original app logic, parsers, uploads, downloads, or settings.
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


_patch_streamlit_title()

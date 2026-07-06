# Contributing

Thank you for improving the TriNetX Publication Toolkit.

## Development principles

1. Keep raw TriNetX exports unchanged.
2. Use synthetic data in examples and tests.
3. Preserve a common interface across all pages.
4. Add parser tests when changing file-ingestion logic.
5. Document any statistical assumptions in the relevant page and in `docs/methods_and_limitations.md`.

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run Home.py
pytest
```

## Pull request checklist

- The page uses `toolkit.ui.configure_page` and `toolkit.ui.render_tool_header`.
- The workflow is numbered as upload, confirm, edit, preview, download, verify.
- The parser returns a parse report with warnings rather than failing silently.
- Downloads use clear file names and indicate the file type.
- No patient-level data or real TriNetX exports are committed.

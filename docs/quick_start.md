# Quick Start

## Install

```bash
git clone https://github.com/drdanovak/TriNetXPublicationToolKit-Publication-Ready.git
cd TriNetXPublicationToolKit-Publication-Ready
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run Home.py
```

On Windows, activate the environment with:

```bash
.venv\\Scripts\\activate
```

## Recommended workflow

1. Export the relevant TriNetX files.
2. Keep the raw exports unchanged.
3. Upload the export to the matching toolkit page.
4. Review the parse report and detected fields.
5. Edit outcome names, cohort names, row order, section headings, and formatting.
6. Download the output as CSV, HTML, Word-compatible document, or PNG.
7. Verify the final output against the original TriNetX export before manuscript use.

## Example data

The `examples/` directory contains synthetic files that mimic common TriNetX export structure. These are for testing and demonstration only.

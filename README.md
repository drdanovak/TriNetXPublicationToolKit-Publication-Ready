# TriNetX Publication Toolkit

A publication-ready Streamlit toolkit for converting TriNetX Analytics exports into manuscript-ready tables, figures, interpretation aids, and reporting checks.

## Purpose

The TriNetX Publication Toolkit is designed for clinical informatics, real-world evidence, and observational epidemiology teams that use TriNetX Analytics exports. It standardizes a workflow from raw TriNetX CSV files to publication-facing artifacts, including baseline characteristic tables, covariate-balance Love plots, outcome tables, Kaplan-Meier curves, forest plots, absolute-risk bar charts, multiplicity corrections, sensitivity metrics, and STROBE reporting checks.

## What is improved in this publication-ready version

This version consolidates the earlier toolkit into a more coherent software product:

- A common Streamlit interface across all tools.
- Clear, standardized tool names without author-branded labels.
- Shared UI components for headers, workflow steps, cautions, export blocks, and verification reminders.
- Shared parsers for TriNetX Measures of Association, Kaplan-Meier, and Baseline Patient Characteristics exports.
- Consistent page configuration, sidebar organization, terminology, and download naming conventions.
- More defensive file parsing and clearer parse reports.
- A corrected effect-size plotting workflow: ratio-scale plots use a null line at 1.0; standardized log-ratio summaries use a null value of 0.0.
- Robust Kaplan-Meier error handling when expected columns or section headers are absent.
- Documentation, example synthetic exports, a license, citation metadata, contribution guidance, and tests.

## Tools

1. Ratio Effect Size and Forest Plot Tool
2. Outcome Interpretation Tool
3. Kaplan-Meier Curve Generator
4. Effect Estimate Forest Plot Generator
5. Two-Cohort Outcome Bar Chart Generator
6. Covariate Balance Love Plot Generator
7. Baseline Table 1 Generator
8. STROBE Reporting Checklist
9. Outcomes Table Generator
10. Multiple Comparisons Correction Tool

## Quick start

Install dependencies with `pip install -r requirements.txt`, then run `streamlit run Home.py` from the repository root.

## Expected inputs

The toolkit is designed around three common TriNetX export families:

- Baseline Patient Characteristics CSV files for Table 1 and covariate-balance diagnostics.
- Measures of Association CSV files for outcome tables, forest plots, bar graphs, multiplicity corrections, and interpretive metrics.
- Kaplan-Meier CSV files for time-to-event curves, hazard-ratio summaries, and outcome tables.

Synthetic examples are available in `examples/`. These files are not real patient data.

## Verification principle

All generated tables and figures should be checked against the original TriNetX export before manuscript submission. This toolkit formats and contextualizes exported data; it does not replace cohort-design review, statistical review, IRB review, or journal-specific reporting requirements.

## Documentation

- `docs/quick_start.md`
- `docs/export_guide.md`
- `docs/methods_and_limitations.md`
- `docs/publication_checklist.md`

## Testing

Run `pytest` from the repository root.

## License

MIT License. See `LICENSE`.

## Suggested citation

TriNetX Publication Toolkit: A Streamlit-based workflow for converting TriNetX exports into manuscript-ready real-world evidence outputs. Version 1.0.0.

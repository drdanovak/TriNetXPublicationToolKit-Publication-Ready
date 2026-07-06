# Release Notes: v1.0.0

This initial publication-ready release converts the earlier collection of TriNetX helper apps into a more coherent toolkit.

## Interface standardization

All pages now use shared Streamlit UI helpers for page configuration, tool headers, workflow steps, parse reports, download sections, and verification reminders.

## Parser standardization

The repository includes shared parsers for TriNetX Measures of Association, Kaplan-Meier, and Baseline Patient Characteristics exports. Parsers return structured data and parse reports with warnings.

## Implemented fixes

- Corrected effect-size plotting semantics by using a null line of 1.0 for ratio-scale plots and 0.0 for standardized log-ratio plots.
- Rebuilt the Kaplan-Meier curve maker with defensive parsing, explicit upload handling, clear errors, editable labels, and 300 DPI export.
- Removed page titles that over-emphasized individual branding and standardized user-facing tool names.
- Replaced center-layout patterns with wide-layout publication workflows.
- Added synthetic examples, tests, documentation, license, citation metadata, and GitHub Actions.

## Verification reminder

Outputs should be verified against the original TriNetX exports before manuscript submission.

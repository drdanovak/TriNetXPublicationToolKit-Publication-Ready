# TriNetX Export Guide

## Baseline Patient Characteristics

Use for:

- PSM Table Generator
- Love Plot Generator

Expected fields include `Characteristic ID`, `Characteristic Name`, `Category`, patient counts, percentages, and before/after standardized mean difference columns.

## Measures of Association

Use for:

- Outcomes Table Generator
- Forest Plot Generator
- Two-Cohort Outcome Bar Graphs
- Multiple Comparisons Correction Tool
- Power, E-value, and NNT/NNH Tool

Expected sections include `Cohort Statistics`, `Risk Difference`, `Risk Ratio`, and optionally `Odds Ratio`.

## Kaplan-Meier

Use for:

- Kaplan-Meier Curve Maker
- Outcomes Table Generator
- Forest Plot Generator

Expected content includes a time column, cohort survival-probability columns, confidence interval columns when available, and optionally hazard ratio, log-rank test, and proportionality sections.

## General advice

Do not edit raw TriNetX exports. Use the toolkit editors to rename outcomes and cohorts. Keep the original export available for verification.

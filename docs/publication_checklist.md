# Publication Readiness Checklist

Use this checklist before submitting a manuscript that uses outputs from the toolkit.

## Repository

- README is complete.
- LICENSE is present.
- CITATION.cff is present.
- Versioned release has been created.
- DOI has been minted through Zenodo or another archive.
- Synthetic examples are included.
- No real patient data or proprietary exports are committed.

## Manuscript

- Study design is named in the title or abstract.
- TriNetX network and data extraction dates are reported.
- Cohort definitions, index date, baseline window, and follow-up window are reported.
- Inclusion and exclusion criteria are reproducible.
- Matching covariates and matching specifications are reported.
- Balance diagnostics are included or described.
- Outcome definitions and time windows are reported.
- Effect estimates, confidence intervals, and p-values are reported consistently.
- Multiplicity strategy is prespecified or justified when many outcomes are tested.
- Limitations include residual confounding, misclassification, selection bias, missingness, and generalizability.

## Toolkit outputs

- Table 1 values match the baseline export.
- Love plot covariates match the matching covariates or explicitly stated display subset.
- Outcome table values match the MOA or KM exports.
- Forest plot estimates and confidence intervals match the source exports.
- Kaplan-Meier axis labels correctly describe survival, event-free probability, or cumulative incidence.
- All figures are exported at 300 DPI or better.

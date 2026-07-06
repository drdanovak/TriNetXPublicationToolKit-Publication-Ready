# Methods and Limitations

## Scope

The toolkit formats and contextualizes TriNetX Analytics exports. It does not independently reproduce TriNetX cohort construction, matching, censoring, or model estimation.

## Propensity score matching

The PSM Table Generator and Love Plot Generator summarize exported baseline balance. Standardized mean differences should be interpreted in relation to the matching strategy, covariate set, and study question. A common threshold is |SMD| < 0.10, but this should not be treated as universal proof of exchangeability.

## Effect estimates

TriNetX Measures of Association exports may contain risk differences, risk ratios, odds ratios, and p-values. Kaplan-Meier exports may contain survival probabilities, hazard ratios, log-rank p-values, and proportionality diagnostics. Avoid mixing RR, OR, and HR estimates without labeling the column clearly.

## Power, E-value, and NNT/NNH

The power calculator uses approximate two-proportion methods. E-values are sensitivity metrics for unmeasured confounding on the risk-ratio scale. NNT/NNH is calculated from absolute risk difference and depends on outcome severity, follow-up duration, and baseline risk.

## Multiple comparisons

Bonferroni and Holm-Bonferroni control the family-wise error rate. Benjamini-Hochberg and Benjamini-Yekutieli control false discovery rate. The user must define the family of tests before interpreting adjusted p-values.

## Verification

Every generated output should be checked against the original TriNetX export. The toolkit is intended to support publication preparation, not replace scientific judgment, statistical consultation, or peer review.

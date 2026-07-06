from __future__ import annotations

import math
from typing import Optional, Tuple

import numpy as np
from scipy.stats import norm
from statsmodels.stats.multitest import multipletests


def safe_float(value) -> Optional[float]:
    try:
        if value is None:
            return None
        text = str(value).strip().replace(",", "").replace("%", "")
        if text == "" or text.lower() in {"nan", "none"}:
            return None
        return float(text)
    except Exception:
        return None


def ratio_to_log_effect(ratio: float) -> Optional[float]:
    value = safe_float(ratio)
    if value is None or value <= 0:
        return None
    return math.log(value) * (math.sqrt(3) / math.pi)


def cohens_h(p1: float, p2: float) -> Optional[float]:
    p1 = safe_float(p1)
    p2 = safe_float(p2)
    if p1 is None or p2 is None or not (0 <= p1 <= 1) or not (0 <= p2 <= 1):
        return None
    return float(2 * np.arcsin(np.sqrt(p1)) - 2 * np.arcsin(np.sqrt(p2)))


def risk_ratio_from_risks(p_exposed: float, p_control: float) -> Optional[float]:
    p_exposed = safe_float(p_exposed)
    p_control = safe_float(p_control)
    if p_exposed is None or p_control is None or p_control <= 0:
        return None
    return float(p_exposed / p_control)


def e_value_from_rr(rr: float) -> Optional[float]:
    rr = safe_float(rr)
    if rr is None or rr <= 0:
        return None
    rr_use = rr if rr >= 1 else 1 / rr
    if rr_use <= 1:
        return 1.0
    return float(rr_use + math.sqrt(rr_use * (rr_use - 1)))


def risk_difference(p_exposed: float, p_control: float) -> Optional[float]:
    p_exposed = safe_float(p_exposed)
    p_control = safe_float(p_control)
    if p_exposed is None or p_control is None:
        return None
    return float(p_exposed - p_control)


def nnt_nnh_from_rd(rd: float, adverse_outcome: bool = True) -> Tuple[str, Optional[float]]:
    rd = safe_float(rd)
    if rd is None:
        return "NNT/NNH", None
    if abs(rd) < 1e-12:
        return "NNT/NNH", np.inf
    benefit = -rd if adverse_outcome else rd
    if benefit > 0:
        return "NNT", float(1 / benefit)
    return "NNH", float(1 / abs(benefit))


def two_proportion_power(n1: int, n2: int, p1: float, p2: float, alpha: float = 0.05, two_sided: bool = True) -> Optional[float]:
    p1 = safe_float(p1)
    p2 = safe_float(p2)
    if p1 is None or p2 is None or n1 <= 0 or n2 <= 0 or not (0 <= p1 <= 1) or not (0 <= p2 <= 1):
        return None
    if abs(p1 - p2) < 1e-12:
        return 0.0
    p_bar = (p1 * n1 + p2 * n2) / (n1 + n2)
    se = math.sqrt(p_bar * (1 - p_bar) * (1 / n1 + 1 / n2))
    if se <= 0:
        return None
    z_alpha = norm.ppf(1 - alpha / 2 if two_sided else 1 - alpha)
    z = abs(p1 - p2) / se
    if two_sided:
        power = norm.cdf(z - z_alpha) + (1 - norm.cdf(z + z_alpha))
    else:
        power = 1 - norm.cdf(z_alpha - z)
    return float(np.clip(power, 0, 1))


def apply_multiple_comparison_methods(p_values, alpha: float = 0.05):
    methods = {
        "Bonferroni": "bonferroni",
        "Holm-Bonferroni": "holm",
        "Benjamini-Hochberg FDR": "fdr_bh",
        "Benjamini-Yekutieli": "fdr_by",
    }
    output = {}
    p = np.asarray([safe_float(x) for x in p_values], dtype=float)
    for label, method in methods.items():
        reject, adjusted, _, _ = multipletests(p, alpha=alpha, method=method)
        output[label] = {"adjusted_p": adjusted, "reject": reject}
    return output


def fmt_p(value, decimals: int = 3) -> str:
    value = safe_float(value)
    if value is None:
        return ""
    if value < 0.001:
        return "<.001"
    text = f"{value:.{decimals}f}"
    return text[1:] if text.startswith("0.") else text


def fmt_pct(value, decimals: int = 2) -> str:
    value = safe_float(value)
    if value is None:
        return ""
    return f"{100 * value:.{decimals}f}%"

import math

from toolkit.stats import nnt_nnh_from_rd, ratio_to_log_effect, risk_ratio_from_risks


def test_log_effect_null_is_zero():
    assert abs(ratio_to_log_effect(1.0)) < 1e-12


def test_log_effect_direction():
    assert ratio_to_log_effect(0.5) < 0
    assert ratio_to_log_effect(2.0) > 0


def test_risk_ratio():
    assert risk_ratio_from_risks(0.10, 0.20) == 0.5


def test_nnt_for_reduced_adverse_outcome():
    label, value = nnt_nnh_from_rd(-0.05, adverse_outcome=True)
    assert label == "NNT"
    assert math.isclose(value, 20.0)

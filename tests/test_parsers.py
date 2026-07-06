from pathlib import Path

from toolkit.parsers import parse_baseline, parse_km, parse_moa

ROOT = Path(__file__).resolve().parents[1]


def test_parse_moa_example():
    data = (ROOT / "examples" / "synthetic_moa_table.csv").read_bytes()
    result = parse_moa(data, "synthetic_moa_table.csv")
    assert len(result.data) == 1
    assert result.data.loc[0, "Risk Ratio"] == 0.667
    assert result.data.loc[0, "RR p"] == 0.003


def test_parse_km_example():
    data = (ROOT / "examples" / "synthetic_km_table.csv").read_bytes()
    result = parse_km(data, "synthetic_km_table.csv")
    assert len(result.data) >= 3
    assert result.report["time_column"] == "Time"
    assert len(result.report["survival_columns"]) == 2


def test_parse_baseline_example():
    data = (ROOT / "examples" / "synthetic_baseline_characteristics.csv").read_bytes()
    result = parse_baseline(data, "synthetic_baseline_characteristics.csv")
    assert len(result.data) >= 3
    assert result.report["before_smd_column"] is not None
    assert result.report["after_smd_column"] is not None

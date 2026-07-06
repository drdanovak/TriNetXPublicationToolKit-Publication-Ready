from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd


@dataclass
class ParseResult:
    data: pd.DataFrame
    report: Dict[str, Any] = field(default_factory=dict)


def clean_cell(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("\ufeff", "").strip().strip('"').strip()


def norm_text(value: Any) -> str:
    value = clean_cell(value).lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def compact_text(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "", clean_cell(value).lower())


def safe_float(value: Any) -> Optional[float]:
    text = clean_cell(value).replace(",", "").replace("%", "")
    if not text:
        return None
    text = text.replace("−", "-").replace("–", "-").replace("—", "-")
    text = text.strip().lstrip("<>=≤≥ ").rstrip("*†‡;,")
    if text.startswith("."):
        text = "0" + text
    try:
        return float(text)
    except Exception:
        match = re.search(r"[-+]?(?:\d+\.\d+|\d+|\.\d+)(?:[eE][-+]?\d+)?", text)
        if match:
            token = match.group(0)
            try:
                return float("0" + token if token.startswith(".") else token)
            except Exception:
                return None
    return None


def parse_p_value(value: Any) -> Optional[float]:
    parsed = safe_float(value)
    if parsed is not None and 0 <= parsed <= 1:
        return parsed
    return None


def read_csv_rows(file_bytes: bytes) -> List[List[str]]:
    text = file_bytes.decode("utf-8-sig", errors="replace")
    rows = list(csv.reader(io.StringIO(text)))
    return [[clean_cell(cell) for cell in row] for row in rows]


def is_blank_row(row: List[Any]) -> bool:
    return all(clean_cell(cell) == "" for cell in row)


def nonempty_count(row: List[Any]) -> int:
    return sum(1 for cell in row if clean_cell(cell))


KNOWN_SECTION_LABELS = {
    "cohort statistics",
    "risk difference",
    "risk ratio",
    "odds ratio",
    "hazard ratio",
    "log rank test",
    "proportionality",
    "notes",
    "graph data table",
}


def detect_export_type(rows: List[List[str]]) -> str:
    joined = "\n".join(" ".join(clean_cell(cell) for cell in row) for row in rows)
    normalized = norm_text(joined)
    if "baseline patient characteristics" in normalized or "characteristic id" in normalized:
        return "Baseline Patient Characteristics"
    if "kaplan meier" in normalized:
        return "Kaplan-Meier"
    if "measures of association" in normalized:
        return "Measures of Association"
    labels = {norm_text(row[0]) for row in rows if row and nonempty_count(row) == 1}
    if "log rank test" in labels or "hazard ratio" in labels:
        return "Kaplan-Meier"
    if "risk difference" in labels or "risk ratio" in labels or "cohort statistics" in labels:
        return "Measures of Association"
    return "Unknown"


def find_table_after_section(rows: List[List[str]], section_label: str) -> Tuple[List[str], List[List[str]]]:
    wanted = norm_text(section_label)
    start = None
    for idx, row in enumerate(rows):
        if row and norm_text(row[0]) == wanted:
            start = idx
            break
    if start is None:
        return [], []
    header_idx = start + 1
    while header_idx < len(rows) and is_blank_row(rows[header_idx]):
        header_idx += 1
    if header_idx >= len(rows):
        return [], []
    headers = [clean_cell(x) for x in rows[header_idx]]
    data_rows: List[List[str]] = []
    idx = header_idx + 1
    while idx < len(rows):
        row = rows[idx]
        if is_blank_row(row):
            break
        if nonempty_count(row) == 1 and norm_text(row[0]) in KNOWN_SECTION_LABELS:
            break
        data_rows.append([clean_cell(cell) for cell in row])
        idx += 1
    return headers, data_rows


def rows_to_records(headers: List[str], rows: List[List[str]]) -> List[Dict[str, str]]:
    normalized = [norm_text(h) for h in headers]
    records = []
    for row in rows:
        padded = row + [""] * max(0, len(headers) - len(row))
        record: Dict[str, str] = {}
        for raw, norm, value in zip(headers, normalized, padded):
            record[norm] = clean_cell(value)
            record[clean_cell(raw)] = clean_cell(value)
        records.append(record)
    return records


def get_value(record: Dict[str, str], aliases: List[str]) -> str:
    for alias in aliases:
        n = norm_text(alias)
        if n in record:
            return record[n]
        if alias in record:
            return record[alias]
    return ""


def parse_effect_section(rows: List[List[str]], section: str) -> Dict[str, Optional[float]]:
    headers, data = find_table_after_section(rows, section)
    records = rows_to_records(headers, data)
    if not records:
        return {"estimate": None, "lower": None, "upper": None, "p": None}
    record = records[0]
    estimate = safe_float(get_value(record, [section, "estimate", "value", "ratio", "measure"]))
    lower = safe_float(get_value(record, ["95 % CI Lower", "95% CI Lower", "Lower 95% CI", "lower", "lcl"]))
    upper = safe_float(get_value(record, ["95 % CI Upper", "95% CI Upper", "Upper 95% CI", "upper", "ucl"]))
    p_value = parse_p_value(get_value(record, ["p", "p value", "p-value", "p_value"]))
    return {"estimate": estimate, "lower": lower, "upper": upper, "p": p_value}


def parse_cohort_statistics(rows: List[List[str]]) -> Tuple[pd.DataFrame, List[str]]:
    headers, data = find_table_after_section(rows, "Cohort Statistics")
    warnings: List[str] = []
    records = rows_to_records(headers, data)
    out = []
    for record in records[:2]:
        out.append(
            {
                "Cohort": get_value(record, ["Cohort"]),
                "Cohort Name": get_value(record, ["Cohort Name", "CohortName"]),
                "Patients in Cohort": safe_float(get_value(record, ["Patients in Cohort", "N", "Total"])),
                "Patients with Outcome": safe_float(get_value(record, ["Patients with Outcome", "Events", "Outcome Count"])),
                "Risk": safe_float(get_value(record, ["Risk", "Risk %", "Risk Percent"])),
            }
        )
    if len(out) < 2:
        warnings.append("Could not detect two complete Cohort Statistics rows.")
    return pd.DataFrame(out), warnings


def parse_moa(file_bytes: bytes, source_name: str = "uploaded.csv") -> ParseResult:
    rows = read_csv_rows(file_bytes)
    export_type = detect_export_type(rows)
    warnings: List[str] = []
    if export_type not in {"Measures of Association", "Unknown"}:
        warnings.append(f"Detected export type was {export_type}, not Measures of Association.")
    cohort_df, cohort_warnings = parse_cohort_statistics(rows)
    warnings.extend(cohort_warnings)
    risk_difference = parse_effect_section(rows, "Risk Difference")
    risk_ratio = parse_effect_section(rows, "Risk Ratio")
    odds_ratio = parse_effect_section(rows, "Odds Ratio")
    title = next((clean_cell(row[0]) for row in rows if row and clean_cell(row[0])), Path(source_name).stem)
    row = {
        "Outcome": clean_outcome_label(title, source_name),
        "Source File": source_name,
        "Export Type": export_type,
        "Cohort 1 Name": cohort_df.iloc[0].get("Cohort Name", "Cohort 1") if len(cohort_df) > 0 else "Cohort 1",
        "Cohort 2 Name": cohort_df.iloc[1].get("Cohort Name", "Cohort 2") if len(cohort_df) > 1 else "Cohort 2",
        "Cohort 1 N": cohort_df.iloc[0].get("Patients in Cohort", np.nan) if len(cohort_df) > 0 else np.nan,
        "Cohort 2 N": cohort_df.iloc[1].get("Patients in Cohort", np.nan) if len(cohort_df) > 1 else np.nan,
        "Cohort 1 Events": cohort_df.iloc[0].get("Patients with Outcome", np.nan) if len(cohort_df) > 0 else np.nan,
        "Cohort 2 Events": cohort_df.iloc[1].get("Patients with Outcome", np.nan) if len(cohort_df) > 1 else np.nan,
        "Cohort 1 Risk": cohort_df.iloc[0].get("Risk", np.nan) if len(cohort_df) > 0 else np.nan,
        "Cohort 2 Risk": cohort_df.iloc[1].get("Risk", np.nan) if len(cohort_df) > 1 else np.nan,
        "Risk Difference": risk_difference["estimate"],
        "RD Lower CI": risk_difference["lower"],
        "RD Upper CI": risk_difference["upper"],
        "RD p": risk_difference["p"],
        "Risk Ratio": risk_ratio["estimate"],
        "RR Lower CI": risk_ratio["lower"],
        "RR Upper CI": risk_ratio["upper"],
        "RR p": risk_ratio["p"],
        "Odds Ratio": odds_ratio["estimate"],
        "OR Lower CI": odds_ratio["lower"],
        "OR Upper CI": odds_ratio["upper"],
        "OR p": odds_ratio["p"],
    }
    return ParseResult(pd.DataFrame([row]), {"source_file": source_name, "export_type": export_type, "rows_parsed": 1, "warnings": warnings, "status": "Parsed Measures of Association export"})


def clean_outcome_label(title: str, filename: str) -> str:
    title = clean_cell(title)
    title = re.sub(r"\s*Measures of Association Table\s*$", "", title, flags=re.I)
    title = re.sub(r"\s*Kaplan[- ]Meier Table\s*$", "", title, flags=re.I)
    if title and title.lower() != "generated by trinetx":
        return title.strip(" -_")
    stem = Path(filename).stem.replace("_", " ").replace("-", " ")
    stem = re.sub(r"(?i)\b(moa|km|table|graph|result)\b", "", stem)
    return re.sub(r"\s+", " ", stem).strip() or "Outcome"


def parse_km(file_bytes: bytes, source_name: str = "uploaded.csv") -> ParseResult:
    text = file_bytes.decode("utf-8-sig", errors="replace")
    lines = text.splitlines()
    warnings: List[str] = []
    header_idx = None
    for idx, line in enumerate(lines):
        lowered = line.lower()
        if "time" in lowered and "survival" in lowered:
            header_idx = idx
            break
    if header_idx is None:
        raise ValueError("Could not find a Kaplan-Meier data header containing time and survival columns.")
    df = pd.read_csv(io.StringIO("\n".join(lines[header_idx:])))
    df.columns = [clean_cell(c) for c in df.columns]
    time_col = next((c for c in df.columns if "time" in c.lower()), None)
    if time_col is None:
        raise ValueError("Kaplan-Meier table did not contain a time column.")
    survival_cols = [c for c in df.columns if "survival probability" in c.lower() and "ci" not in c.lower()]
    if len(survival_cols) < 2:
        raise ValueError("Kaplan-Meier table must contain survival probability columns for two cohorts.")
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=[time_col]).sort_values(time_col).reset_index(drop=True)
    for col in survival_cols:
        df[col] = df[col].ffill()
    rows = read_csv_rows(file_bytes)
    hazard = parse_effect_section(rows, "Hazard Ratio")
    logrank = parse_effect_section(rows, "Log-Rank Test")
    report = {
        "source_file": source_name,
        "export_type": "Kaplan-Meier",
        "time_column": time_col,
        "survival_columns": survival_cols[:2],
        "hazard_ratio": hazard.get("estimate"),
        "log_rank_p": logrank.get("p"),
        "warnings": warnings,
        "status": "Parsed Kaplan-Meier export",
    }
    return ParseResult(df, report)


def parse_baseline(file_bytes: bytes, source_name: str = "baseline.csv") -> ParseResult:
    text = file_bytes.decode("utf-8-sig", errors="replace")
    lines = text.splitlines()
    header_idx = None
    for idx, line in enumerate(lines[:100]):
        try:
            cols = [clean_cell(c) for c in next(csv.reader([line]))]
        except Exception:
            continue
        if {"Characteristic ID", "Characteristic Name", "Category"}.issubset(set(cols)):
            header_idx = idx
            break
    if header_idx is None:
        raise ValueError("Could not find a Baseline Patient Characteristics header row.")
    df = pd.read_csv(io.StringIO("\n".join(lines[header_idx:])))
    df.columns = [clean_cell(c) for c in df.columns]
    warnings: List[str] = []
    required = ["Characteristic ID", "Characteristic Name", "Category"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError("Missing required baseline columns: " + ", ".join(missing))
    for col in df.columns:
        if col not in required:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace("%", "", regex=False).str.replace(",", "", regex=False), errors="ignore")
    before_smd = next((c for c in df.columns if "standardized mean difference" in c.lower() and "before" in c.lower()), None)
    after_smd = next((c for c in df.columns if "standardized mean difference" in c.lower() and "after" in c.lower()), None)
    if before_smd is None or after_smd is None:
        warnings.append("Before and after standardized mean difference columns were not both detected.")
    return ParseResult(df.dropna(how="all").reset_index(drop=True), {"source_file": source_name, "export_type": "Baseline Patient Characteristics", "rows_parsed": int(len(df)), "before_smd_column": before_smd, "after_smd_column": after_smd, "warnings": warnings, "status": "Parsed baseline export"})


def parse_multiple_moa(uploaded_files) -> ParseResult:
    frames = []
    reports = []
    warnings: List[str] = []
    for file in uploaded_files:
        try:
            result = parse_moa(file.getvalue(), file.name)
            frames.append(result.data)
            reports.append(result.report)
            warnings.extend([f"{file.name}: {w}" for w in result.report.get("warnings", [])])
        except Exception as exc:
            warnings.append(f"{file.name}: {exc}")
    data = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    return ParseResult(data, {"files_processed": len(uploaded_files), "rows_parsed": int(len(data)), "warnings": warnings, "status": "Parsed uploaded MOA files"})

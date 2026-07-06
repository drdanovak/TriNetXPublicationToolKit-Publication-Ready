from __future__ import annotations

import html
from typing import Any, List

import pandas as pd


def escape(value: Any) -> str:
    return html.escape("" if value is None else str(value))


def fmt_int(value: Any) -> str:
    try:
        if pd.isna(value):
            return ""
        return f"{int(round(float(value))):,}"
    except Exception:
        return "" if value is None else str(value)


def fmt_float(value: Any, digits: int = 2) -> str:
    try:
        if pd.isna(value):
            return ""
        return f"{float(value):.{digits}f}"
    except Exception:
        return "" if value is None else str(value)


def fmt_percent(value: Any, digits: int = 2, source_is_proportion: bool = True) -> str:
    try:
        if pd.isna(value):
            return ""
        number = float(value)
        if source_is_proportion:
            number *= 100
        return f"{number:.{digits}f}%"
    except Exception:
        return "" if value is None else str(value)


def fmt_ci(point: Any, lower: Any, upper: Any, digits: int = 2) -> str:
    p = fmt_float(point, digits)
    lo = fmt_float(lower, digits)
    hi = fmt_float(upper, digits)
    if p and lo and hi:
        return f"{p} ({lo} to {hi})"
    return p


def dataframe_to_html_table(df: pd.DataFrame, title: str = "", table_class: str = "pub-table") -> str:
    css = """
<style>
.pub-table {border-collapse: collapse; width: 100%; font-family: Arial, sans-serif; font-size: 13px;}
.pub-table th, .pub-table td {border: 1px solid #d0d7de; padding: 6px 8px; vertical-align: top;}
.pub-table th {background: #f3f4f6; font-weight: 700; text-align: center;}
.pub-table td:first-child {text-align: left; font-weight: 600;}
.pub-table td {text-align: right;}
</style>
"""
    title_html = f"<p><strong>{escape(title)}</strong></p>" if title else ""
    parts: List[str] = [css, title_html, f"<table class='{table_class}'>", "<thead><tr>"]
    for col in df.columns:
        parts.append(f"<th>{escape(col)}</th>")
    parts.append("</tr></thead><tbody>")
    for _, row in df.iterrows():
        parts.append("<tr>")
        for col in df.columns:
            parts.append(f"<td>{escape(row[col])}</td>")
        parts.append("</tr>")
    parts.append("</tbody></table>")
    return "".join(parts)


def word_compatible_html(table_html: str, title: str = "TriNetX Toolkit Output") -> str:
    safe_title = escape(title)
    return "<!DOCTYPE html><html><head><meta charset='utf-8'><title>" + safe_title + "</title></head><body>" + table_html + "</body></html>"

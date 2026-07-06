from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "Home.py", *sorted((ROOT / "pages").glob("*.py"))]
MARKER = "render_standard_tool_instructions(__file__)"
IMPORT_LINE = "from toolkit.interface_guidance import render_standard_tool_instructions"


def _insert_header_after_title(text: str) -> tuple[str, bool]:
    if MARKER in text:
        return text, False
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if "st.title(" in line:
            indent = line[: len(line) - len(line.lstrip())]
            snippet = [
                "",
                f"{indent}try:",
                f"{indent}    {IMPORT_LINE}",
                f"{indent}    render_standard_tool_instructions(__file__)",
                f"{indent}except Exception:",
                f"{indent}    pass",
                "",
            ]
            lines[idx + 1:idx + 1] = snippet
            return "\n".join(lines) + "\n", True
    return text, False


def _move_sidebar_uploads_to_main(text: str) -> tuple[str, bool]:
    updated = text.replace("st.sidebar.file_uploader(", "st.file_uploader(")
    return updated, updated != text


def patch_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    updated, changed_header = _insert_header_after_title(original)
    updated, changed_uploads = _move_sidebar_uploads_to_main(updated)
    changed = changed_header or changed_uploads
    if changed:
        path.write_text(updated, encoding="utf-8")
    return changed


def main() -> None:
    changed = []
    for path in TARGETS:
        if path.exists() and patch_file(path):
            changed.append(str(path.relative_to(ROOT)))
    if changed:
        print("Patched files:")
        for item in changed:
            print(f"- {item}")
    else:
        print("No files needed patching.")


if __name__ == "__main__":
    main()

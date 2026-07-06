from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "Home.py", *sorted((ROOT / "pages").glob("*.py"))]
MARKER = "render_standard_tool_instructions(__file__)"


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return False
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if "st.title(" in line:
            indent = line[: len(line) - len(line.lstrip())]
            snippet = [
                "",
                f"{indent}try:",
                f"{indent}    from toolkit.interface_guidance import render_standard_tool_instructions",
                f"{indent}    render_standard_tool_instructions(__file__)",
                f"{indent}except Exception:",
                f"{indent}    pass",
                "",
            ]
            lines[idx + 1:idx + 1] = snippet
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return True
    return False


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

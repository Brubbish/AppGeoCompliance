"""Shared helpers for the software market compliance skill."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

SUPPORTED_MARKETS = ("cn-mainland", "us", "eu")
EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    "coverage",
    ".gradle",
    "Pods",
}
MAX_FILE_BYTES = 2 * 1024 * 1024

TEXT_EXTENSIONS = {
    ".c", ".cc", ".cpp", ".cs", ".css", ".csv", ".go", ".h", ".html",
    ".ini", ".java", ".js", ".jsx", ".json", ".kt", ".md", ".m", ".mm",
    ".plist", ".properties", ".py", ".rb", ".rs", ".swift", ".toml", ".ts",
    ".tsx", ".txt", ".vue", ".xml", ".yaml", ".yml",
}
TEXT_FILENAMES = {
    "AndroidManifest.xml",
    "Info.plist",
    "Podfile",
    "Package.swift",
    "Gemfile",
    "LICENSE",
    "NOTICE",
    "README",
}


@dataclass(frozen=True)
class TextFile:
    path: Path
    relative_path: str
    text: str
    lines: tuple[str, ...]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def iter_text_files(root: Path) -> tuple[list[TextFile], list[dict[str, str]]]:
    """Read small text-like files and record files that could not be inspected."""
    files: list[TextFile] = []
    errors: list[dict[str, str]] = []
    if not root.exists() or not root.is_dir():
        return [], [{"file": str(root), "error": "project root is missing or not a directory"}]

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        try:
            relative = path.relative_to(root)
        except ValueError:
            continue
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        if path.name not in TEXT_FILENAMES and path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                errors.append({"file": str(relative), "error": "file exceeds scan size limit"})
                continue
            raw = path.read_bytes()
            if b"\x00" in raw:
                errors.append({"file": str(relative), "error": "binary content"})
                continue
            text = raw.decode("utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append({"file": str(relative), "error": str(exc)})
            continue
        files.append(TextFile(path, relative.as_posix(), text, tuple(text.splitlines())))
    return files, errors


def read_markets_yaml(path: Path) -> list[str]:
    """Parse the intentionally tiny compliance-input.yaml format."""
    text = path.read_text(encoding="utf-8")
    markets: list[str] = []
    in_markets = False
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if re.match(r"^markets\s*:\s*(?:\[.*\])?\s*$", line):
            in_markets = True
            inline = line.split(":", 1)[1].strip()
            if inline.startswith("[") and inline.endswith("]"):
                markets.extend(item.strip().strip("'\"") for item in inline[1:-1].split(",") if item.strip())
                in_markets = False
            continue
        if in_markets:
            match = re.match(r"^\s*-\s*([^\s#]+)\s*$", line)
            if match:
                markets.append(match.group(1).strip("'\""))
            elif not line.startswith(" ") and not line.startswith("\t"):
                in_markets = False
    return markets


def validate_markets(markets: Iterable[str]) -> list[str]:
    values = [str(item).strip() for item in markets if str(item).strip()]
    unknown = sorted(set(values) - set(SUPPORTED_MARKETS))
    if unknown:
        raise ValueError(f"unknown market(s): {', '.join(unknown)}; choose from {', '.join(SUPPORTED_MARKETS)}")
    if not values:
        raise ValueError("at least one market is required")
    return list(dict.fromkeys(values))


def line_evidence(file: TextFile, line_number: int, width: int = 240) -> dict[str, Any]:
    excerpt = file.lines[line_number - 1].strip() if 0 < line_number <= len(file.lines) else ""
    return {"file": file.relative_path, "line": line_number, "excerpt": excerpt[:width]}


def find_matches(file: TextFile, pattern: str, flags: int = re.IGNORECASE, limit: int = 20) -> list[dict[str, Any]]:
    try:
        regex = re.compile(pattern, flags)
    except re.error:
        return []
    matches: list[dict[str, Any]] = []
    for line_number, line in enumerate(file.lines, start=1):
        if regex.search(line):
            matches.append(line_evidence(file, line_number))
            if len(matches) >= limit:
                break
    return matches


def all_text(files: Iterable[TextFile]) -> str:
    return "\n".join(file.text for file in files)


def contains_any(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE | re.MULTILINE) for pattern in patterns)


def first_evidence(files: Iterable[TextFile], patterns: Iterable[str]) -> dict[str, Any] | None:
    for file in files:
        for pattern in patterns:
            matches = find_matches(file, pattern, limit=1)
            if matches:
                return matches[0]
    return None


def finding(
    *,
    finding_id: str,
    domain: str,
    market: str,
    status: str,
    severity: str,
    title: str,
    facts: list[str] | None = None,
    evidence: list[dict[str, Any]] | None = None,
    why_not_confirmed: list[str] | None = None,
    questions: list[str] | None = None,
    source_ids: list[str] | None = None,
    remediation: str = "",
) -> dict[str, Any]:
    return {
        "id": finding_id,
        "domain": domain,
        "market": market,
        "status": status,
        "severity": severity,
        "title": title,
        "facts": facts or [],
        "evidence": evidence or [],
        "why_not_confirmed": why_not_confirmed or [],
        "questions": questions or [],
        "source_ids": source_ids or [],
        "remediation": remediation,
    }

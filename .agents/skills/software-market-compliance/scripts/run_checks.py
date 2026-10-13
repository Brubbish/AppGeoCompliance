"""Run lightweight candidate scans for software market compliance review."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Callable

from common import TextFile, iter_text_files, read_markets_yaml, validate_markets, write_json
from scan_age import scan as scan_age
from scan_maps import scan as scan_maps
from scan_naming import scan as scan_naming
from scan_regulation import scan as scan_regulation

SKILL_ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ("naming", "regulation", "maps", "age")
STATUS_ORDER = {
    "candidate": 0,
    "scan_incomplete": 1,
    "not_detected": 2,
}
SEVERITY_ORDER = {"blocker": 0, "high": 1, "medium": 2, "low": 3, "info": 4}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check naming, regulatory triggers, maps, and age/child signals for CN, US, and EU releases."
    )
    parser.add_argument("--project-root", default=".", help="Project directory to scan (default: current directory).")
    parser.add_argument(
        "--input",
        default="compliance-input.yaml",
        help="Relative or absolute path to the minimal markets YAML file (default: compliance-input.yaml).",
    )
    parser.add_argument(
        "--markets",
        nargs="+",
        help="Override markets from the input file: cn-mainland, us, eu.",
    )
    parser.add_argument("--format", choices=("markdown", "json", "both"), default="markdown")
    parser.add_argument("--output", help="Write output to this path. Required when --format both is used.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON sent to stdout.")
    return parser


def _resolve_input(project_root: Path, input_value: str) -> Path:
    candidate = Path(input_value)
    return candidate if candidate.is_absolute() else project_root / candidate


def _is_inside(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _filter_product_files(files: list[TextFile], project_root: Path, output_path: Path | None) -> list[TextFile]:
    excluded_files = {
        "compliance-source-registry.md",
        "compliance-input.yaml",
        "compliance-report.md",
        "compliance-report.json",
    }
    result: list[TextFile] = []
    for file in files:
        if _is_inside(file.path, SKILL_ROOT):
            continue
        if file.path.name in excluded_files:
            continue
        if output_path is not None and file.path.resolve() == output_path.resolve():
            continue
        if file.path.name.startswith("compliance-report"):
            continue
        result.append(file)
    return result


def _source_index() -> dict[str, dict[str, Any]]:
    path = SKILL_ROOT / "references" / "source-registry.json"
    records = json.loads(path.read_text(encoding="utf-8"))
    return {record["id"]: record for record in records}


def _scan_incomplete(error: str, file: str = "") -> dict[str, Any]:
    return {
        "id": "SCAN-INCOMPLETE",
        "domain": "scanner",
        "market": "global",
        "status": "scan_incomplete",
        "severity": "medium",
        "title": "Scan could not inspect all requested inputs",
        "facts": [error],
        "evidence": [{"file": file, "line": 0, "excerpt": error}] if file else [],
        "why_not_confirmed": [],
        "questions": [],
        "source_ids": [],
        "remediation": "Make the file readable or provide the requested input, then run the scan again.",
    }


def _not_detected(domain: str, market: str) -> dict[str, Any]:
    return {
        "id": f"{domain.upper()}-NOT-DETECTED",
        "domain": domain,
        "market": market,
        "status": "not_detected",
        "severity": "info",
        "title": f"No scanner candidate detected for {domain}",
        "facts": ["No rule-pattern match was found in readable scanned files."],
        "evidence": [],
        "why_not_confirmed": [],
        "questions": [],
        "source_ids": [],
        "remediation": "The model must still inspect this domain using the code-review checklist.",
    }


def _sort_findings(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        findings,
        key=lambda item: (
            STATUS_ORDER.get(item["status"], 99),
            SEVERITY_ORDER.get(item["severity"], 99),
            item["market"],
            item["id"],
        ),
    )


def run(project_root: Path, markets: list[str], output_path: Path | None = None) -> dict[str, Any]:
    raw_files, read_errors = iter_text_files(project_root)
    files = _filter_product_files(raw_files, project_root, output_path)
    findings: list[dict[str, Any]] = []

    for error in read_errors:
        findings.append(_scan_incomplete(error["error"], error.get("file", "")))

    scanners: list[tuple[str, Callable[[list[TextFile], list[str], Path], list[dict[str, Any]]]]] = [
        ("naming", scan_naming),
        ("regulation", scan_regulation),
        ("maps", scan_maps),
        ("age", scan_age),
    ]
    for domain, scanner in scanners:
        try:
            findings.extend(scanner(files, markets, SKILL_ROOT))
        except Exception as exc:  # Report a partial scan instead of claiming no issue.
            findings.append(_scan_incomplete(f"{domain} scanner failed: {exc}"))

    reported_pairs = {(item["domain"], item["market"]) for item in findings if item["domain"] in DOMAINS}
    for market in markets:
        for domain in DOMAINS:
            if (domain, market) not in reported_pairs:
                findings.append(_not_detected(domain, market))

    findings = _sort_findings(findings)
    source_ids = sorted({source_id for item in findings for source_id in item.get("source_ids", [])})
    index = _source_index()
    sources = [index[source_id] for source_id in source_ids if source_id in index]
    counts = Counter(item["status"] for item in findings)
    return {
        "schema_version": "1.0",
        "skill": "software-market-compliance",
        "project_root": str(project_root),
        "markets": markets,
        "scanned_file_count": len(files),
        "excluded_file_count": len(raw_files) - len(files),
        "findings": findings,
        "sources": sources,
        "summary": {
            "candidate": counts.get("candidate", 0),
            "not_detected": counts.get("not_detected", 0),
            "scan_incomplete": counts.get("scan_incomplete", 0),
        },
        "limitations": [
            "Static scanning reports pattern matches only and does not determine legal, platform, or contract violations.",
            "not_detected means no configured pattern matched readable scanned files; it does not mean the domain was reviewed or compliant.",
            "Country/region naming, boundaries, China map-review scope, service applicability, and age rules require contextual model review and may require developer confirmation."
        ],
    }


def _md(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def _format_sources(source_ids: list[str], source_index: dict[str, dict[str, Any]]) -> str:
    values: list[str] = []
    for source_id in source_ids:
        source = source_index.get(source_id)
        if source:
            values.append(f"[{source_id}]({source['url']})")
        else:
            values.append(source_id)
    return ", ".join(values) or "-"


def _format_section(title: str, findings: list[dict[str, Any]], source_index: dict[str, dict[str, Any]]) -> list[str]:
    lines = [f"## {title}", ""]
    if not findings:
        lines.append("None.")
        lines.append("")
        return lines
    for item in findings:
        lines.extend([
            f"### {item['id']} ({item['market']}, {item['severity']})",
            "",
            item["title"],
            "",
        ])
        if item["facts"]:
            lines.append("**Detected facts**")
            lines.extend(f"- {_md(fact)}" for fact in item["facts"])
            lines.append("")
        if item["evidence"]:
            lines.append("**Evidence**")
            for evidence in item["evidence"]:
                location = evidence.get("file", "unknown file")
                line = evidence.get("line", 0)
                suffix = f":{line}" if line else ""
                lines.append(f"- `{_md(location)}{suffix}`: {_md(evidence.get('excerpt', ''))}")
            lines.append("")
        if item["why_not_confirmed"]:
            lines.append("**Why this is only a candidate**")
            lines.extend(f"- {_md(reason)}" for reason in item["why_not_confirmed"])
            lines.append("")
        if item["questions"]:
            lines.append("**Developer confirmation needed**")
            lines.extend(f"- {_md(question)}" for question in item["questions"])
            lines.append("")
        if item["source_ids"]:
            lines.append(f"**Sources:** {_format_sources(item['source_ids'], source_index)}")
            lines.append("")
        if item["remediation"]:
            lines.append(f"**Next step:** {_md(item['remediation'])}")
            lines.append("")
    return lines


def markdown_report(report: dict[str, Any]) -> str:
    source_index = {source["id"]: source for source in report["sources"]}
    findings = report["findings"]
    grouped = {
        "candidate": [item for item in findings if item["status"] == "candidate"],
        "not_detected": [item for item in findings if item["status"] == "not_detected"],
        "scan_incomplete": [item for item in findings if item["status"] == "scan_incomplete"],
    }
    summary = report["summary"]
    lines = [
        "# Software Market Candidate Scan",
        "",
        f"- **Markets:** {', '.join(report['markets'])}",
        f"- **Scanned files:** {report['scanned_file_count']}",
        f"- **Excluded skill/reference files:** {report['excluded_file_count']}",
        f"- **Scanner candidates:** {summary['candidate']}",
        f"- **Domains with no scanner match:** {summary['not_detected']}",
        f"- **Scan incomplete items:** {summary['scan_incomplete']}",
        "",
        "> This is a candidate scan, not a compliance decision. The model must complete the code-review checklist even when the scanner finds no matches.",
        "> Required checklist: `references/code-review-checklist.md` in the `software-market-compliance` skill directory.",
        "",
    ]
    lines.extend(_format_section("Scanner Candidates", grouped["candidate"], source_index))
    lines.extend(_format_section("No Scanner Match", grouped["not_detected"], source_index))
    lines.extend(_format_section("Scan Incomplete", grouped["scan_incomplete"], source_index))
    lines.extend(["## Limitations", ""])
    lines.extend(f"- {limitation}" for limitation in report["limitations"])
    lines.append("")
    return "\n".join(lines)


def _write_output(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _exit_code(report: dict[str, Any]) -> int:
    return 2 if report["summary"]["scan_incomplete"] else 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    project_root = Path(args.project_root).resolve()
    if not project_root.is_dir():
        print(f"error: project root is not a directory: {project_root}", file=sys.stderr)
        return 2

    try:
        if args.markets:
            markets = validate_markets(args.markets)
        else:
            input_path = _resolve_input(project_root, args.input)
            if not input_path.is_file():
                report = {
                    "schema_version": "1.0",
                    "skill": "software-market-compliance",
                    "project_root": str(project_root),
                    "markets": [],
                    "scanned_file_count": 0,
                    "excluded_file_count": 0,
                    "findings": [_scan_incomplete(f"markets input file is missing: {input_path}", str(input_path))],
                    "sources": [],
                    "summary": {"candidate": 0, "not_detected": 0, "scan_incomplete": 1},
                    "limitations": ["No market was available, so domain checks were not run."],
                }
                payload = markdown_report(report) if args.format == "markdown" else json.dumps(report, ensure_ascii=False, indent=2)
                if args.output:
                    _write_output(Path(args.output), payload)
                else:
                    print(payload)
                return 2
            markets = validate_markets(read_markets_yaml(input_path))
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.format == "both" and not args.output:
        print("error: --output is required when --format both is used", file=sys.stderr)
        return 2

    output_path = Path(args.output).resolve() if args.output else None
    report = run(project_root, markets, output_path)
    json_payload = json.dumps(report, ensure_ascii=False, indent=2 if args.pretty or args.format != "json" else None) + "\n"
    markdown_payload = markdown_report(report)

    if args.format == "json":
        if output_path:
            _write_output(output_path, json_payload)
        else:
            print(json_payload, end="")
    elif args.format == "markdown":
        if output_path:
            _write_output(output_path, markdown_payload)
        else:
            print(markdown_payload)
    else:
        assert output_path is not None
        markdown_path = output_path if output_path.suffix.lower() == ".md" else output_path.with_suffix(".md")
        json_path = markdown_path.with_suffix(".json")
        _write_output(markdown_path, markdown_payload)
        _write_output(json_path, json_payload)
        print(f"wrote {markdown_path}")
        print(f"wrote {json_path}")

    return _exit_code(report)


if __name__ == "__main__":
    raise SystemExit(main())

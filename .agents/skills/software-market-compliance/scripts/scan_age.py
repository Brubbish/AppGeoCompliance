"""Age, child-user, and store age-rating candidate checks."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from common import TextFile, finding, find_matches, load_json


def _evidence_for(files: list[TextFile], patterns: list[str], limit: int = 6) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    for file in files:
        for pattern in patterns:
            evidence.extend(find_matches(file, pattern, limit=limit - len(evidence)))
            if len(evidence) >= limit:
                return evidence
    return evidence


def _minimum_age_evidence(files: list[TextFile], patterns: list[str]) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    for file in files:
        for line_number, line in enumerate(file.lines, start=1):
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    evidence.append({"file": file.relative_path, "line": line_number, "excerpt": line.strip()[:240]})
                    break
            if len(evidence) >= 4:
                return evidence
    return evidence


def _structured_store_candidates(files: list[TextFile]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for file in files:
        if file.path.suffix.lower() != ".json":
            continue
        try:
            data = json.loads(file.text)
        except (json.JSONDecodeError, TypeError):
            continue
        if not isinstance(data, dict):
            continue
        rating = str(data.get("ageRating", data.get("age_rating", data.get("rating", "")))).lower()
        adult_flag = data.get("containsAdultContent", data.get("contains_adult_content"))
        if rating in {"everyone", "all ages", "4+", "3+"} and adult_flag is True:
            candidates.append({
                "file": file.relative_path,
                "line": 1,
                "excerpt": "Structured JSON contains an all-ages rating and containsAdultContent=true."
            })
    return candidates


def scan(
    files: list[TextFile],
    markets: list[str],
    skill_root: Path,
) -> list[dict[str, Any]]:
    rules = load_json(skill_root / "rules" / "age.json")
    findings: list[dict[str, Any]] = []

    age_signals = _evidence_for(files, rules["age_patterns"])
    minimum_age = _minimum_age_evidence(files, rules["minimum_age_patterns"])
    bypass = _evidence_for(files, rules["explicit_bypass_patterns"])
    all_ages = _evidence_for(files, rules["all_ages_patterns"])
    adult_content = _evidence_for(files, rules["adult_content_patterns"])
    structured_candidates = _structured_store_candidates(files)

    if minimum_age and bypass:
        for market in markets:
            findings.append(
                finding(
                    finding_id="AGE-MINIMUM-AGE-BYPASS",
                    domain="age",
                    market=market,
                    status="candidate",
                    severity="high",
                    title="Declared minimum age and age-gate bypass signals both appear in project files",
                    facts=["A minimum-age rule and a setting/code signal that disables or bypasses an age gate were detected."],
                    evidence=(minimum_age + bypass)[:8],
                    why_not_confirmed=["Static scanning cannot determine whether these files are active in the release or whether a backend enforces the age restriction."],
                    questions=[
                        "Is this configuration used by the production release?",
                        "Can a user below the declared minimum age reach the restricted feature?",
                        "Is enforcement performed by a backend or store-level control?"
                    ],
                    source_ids=rules["sources"].get(market, []),
                    remediation="Trace the release access-control path and compare it with the declared age rule.",
                )
            )

    if structured_candidates:
        for market in markets:
            findings.append(
                finding(
                    finding_id="AGE-STORE-RATING-CANDIDATE",
                    domain="age",
                    market=market,
                    status="candidate",
                    severity="high",
                    title="Structured JSON contains an all-ages rating and adult-content flag",
                    facts=["A JSON file declares an all-ages rating together with containsAdultContent=true."],
                    evidence=structured_candidates,
                    why_not_confirmed=["The file may be a draft, fixture, internal test, or metadata for a different release."],
                    questions=["Is this the final store submission for the release under review?", "Does the flag describe content users can access in that release?"],
                    source_ids=rules["sources"].get(market, []),
                    remediation="Compare the source document with the current store submission and actual available content.",
                )
            )
    elif all_ages and adult_content:
        for market in markets:
            findings.append(
                finding(
                    finding_id="AGE-STORE-RATING-CANDIDATE",
                    domain="age",
                    market=market,
                    status="candidate",
                    severity="high",
                    title="All-ages rating and adult-content signals need release-context review",
                    facts=["All-ages rating and adult-content signals were found in scanned project files."],
                    evidence=(all_ages + adult_content)[:8],
                    why_not_confirmed=["The signals may come from documentation, test data, or different product surfaces."],
                    questions=["Do both signals describe the same released app and content catalog?", "What is the final store age-rating submission?"],
                    source_ids=rules["sources"].get(market, []),
                    remediation="Compare final store metadata with the actual release content.",
                )
            )

    if age_signals:
        for market in markets:
            questions = [
                "What age range is the product designed for in this market?",
                "Does the date-of-birth or age input actively restrict access, or is it informational only?",
                "What data is collected from minors and what parental-control or consent flow applies?"
            ]
            if market == "us":
                questions.append("Is the service directed to children under 13 or does it have actual knowledge of collecting their personal information?")
            if market == "eu":
                questions.append("Which EU member states are targeted, and what age/consent basis applies in each relevant state?")
            findings.append(
                finding(
                    finding_id="AGE-CHILD-SIGNAL",
                    domain="age",
                    market=market,
                    status="candidate",
                    severity="high" if market == "us" else "medium",
                    title="Age, child-user, or parental-control signals need code review",
                    facts=["Age, child, minor, COPPA, parental-consent, or date-of-birth signals were detected."],
                    evidence=age_signals[:6],
                    why_not_confirmed=["Static scanning cannot establish the intended audience, actual knowledge, runtime enforcement, or completed consent flow."],
                    questions=questions,
                    source_ids=rules["sources"].get(market, []),
                    remediation="Trace audience, age-gate, guardian flow, store rating, and data handling in the release implementation.",
                )
            )

    return findings

"""Country and region naming review candidates.

This scanner deliberately does not turn geopolitical terms into legal violations.
It identifies display text that needs a market- and context-specific review.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from common import TextFile, finding, find_matches, load_json


def scan(
    files: list[TextFile],
    markets: list[str],
    skill_root: Path,
) -> list[dict[str, Any]]:
    rules = load_json(skill_root / "rules" / "naming.json")
    findings: list[dict[str, Any]] = []

    for rule in rules["patterns"]:
        applicable_markets = [market for market in markets if market in rule.get("markets", markets)]
        if not applicable_markets:
            continue
        evidence: list[dict[str, Any]] = []
        for file in files:
            evidence.extend(find_matches(file, rule["pattern"], limit=3))
            if len(evidence) >= 6:
                break
        if not evidence:
            continue

        for market in applicable_markets:
            findings.append(
                finding(
                    finding_id=f"NAME-REVIEW-{rule['id'].upper()}",
                    domain="naming",
                    market=market,
                    status="candidate",
                    severity="medium",
                    title=f"Review country or region naming: {rule['label']}",
                    facts=[
                        "The project contains a country, region, or disputed-area label "
                        "whose acceptability depends on display context and target market."
                    ],
                    evidence=evidence,
                    why_not_confirmed=[
                        "A text match does not establish that the label is unlawful or violates a platform rule.",
                        "Static scanning cannot determine the intended audience, surrounding UI, or approved naming policy."
                    ],
                    questions=[
                        "Is this text user-facing in the selected market?",
                        "Which product surface uses it: map, country selector, marketing, report, or internal data?",
                        "Does the project have an approved market-specific naming decision for this entity?"
                    ],
                    source_ids=rules["sources"],
                    remediation=(
                        "Record the approved display label, target market, surface, reviewer, and source basis. "
                        "Do not replace labels globally without a context-specific decision."
                    ),
                )
            )
    return findings

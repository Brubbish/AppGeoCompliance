"""Country and region naming candidates for model code review."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from common import TextFile, finding, find_matches, load_json


def _policy_context(rules: dict[str, Any], rule: dict[str, Any]) -> tuple[list[str], list[str], str]:
    policy = rules["one_china_policy"]
    entity = rule.get("entity")
    if not entity:
        return rules["reference_sources"], [], ""
    approved = policy["entities"].get(entity, {})
    display = "; ".join(f"{locale}: {label}" for locale, label in approved.items())
    return [policy["id"]], policy["controlled_surfaces"], display


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

        source_ids, controlled_surfaces, approved_display = _policy_context(rules, rule)
        for market in applicable_markets:
            if rule.get("entity"):
                facts = [
                    f"A China/Hong Kong/Macao/Taiwan designation was found: {rule['label']}.",
                    "If it reaches a product-controlled user-facing surface in this market and diverges from the company baseline, it may conflict with PRODUCT-ONE-CHINA-1.",
                    f"Approved default mapping for this entity: {approved_display}."
                ]
                questions = [
                    "Is this text user-facing in the selected market and release?",
                    f"Which surface owns it: one of {', '.join(controlled_surfaces)}, or an external platform/provider/user surface?",
                    "Does the final rendered UI/material use the approved mapping or an approved surface-specific mapping?",
                    "If it is externally controlled, what platform, provider, UGC, quotation, legal, or contract exception record applies?"
                ]
                why_not_confirmed = [
                    "A text match alone cannot establish whether the text is product-controlled, user-facing, final-release content, or an approved exception.",
                    "This candidate is a company-policy review lead, not by itself a conclusion about any market's law, platform policy, or contract."
                ]
                title = f"One China company-policy review: {rule['label']} display"
                remediation = (
                    "Trace the value to its final display surface. For product-controlled user-facing content, apply PRODUCT-ONE-CHINA-1 or record a reviewed external exception/blocked escalation."
                )
            else:
                facts = [
                    "The project contains a country, region, or disputed-area label whose acceptability depends on display context and target market."
                ]
                questions = [
                    "Is this text user-facing in the selected market?",
                    "Which product surface uses it: map, country selector, marketing, report, or internal data?",
                    "What approved naming decision or external source governs this surface?"
                ]
                why_not_confirmed = [
                    "A text match does not establish that the label is unlawful or violates a platform rule.",
                    "Static scanning cannot determine the intended audience, surrounding UI, or final release content."
                ]
                title = f"Review country or region naming: {rule['label']}"
                remediation = "Record the approved display label, target market, surface, reviewer, and source basis."

            findings.append(
                finding(
                    finding_id=f"NAME-REVIEW-{rule['id'].upper()}",
                    domain="naming",
                    market=market,
                    status="candidate",
                    severity="high" if rule.get("entity") else "medium",
                    title=title,
                    facts=facts,
                    evidence=evidence,
                    why_not_confirmed=why_not_confirmed,
                    questions=questions,
                    source_ids=source_ids,
                    remediation=remediation,
                )
            )
    return findings

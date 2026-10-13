"""Narrow regulatory-trigger candidate checks."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from common import TextFile, contains_any, finding, find_matches, load_json

ACTIVE_LOCATION_PATTERNS = [
    r"navigator\.geolocation\.(?:getCurrentPosition|watchPosition)",
    r"(?:startUpdatingLocation|requestLocation|requestSingleUpdate|requestLocationUpdates)",
    r"CLLocationManager",
    r"FusedLocationProviderClient",
    r"getLastKnownLocation",
]
APP_INDICATOR_PATTERNS = [r"<manifest\b", r"CFBundleIdentifier", r"android\.app\.Application"]
REPORT_OR_BLOCK_PATTERNS = [r"\breport\b", r"\bblock\b", r"举报", r"屏蔽", r"拉黑"]


def _collect_evidence(files: list[TextFile], patterns: list[str], limit: int = 6) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    for file in files:
        for pattern in patterns:
            evidence.extend(find_matches(file, pattern, limit=limit - len(evidence)))
            if len(evidence) >= limit:
                return evidence
    return evidence


def _market_sources(rules: dict[str, Any], market: str) -> list[str]:
    return list(rules["sources"].get(market, []))


def _metadata_location_candidates(files: list[TextFile]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for file in files:
        if file.path.suffix.lower() != ".json":
            continue
        try:
            value = json.loads(file.text)
        except (json.JSONDecodeError, TypeError):
            continue
        if not isinstance(value, dict):
            continue
        location_fields = {str(key).lower(): item for key, item in value.items()}
        collected = location_fields.get("locationcollected", location_fields.get("location_collected"))
        shared = location_fields.get("locationshared", location_fields.get("location_shared"))
        if collected is False and shared is True:
            candidates.append({
                "file": file.relative_path,
                "line": 1,
                "excerpt": "Structured JSON contains locationCollected=false and locationShared=true."
            })
    return candidates


def scan(
    files: list[TextFile],
    markets: list[str],
    skill_root: Path,
) -> list[dict[str, Any]]:
    rules = load_json(skill_root / "rules" / "regulation.json")
    findings: list[dict[str, Any]] = []

    metadata_candidates = _metadata_location_candidates(files)
    non_collection = _collect_evidence(files, rules["privacy_non_collection_patterns"])
    location_signals = _collect_evidence(
        files,
        rules["location_signal_patterns"] + ACTIVE_LOCATION_PATTERNS + rules["location_transmission_patterns"],
    )

    for market in markets:
        if metadata_candidates:
            findings.append(
                finding(
                    finding_id="REG-PRIVACY-METADATA-CANDIDATE",
                    domain="regulation",
                    market=market,
                    status="candidate",
                    severity="high",
                    title="Structured JSON contains conflicting location collection/sharing fields",
                    facts=["The same JSON document declares location as not collected and also shared."],
                    evidence=metadata_candidates,
                    why_not_confirmed=["The scanner cannot determine whether the document is authoritative, current, submitted, or describes the reviewed product release."],
                    questions=["Is this metadata current and user-facing?", "Does it describe the same build and market being reviewed?"],
                    source_ids=_market_sources(rules, market),
                    remediation="Compare the document with the actual data flow and final privacy/store disclosures.",
                )
            )
        elif non_collection and location_signals:
            findings.append(
                finding(
                    finding_id="REG-PRIVACY-LOCATION-CANDIDATE",
                    domain="regulation",
                    market=market,
                    status="candidate",
                    severity="high",
                    title="Location non-collection statement and location code signals both appear",
                    facts=[
                        "A privacy or store statement says location is not collected or used.",
                        "Location permission, request, transmission, or storage signals were found in scanned files."
                    ],
                    evidence=(non_collection + location_signals)[:8],
                    why_not_confirmed=["The files may not describe the same release, and static scanning cannot establish runtime/backend behavior or SDK collection."],
                    questions=[
                        "Do these files describe the same production release?",
                        "Does the released build or a bundled SDK transmit or persist location?",
                        "Are there newer store disclosures or privacy notices outside the scanned files?"
                    ],
                    source_ids=_market_sources(rules, market),
                    remediation="Trace the release data flow and compare it with the final disclosure.",
                )
            )

    ai_evidence = _collect_evidence(files, rules["ai_patterns"])
    ugc_evidence = _collect_evidence(files, rules["ugc_patterns"])
    filing_evidence = _collect_evidence(files, rules["china_filing_evidence_patterns"])
    label_evidence = _collect_evidence(files, rules["ai_label_patterns"])
    app_evidence = _collect_evidence(files, APP_INDICATOR_PATTERNS)
    has_report_or_block = contains_any("\n".join(file.text for file in files), REPORT_OR_BLOCK_PATTERNS)

    if "cn-mainland" in markets and app_evidence and not filing_evidence:
        findings.append(
            finding(
                finding_id="CN-REG-APP-FILING-SIGNAL",
                domain="regulation",
                market="cn-mainland",
                status="candidate",
                severity="high",
                title="Mobile application detected; check mainland China filing applicability",
                facts=["Android or iOS application indicators were detected.", "No filing reference was found in scanned text."],
                evidence=app_evidence[:4],
                why_not_confirmed=["An app indicator does not establish whether the service is offered in mainland China or whether filing evidence is stored elsewhere."],
                questions=[
                    "Will this app provide internet information services to users in mainland China?",
                    "If so, what is the current APP filing record?",
                    "Does the service type require an additional sector-specific license?"
                ],
                source_ids=["CN-APP-FILING", "CN-ANTI-FRAUD-LAW"],
                remediation="Verify applicability with the service owner and record the filing/permit evidence for the release.",
            )
        )

    if "cn-mainland" in markets and ai_evidence:
        findings.append(
            finding(
                finding_id="CN-REG-GEN-AI-SIGNAL",
                domain="regulation",
                market="cn-mainland",
                status="candidate",
                severity="high",
                title="Generative or synthetic AI signals detected; check mainland China service scope",
                facts=[
                    "Generative AI or deep-synthesis signals were detected.",
                    "No AI-content labeling signal was found." if not label_evidence else "AI-content labeling-related text was found."
                ],
                evidence=(ai_evidence + label_evidence)[:8],
                why_not_confirmed=["Applicability depends on service role, audience, output types, and whether the service is offered to the mainland-China public."],
                questions=[
                    "Is this feature provided to the public in mainland China?",
                    "Does it generate or materially edit text, audio, images, video, or virtual scenes?",
                    "What visible and metadata labels are applied to generated/exported content?",
                    "Has a qualified reviewer assessed service-role, assessment, or filing requirements?"
                ],
                source_ids=["CN-GEN-AI", "CN-DEEP-SYNTHESIS", "CN-AI-LABEL"],
                remediation="Trace the feature and document the scope, labeling, and applicable filing assessment.",
            )
        )

    if "cn-mainland" in markets and ugc_evidence and not has_report_or_block:
        findings.append(
            finding(
                finding_id="CN-REG-UGC-SIGNAL",
                domain="regulation",
                market="cn-mainland",
                status="candidate",
                severity="medium",
                title="User-content signals detected without an obvious report/block text signal",
                facts=["User-generated-content signals were detected.", "No report or block text signal was found in scanned files."],
                evidence=ugc_evidence[:6],
                why_not_confirmed=["Moderation and reporting controls may exist in a backend, another component, or a localized UI not scanned here."],
                questions=["How do users report content?", "What moderation and escalation flows exist?", "Which shipped UI exposes these controls?"],
                source_ids=["CN-CONTENT-ECOLOGY"],
                remediation="Trace and review the user-content governance path in code and the released UI.",
            )
        )

    if "eu" in markets and ai_evidence:
        findings.append(
            finding(
                finding_id="EU-REG-AI-ACT-SIGNAL",
                domain="regulation",
                market="eu",
                status="candidate",
                severity="medium",
                title="AI-related signals detected; review EU AI Act role and purpose",
                facts=["AI-related project signals were detected."],
                evidence=ai_evidence[:6],
                why_not_confirmed=["Static analysis cannot establish market availability, organizational role, intended purpose, or system classification."],
                questions=["Will this feature be offered or used in the EU?", "What role does the organization have?", "What is the system's intended purpose?"],
                source_ids=["EU-AI-ACT"],
                remediation="Trace the AI feature and document the role/purpose assessment.",
            )
        )

    if "eu" in markets and ugc_evidence:
        findings.append(
            finding(
                finding_id="EU-REG-DSA-SIGNAL",
                domain="regulation",
                market="eu",
                status="candidate",
                severity="medium",
                title="User-content signals detected; review EU service role",
                facts=["User-content or public-posting signals were detected."],
                evidence=ugc_evidence[:6],
                why_not_confirmed=["Static analysis cannot determine whether the service is an intermediary, hosting service, online platform, or another category."],
                questions=["Can users disseminate content to the public?", "What DSA service category describes this service?", "What notice and appeal flows exist?"],
                source_ids=["EU-DSA"],
                remediation="Trace the public user-content flow and document the service-role analysis.",
            )
        )

    return findings

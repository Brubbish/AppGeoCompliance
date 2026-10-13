"""Map, geospatial-data, attribution, and China map-review candidates."""
from __future__ import annotations

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


def _provider_evidence(files: list[TextFile], providers: dict[str, list[str]]) -> dict[str, list[dict[str, Any]]]:
    found: dict[str, list[dict[str, Any]]] = {}
    for provider, tokens in providers.items():
        evidence = _evidence_for(files, list(tokens), limit=4)
        if evidence:
            found[provider] = evidence
    return found


def scan(
    files: list[TextFile],
    markets: list[str],
    skill_root: Path,
) -> list[dict[str, Any]]:
    rules = load_json(skill_root / "rules" / "maps.json")
    findings: list[dict[str, Any]] = []
    providers = _provider_evidence(files, rules["providers"])
    if not providers:
        return findings

    disabled = _evidence_for(files, rules["explicit_disabled_attribution_patterns"])
    attribution = _evidence_for(files, rules["attribution_patterns"])
    public_map = _evidence_for(files, rules["public_map_patterns"])
    review_evidence = _evidence_for(files, rules["china_review_evidence_patterns"])
    boundaries = _evidence_for(files, rules["custom_boundary_patterns"])
    coordinates = _evidence_for(files, rules["coordinate_patterns"])
    offline = _evidence_for(files, rules["offline_patterns"])
    provider_names = ", ".join(sorted(providers))
    provider_evidence = [item for values in providers.values() for item in values][:6]

    if disabled or not attribution:
        for market in markets:
            findings.append(
                finding(
                    finding_id="MAP-ATTRIBUTION-VERIFY",
                    domain="maps",
                    market=market,
                    status="candidate",
                    severity="high" if disabled else "medium",
                    title="Map attribution needs contract and rendered-UI verification",
                    facts=[
                        f"Detected map provider signal(s): {provider_names}.",
                        "Attribution/logo is explicitly disabled in source." if disabled else "No attribution text was found in scanned source.",
                        "A possible attribution string was found in source." if attribution else ""
                    ],
                    evidence=(provider_evidence + disabled + attribution)[:8],
                    why_not_confirmed=["Static source cannot prove the final rendered attribution or the exact requirements in the provider's contract."],
                    questions=[
                        "Does the provider require attribution for the selected product and plan?",
                        "Is required attribution visible in every released map view, including native-rendered controls?",
                        "Can you provide the applicable terms and a screenshot of the final map UI?"
                    ],
                    source_ids=rules["sources"].get(market, []),
                    remediation="Compare the actual contract with the released map UI; restore provider-required attribution if absent.",
                )
            )

    if "cn-mainland" in markets and public_map and not review_evidence:
        findings.append(
            finding(
                finding_id="CN-MAP-PUBLIC-REVIEW",
                domain="maps",
                market="cn-mainland",
                status="candidate",
                severity="high",
                title="Map display needs mainland China review evidence",
                facts=[
                    f"Detected map provider signal(s): {provider_names}.",
                    "The project contains public-map or geographic-display signals.",
                    "No map review, surveying qualification, or authorization evidence was found in scanned files."
                ],
                evidence=(provider_evidence + public_map)[:8],
                why_not_confirmed=["Static analysis cannot establish whether the view is public in mainland China, whether an exception applies, or whether evidence is stored elsewhere."],
                questions=[
                    "Will this map be displayed to mainland-China users?",
                    "Is the displayed map a simple diagram or an internet map requiring review analysis?",
                    "What supplier authorization, qualification, review number, or exemption basis covers the released map?"
                ],
                source_ids=rules["sources"]["cn-mainland"],
                remediation="Document the map-display analysis and include supplier authorization, review number, or applicable exception basis in the release package.",
            )
        )

    if boundaries:
        for market in markets:
            findings.append(
                finding(
                    finding_id="MAP-BOUNDARY-REVIEW",
                    domain="maps",
                    market=market,
                    status="candidate",
                    severity="high" if market == "cn-mainland" else "medium",
                    title="Custom boundary or disputed-area map content needs review",
                    facts=["The project contains boundary, border, administrative-area, or disputed-area map signals."],
                    evidence=boundaries[:6],
                    why_not_confirmed=["A static keyword cannot identify the final geometry, label, market view, or whether a provider-rendered layer is used unchanged."],
                    questions=[
                        "Is this a custom overlay or a provider-rendered default layer?",
                        "Which markets can see it, and what naming policy applies?",
                        "Has the final rendered map been reviewed against the applicable market requirements?"
                    ],
                    source_ids=rules["sources"].get(market, []),
                    remediation="Review final rendered screenshots and retain the data source, version, and approval decision.",
                )
            )

    if coordinates:
        for market in markets:
            findings.append(
                finding(
                    finding_id="MAP-COORDINATE-REVIEW",
                    domain="maps",
                    market=market,
                    status="candidate",
                    severity="low",
                    title="Coordinate-system use needs supplier and market review",
                    facts=[f"Coordinate-system reference(s) found: {', '.join(sorted({item['excerpt'] for item in coordinates[:4]}))}."],
                    evidence=coordinates[:6],
                    why_not_confirmed=[
                        "Coordinate-system use is not by itself a legal violation, and static analysis cannot validate the full data path.",
                        "Absence of GCJ-02 is never treated as a universal mainland-China violation."
                    ],
                    questions=[
                        "What coordinate system does each input, SDK, conversion, and output use?",
                        "Do supplier API requirements and the release market's map-review decision cover these conversions?"
                    ],
                    source_ids=rules["sources"].get(market, []),
                    remediation="Document input/output coordinate systems and test known points through the released map stack.",
                )
            )

    if offline:
        for market in markets:
            findings.append(
                finding(
                    finding_id="MAP-OFFLINE-REVIEW",
                    domain="maps",
                    market=market,
                    status="candidate",
                    severity="medium",
                    title="Offline, prefetch, or bulk map-data behavior needs license review",
                    facts=["Offline/prefetch/bulk map-data signals were detected."],
                    evidence=offline[:6],
                    why_not_confirmed=["The scanner cannot distinguish permitted offline use from prohibited retrieval or confirm account-specific terms."],
                    questions=[
                        "Which map product, plan, and license authorize the offline or prefetch behavior?",
                        "What request volume, caching, export, and redistribution behavior occurs in production?"
                    ],
                    source_ids=rules["sources"].get(market, []),
                    remediation="Compare implementation with the exact supplier contract, API terms, caching limits, and attribution obligations.",
                )
            )

    return findings

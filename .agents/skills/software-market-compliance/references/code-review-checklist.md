# Model Code Review Checklist

This checklist is the second, mandatory track of `software-market-compliance`. Complete it after the candidate scanner, including when the scanner reports zero matches. A scanner result is a lead, not a legal conclusion; absence of a match is not evidence that a domain is safe.

## Review protocol

1. Confirm selected markets. Keep `cn-mainland`, `us`, and `eu` separate for legal, platform, distribution, data-protection, map, and age/children analysis. The cross-market policy applies only to each selected market's product-controlled **region-naming surfaces**; do not use it to replace market-specific legal, map, or age rules.
2. Map relevant product surfaces and trace the implementation: entry point, user-visible surface, state/permission gates, API calls, persistence, SDK/backend boundary, release configuration, and store/marketing assets that are present in the repository.
3. Review every applicable item in the four domains below, even if the scanner has no candidate. Use repository search to locate code, then read surrounding implementation and call sites. Do not infer runtime behavior from a permission or dependency name alone.
4. For every conclusion, record code/file evidence or the missing evidence. Cite the applicable source IDs from `references/source-registry.json` and explain why the source applies to the selected market and product behavior.
5. When applicability or production behavior cannot be established from the repository, mark `not_reviewable` or `candidate` and ask the developer for the specific missing fact. Do not turn uncertainty into a violation.

## Result vocabulary

- `confirmed_issue`: The reviewed implementation and available release evidence establish a concrete conflict with a cited applicable `company_policy`, legal, platform, or contract requirement. State the requirement type. A `company_policy` issue is an internal release-policy deviation, not a regulator or court finding.
- `candidate`: Evidence suggests a possible issue, but a required applicability, runtime, release, market, or contract fact is unresolved.
- `not_found`: The reviewed code and available evidence did not reveal the described issue. This is limited to the reviewed scope and is not a compliance certification.
- `not_reviewable`: Necessary code, generated assets, backend behavior, commercial terms, submission materials, target member state, or other evidence is absent.

A scanner candidate may be reclassified after code review. Preserve both the original scanner result and the model's reasoned review result; do not silently overwrite one with the other.

## A. Country and region naming

Review user-visible surfaces, not only strings:

- Country/region selectors, account/profile forms, locale files, reports, exports, marketing pages, store title/description/screenshots, map labels, country codes, and fallback names.
- Trace the data model from internal identifier/code to localized display label. Check that labels do not accidentally expose raw codes, use an unrelated locale, or vary inconsistently across equivalent user-facing surfaces.
- Compare product-controlled labels against [`PRODUCT-ONE-CHINA-1`](product-one-china-policy.md). This company policy applies to every selected market's **controlled region-naming surfaces** and requires China-associated hierarchy and approved mappings for Hong Kong, Macao, and Taiwan on those surfaces.
- For product-controlled country/region selectors, comparison tables, custom map legends, store materials, marketing materials, and user-facing exports, do not render Hong Kong, Macao, or Taiwan as sovereign-country peers of China **in the region-name/region-label text**. Use the approved policy mapping or a documented surface-specific approved mapping. Map boundaries, layers, geometry, coordinates, provider authorization/review, and map contracts remain separate market-specific map checks.
- Keep internal identifiers, ISO/UN codes, provider identifiers, and user-visible labels separate. Technical identifiers may remain in data storage but must not be exposed as user-facing geopolitical labels without review.
- For every candidate geopolitical label, inspect the full sentence, UI purpose, target market, surrounding entities, whether the surface is product/platform/provider/user controlled, and whether it is a neutral data field, map label, editorial statement, or marketing claim.
- For platform-fixed fields, provider-rendered map labels, user-generated content, verbatim quotations, or a cited legal/platform/contract requirement, record the owner and exception basis. Do not silently waive this naming policy; mark an unresolved conflict affecting region-naming display `candidate` or `not_reviewable` and route it as `blocked_pending_escalation`.
- Check relevant text embedded in repository images only when an OCR/image inspection capability is available. If not, list the unreviewed assets as `not_reviewable` rather than claiming they are clear.

A match for Taiwan, Hong Kong, or Macao is not automatically a legal violation. If code, final UI, store preview, or marketing evidence confirms a product-controlled user-facing display that diverges from `PRODUCT-ONE-CHINA-1`, report a `confirmed_issue` with requirement type `company_policy`. Do not use ISO, UN statistics codes, provider labels, or style guides as proof that an external law settles sovereignty or requires the company's exact mapping.

## B. Legal and regulatory triggers

Read the implementation and determine whether a regulated activity is actually present. Focus only on the selected markets and this skill's scope:

### Mainland China

- APP filing: inspect the app/package entry point, service type, intended distribution, filing number/record references, release metadata, and any sector-specific license evidence. A mobile app indicator alone is not enough to establish filing applicability or a violation.
- Generative AI/deep synthesis: trace whether the product provides generation or material editing to mainland-China users, who operates the service, what content types are produced, and where labeling, complaints, content handling, and assessment/filing evidence exist.
- User content: inspect actual create/upload/comment/publication flows, reporting and moderation entry points, enforcement and escalation paths. A string named `report` does not prove the control exists.
- Privacy/data: trace personal information collection from UI/permission through SDK/API/backend storage and sharing. Compare observed flows with privacy notices and release/store declarations. A permission alone does not prove collection; an SDK alone does not prove transmission.

### United States

- COPPA/child privacy: evaluate whether the service is directed to children under 13 or has actual knowledge of collecting their personal information. Coordinate the detailed age analysis with Domain D.
- State privacy: inspect location, identifiers, child data, disclosures, deletion/access/opt-out paths and SDK sharing. Applicability thresholds, exemptions, residency and business facts may require developer confirmation; do not infer them from source code alone.
- FTC consumer-protection exposure: compare privacy, age, location, and product claims in the repository with implementation evidence. Report a deceptive/unfair-practice concern only as a legal-review candidate unless the full facts and applicable requirement are clear.

### European Union

- GDPR: determine whether EU territorial scope is plausibly met; trace personal-data purposes, disclosures, rights flows and location/child data. Distinguish ordinary personal data from Article 9 special-category data; do not assume location alone is special-category data.
- DSA: inspect whether users store or disseminate information to the public and identify the apparent service role before checking platform obligations. A comments widget alone does not establish the operator is an online platform.
- AI Act: identify intended purpose and organizational role (provider/deployer/importer/distributor) from the project evidence. Do not assign a risk class from model/API names alone; flag missing role/use facts for confirmation.
- Children: coordinate with Domain D. If the intended member states are not known, do not apply one EU-wide age-of-consent threshold.

For each potentially applicable rule, record: source ID, trigger fact, implementation evidence, unresolved facts, and the next developer question. Never infer an APP filing, permit, algorithm filing, security assessment, GDPR DPIA, DSA role, COPPA applicability, or AI Act classification solely from a keyword.

## C. Maps and geospatial information

Trace each map surface from provider/data source through rendering and any custom overlay:

- Identify map SDK/API, tile/data provider, geocoder, routing provider, offline data, cached/exported data, and any self-produced boundary or administrative layer.
- Read the relevant dependency/configuration and rendering component. Check whether required provider attribution is visible in the actual UI; a source string or `attributionEnabled` setting alone cannot prove what users see.
- Inspect final map screenshots/assets when available. Review boundary and region labels, administrative hierarchy, disputed-area overlays, coastline, flags, and map legends for each selected market. Apply `PRODUCT-ONE-CHINA-1` only to product-controlled region-name text in custom labels, legends, and overlays; assess boundaries, layers, coordinates, provider authorization/review, and map contracts under each market's map rules.
- For mainland China, determine whether the product displays a public map, what is customized, what supplier qualifications/authorization and review evidence exist, and whether a map-review exception is being relied on. A missing审图号 in source does not by itself prove a violation.
- Trace coordinate inputs/outputs and conversions, and compare them with the selected provider API contract and data source. Do not treat absence of GCJ-02 as a universal legal violation.
- Check the actual product/plan terms for attribution, caching, offline use, storage, export, and redistribution. If contract text/account plan is unavailable, mark `not_reviewable` or `candidate`.

A provider's rendered border, ISO/UN code, or map label is not a legal boundary determination. Do not state that a map is compliant merely because it comes from a named provider or standard map source.

## D. Age, children, and age ratings

Trace intended audience, age inputs, access gates, and data handling:

- Find age/date-of-birth fields, minimum-age configuration, age-gate UI, server-side checks, bypass/debug paths, parental controls/consent, child/family modes, and account deletion or guardian flows.
- Follow the age value from input to validation and to protected features. Check whether enforcement is client-side only, server-side, bypassable, and enabled in the production configuration.
- Inspect store age-rating questionnaires/metadata and compare them with actual user-generated content, chat, user contact, AI generation, adult themes, gambling, or other age-relevant functions. Do not infer a store rating from keywords alone.
- Trace whether child/minor accounts can use location, targeted ads, public posting, direct messaging, or AI features, and what controls actually gate those flows.
- For the United States, establish the COPPA audience/actual-knowledge facts rather than treating any child-related string as sufficient.
- For the EU, identify target member states and the legal basis used for child consent; do not assume one threshold across all member states.
- For mainland China, check whether minors are in scope and what applicable personal-information safeguards are implemented; ask for product audience and release facts not present in code.

A birthday field does not prove effective age verification. A minimum-age constant does not prove enforcement. A mismatch found only between unrelated source files is a candidate until the developer confirms they describe the same release.

## Required review output

After the scanner report, include a model-reviewed table with at least one row for each domain and market. Split rows further when there are distinct features or release surfaces.

| Market | Domain | Result | Reviewed implementation/evidence | Applicable source IDs | Missing facts / developer questions |
|---|---|---|---|---|---|
| cn-mainland | maps | candidate | `src/map/MapView.tsx:42` renders provider map; no release screenshot available | `CN-MAP-REGULATION`, `CN-MNR-MAP-GUIDE` | Is this shown to mainland users? Which review/authorization covers this layer? |
| cn-mainland | naming | candidate | `src/regions.ts:18` renders a custom region label for Taiwan | `PRODUCT-ONE-CHINA-1` | Is this label product-controlled and user-facing? Does it use the approved mapping or an approved exception? |

Then summarize:

1. **Confirmed issues**: Only model-reviewed concrete conflicts. Each item must state market, requirement type (`company_policy`, `law`, `platform`, or `contract`), code/release evidence, source ID, and remediation. Keep `company_policy` deviations separate from external legal, platform, and contract conclusions. If none, say none established from reviewed evidence.
2. **Candidates requiring developer confirmation**: State the observed fact and ask specific, answerable questions. For an external conflict with `PRODUCT-ONE-CHINA-1` in the region-naming domain, include the exact external source/version, surface owner, market, channel, language, screenshot/preview, and `blocked_pending_escalation` status. Do not use this naming policy to replace market-specific legal, map, or age sources in other domains.
3. **Not reviewable**: List missing assets, backend paths, terms, release/store submissions, markets, or runtime evidence.
4. **Scanner-only leads**: Preserve candidate IDs/locations not confirmed by code review and say why they remain candidates.
5. **Scope limits**: State which files, build outputs, images, backends, or market-specific materials were not available.

Never use scanner exit status or a zero-candidate report as a compliance verdict.

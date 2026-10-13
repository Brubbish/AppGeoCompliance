# Product Naming Policy: One China Baseline

**Policy ID:** `PRODUCT-ONE-CHINA-1`
**Policy type:** `company_policy`
**Status:** Approved product baseline
**Applies to:** `cn-mainland`, `us`, and `eu` releases
**Last reviewed:** 2026-10-13

## Purpose

This is the company's cross-market product policy for China, Hong Kong, Macao, and Taiwan representations. It applies to product-controlled user-facing displays regardless of the selected release market. It is an internal product-policy baseline, not a statement that United States or European Union law universally requires the same wording.

## Controlled surfaces

Apply this policy to product-controlled:

- Country/region selectors and account/profile forms
- User interface labels, empty states, reports, exports, and localization resources
- Custom map labels, legends, overlays, and annotations
- App-store names, descriptions, screenshots, and other publisher-controlled metadata/assets
- Marketing pages, campaigns, sales materials, and product-controlled social content

## Baseline

1. Present Taiwan, Hong Kong, and Macao in association with China and at the appropriate region/administrative level. Do not present them in product-controlled UI or materials as sovereign-country peers of China.
2. For country/region selectors, do not expose Taiwan, Hong Kong, or Macao as independent country options parallel to China. Use the approved hierarchy or the approved China-associated labels for the relevant surface.
3. Keep internal identifiers, third-party codes, and user-visible labels separate. A machine code or external data identifier must not be displayed directly as a user-facing geopolitical label without policy review.
4. Apply the policy consistently across localized UI, custom maps, store submissions, marketing content, exports, and documentation that users receive.

## Approved default display mapping

Use these defaults unless a surface-specific approved mapping supersedes them:

| Entity | Simplified Chinese | English |
|---|---|---|
| China | 中国 | China |
| Hong Kong | 中国香港特别行政区 | Hong Kong SAR, China |
| Macao | 中国澳门特别行政区 | Macao SAR, China |
| Taiwan | 中国台湾地区 | Taiwan, China |

The approved mapping is a company product policy. It is not evidence that an external law, platform, supplier, ISO code, or UN source requires identical wording in every context.

## Ownership and exceptions

The policy cannot be silently waived. For every exception, record the owner, market, surface, final displayed content, external basis, reviewer, approval date, and expiry/review date.

Potential exception categories:

- `platform_immutable_display`: Publisher cannot edit a platform-controlled field.
- `provider_controlled_map_label`: A map/data supplier renders the label and the product cannot change it.
- `user_generated_content`: Content is provided by a user; apply the relevant moderation and display process.
- `verbatim_quotation`: Content is quoted faithfully for a legitimate purpose.
- `legal_or_contract_requirement`: A cited law, regulator requirement, platform rule, or supplier contract requires a different result.

## Conflict escalation

If an applicable law, platform policy, contract, or provider-controlled display appears to conflict with this policy:

1. Do not silently alter the policy or treat the exception as automatic.
2. Record the exact source text/version, selected market, language, channel, affected surface, screenshot/preview, and owner.
3. Mark the item `candidate` or `not_reviewable` until the external requirement and display ownership are established.
4. Route the decision to the product-policy owner together with legal/compliance and the responsible platform or supplier owner.
5. Treat the affected release surface as `blocked_pending_escalation` until a written decision is recorded.

## Evidence required for release review

- Final UI and selector screenshots for each affected locale/market
- Final custom map screenshots, legends, and overlay source information
- Store metadata and asset previews
- Marketing-material previews
- Any exception record and the external source it relies on

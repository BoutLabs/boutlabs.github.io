# Bout Labs Website — Decision Log

Load-bearing decisions and the reasoning behind them. Each entry should
answer: **what did we decide**, **why**, and **what would change our mind**.

Newest entries at the top.

## Template

```markdown
## YYYY-MM-DD — <Decision title>

**Context**: what problem prompted this

**Decision**: what we picked

**Why**: the reasoning. Be specific — "it felt better" doesn't help future readers.

**Alternatives considered**:
- Option A — rejected because ...
- Option B — rejected because ...

**Trip-wire**: what would change our mind. "If we see X happen more than N times, revisit."
```

---

## 2026-11-18 — Cookieless analytics, and a single privacy core

**Context**: The site still loaded Universal Analytics `UA-143690680-1`, a product Google shut down in 2023. New privacy and support pages needed a real analytics choice and one set of standard terms.

**Decision**: Remove the Google tag. Add Cloudflare Web Analytics behind `cloudflare_analytics_token`, rendered only when the token is set (it is blank in this change). Standard privacy terms live once, in `_includes/privacy-shared-core.md`, and published pages include that file. Unpublished product stubs stay in `_privacy/` and are not built.

**Why**: Jesse picked Cloudflare Web Analytics over GA4 so the site can skip a cookie banner. One include cannot drift the way a copied block can. www.boutlabs.com is not proxied through Cloudflare, so the beacon has to be pasted; it will not show up on its own.

**Alternatives considered**:
- GA4 with a consent banner — rejected; the chosen tool is cookieless.
- Copying the shared core into each page and syncing with a script — the script still updates unpublished stubs, but live pages include the file instead.

**Trip-wire**: If the beacon, Adobe Fonts, or a future scheduling widget starts setting cookies or sharing data for ads, the "no banner" claim on `/privacy/` has to be rewritten.

---

## 2026-11-19 — Per-product contact model, city-only address

**Context**: The privacy core hard-coded a personal email address and a street address. County Records Atlas now uses a contact form with no published email.

**Decision**: The shared core (now 0.4-draft) points to "the contact method" in each product section and prints only "Tampa, Florida". The apps (HereNotes, Bout Fitness, Booty Babez) and boutlabs.com use the support form plus `privacy@boutlabs.com`. County Records Atlas uses its own `/contact/` form only.

**Why**: Jesse approved it. A form-only channel is fine where GDPR and CCPA are unlikely to apply (County Records Atlas); the apps and this site keep an email address next to the form, which is the safer default for products that reach EU or California users.

**Trip-wire**: `privacy@boutlabs.com` must exist before merge. Any commercial newsletter needs a real postal address first.

---

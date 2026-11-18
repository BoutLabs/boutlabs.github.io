# Open items for the privacy pages

These were `[OPEN: …]` placeholders or counsel flags in the drafts. They are **not** rendered on the published pages. Anything that had to stay on a page is written as **Not confirmed yet** (search the privacy page for that phrase).

Do not merge this to `master` until the items marked **before merge** are resolved. Master is production.

## Before merge

- [ ] Set **Effective date** and **Last updated** on `/privacy/` and `/herenotes/privacy/`. Both currently say November 18, 2026, the draft date, not the day the page goes live.
- [ ] Drop `-draft` from the shared-core version string (`0.3-draft` in `_includes/privacy-shared-core.md`) once counsel signs off, and bump the date.
- [ ] Paste `cloudflare_analytics_token` in `_config.yml`. Until then the beacon is not on the site, but `/privacy/` already says we use Cloudflare Web Analytics. Either set the token or change that section before merge.
- [ ] Counsel review of both privacy pages. The drafts said they were not ready to publish until that review.

## Assumptions now in the published text

- [ ] **Earlier versions are available on request** (shared core §13). The draft's other option was a link to an archive. Confirm which one.
- [ ] **Support replies within two business days** (`support.html`). Same promise as the contact page. Confirm or change it.
- [ ] **iCloud deletion path** is published on the HereNotes policy and the support FAQ: Settings → [your name] → iCloud → Manage Account Storage → HereNotes → Delete Data. Not verified on a device.
- [ ] **Bare-domain redirect disclosure** was filled from a live check on November 18, 2026 (see below). Re-check if DNS changes.

## Counsel flags (removed from the page, not resolved)

- [ ] Confirm the exact registered name and state of formation. The page says Bout Labs, LLC.
- [ ] Decide whether an EU/UK representative (GDPR Art. 27) is needed.
- [ ] Retention: Jesse asked to keep support and inquiry messages indefinitely. The page says while the request is active, then up to 3 years after last contact, longer only for legal claims or obligations. "Indefinitely" does not meet GDPR/UK GDPR storage limitation or the CCPA retention-disclosure rule. Confirm the 3-year figure, that Capsule's own retention (life of the account) can be reconciled with it, and that someone actually deletes on that schedule.
- [ ] Confirm the international-transfer mechanism for each provider. Cloudflare (analytics), Cloudflare (DNS and the bare-domain redirect), Adobe, and GitHub are **Not confirmed yet** in the provider table. Capsule and Google Workspace use the wording from the draft.
- [ ] Confirm the legal-basis mapping per product.
- [ ] Confirm whether CCPA/CPRA (and other state laws) apply to Bout Labs, LLC, and whether to say we honor those rights regardless.
- [ ] Children / COPPA wording.
- [ ] ePrivacy Art. 5(3): the Cloudflare beacon reads Performance API timings. Confirm that a cookie banner is still not required.
- [ ] Confirm the "no sale / no sharing / no Do Not Sell link" sentences for this website.
- [ ] HereNotes: confirm iCloud private-database sync is fairly described as "not received by Bout Labs," and that "Data Not Collected" is the right App Store label.
- [ ] HereNotes: confirm the iCloud Sync sentences do not claim anything about what Apple can access.
- [ ] HereNotes: confirm Maps, place search, and address lookup should be disclosed here and on the App Store label. The disclosure is on the page.
- [ ] HereNotes: confirm the security wording (no extra passcode, no end-to-end encryption claim).

## Facts still to verify

- [ ] Cloudflare's current docs: no fingerprinting; IP discarded; full beacon data about 7 days, then about a 10% sample; dashboards about six months.
- [ ] Live cookie and storage audit of `/`, `/contact-us/`, `/support/`, `/privacy/`, and a blog post after the beacon is installed. The Universal Analytics tag is already removed.
- [ ] Whether Adobe Fonts sets a cookie or stores anything on the visitor's device. The page says that is not confirmed, and that the font request sends the IP address to Adobe.
- [ ] Whether `service.capsulecrm.com` sets a cookie on submit or on the redirect back.
- [ ] Cloudflare DPA applies to this account, and its Data Privacy Framework certification.
- [ ] Adobe's DPF certification / SCCs.
- [ ] GitHub's DPF certification / SCCs.
- [ ] HereNotes background updates are CloudKit push, and no push token is sent to Bout Labs. The page does not claim the push-token part.
- [ ] No third-party libraries in HereNotes 1.0, again, before each release.
- [ ] `booking_url` in `_config.yml` is empty. If a scheduling tool is added, it belongs on the privacy page. It would likely change the cookie answer.
- [ ] The blog and RSS feed set no cookies of their own. True of the templates today; re-check if that changes.

## Explicitly not done

- [ ] Global Privacy Control / Do Not Track do **not** skip the beacon. The page does not claim they do. Add the skip before saying so.
- [ ] Bout Fitness and Booty Babez privacy pages are stubs in this folder. Not published, not linked.
- [ ] The inactive HereNotes analytics / PostHog paragraph was left out of the repo on purpose.
- [ ] Capsule-side setup for the support form: a Product list custom field (option labels must match the form), what a web-form lead creates, CAPTCHA, and a notification for the tag `Support`. No Capsule settings were changed.
- [ ] No test submission was sent to Capsule.

## Adobe Fonts

Left loaded, pending a decision: self-host fonts we are licensed to host, load Adobe after consent, or keep disclosing the current request. Every page loads it from `_includes/head-adobe-fonts.html` (a stylesheet link to `https://use.typekit.net/dbt2loy.css`), included by `_includes/head.html`.

## DNS check (November 18, 2026)

- Nameservers are Cloudflare (`jack.ns.cloudflare.com`, `iris.ns.cloudflare.com`).
- `www.boutlabs.com` is a CNAME to `boutlabs.github.io`. The response is `server: GitHub.com` via Fastly, with no `cf-ray`. **www is not proxied**, so Cloudflare will not inject the Web Analytics beacon automatically. Paste the token; that is the setup that works.
- `https://boutlabs.com` returns 302 from Cloudflare (`server: cloudflare`, `cf-ray` set) with `X-Served-By: Namecheap URL Forward` to `http://www.boutlabs.com/` (http, not https). That redirect is the Cloudflare edge disclosure on the privacy page. The http target is a separate Namecheap setting and was not changed.

# Bout Labs Website — Lessons

Project-specific gotchas the agents should know about. Generic stack gotchas live in the cornerman stack preset under `known_gotchas`; this file is for things specific to *this* project.

The `learnings-extractor` agent writes new entries to `## Pending review` after CI investigations and PR merges; a human promotes them to `## Active` after triage. Entries older than `cornerman.learning_expiry_days` (default 90) rotate to `## Archive`. See `.claude/plugins/cornerman/docs/lessons-format.md` for the entry format.

## Active

### Cloudflare Web Analytics token is empty on purpose
- **Symptom**: `cloudflare_analytics_token` in `_config.yml` is blank, so no
  beacon is in the HTML. `/privacy/` already describes Cloudflare Web Analytics.
- **Why it matters**: merging that page while the token is blank publishes a
  policy for a tool the site is not running. www.boutlabs.com is not proxied,
  so Cloudflare will not inject the beacon for you.
- **How to apply**: paste the token from the Cloudflare dashboard. The include
  is `_includes/cloudflare-analytics.html`. Do not add a Google tag back.
  `rake test` fails if `googletagmanager`, `gtag(`, or `UA-143690680` shows
  up in `_site/`.

### Master is production — no staging
- **Symptom**: a merge to `master` is live on https://www.boutlabs.com within
  ~1–2 minutes.
- **Why it matters**: there is no "we'll catch it in staging" safety net.
- **How to apply**: never merge a PR you wouldn't deploy. PR previews aren't
  wired up; rely on local `bundle exec jekyll serve` + screenshots in the PR.

### LinkedIn company URLs are intentionally url-ignored in html-proofer
- **Symptom**: `Rakefile` ignores `http[s]?://www.linkedin.com/company/boutlabs*`
- **Why**: LinkedIn 999s automated HEAD/GET against their pages, which makes
  html-proofer fail spuriously.
- **How to apply**: don't "fix" the ignore — extending it to other LinkedIn
  paths is fine if they trip the same gate, but don't remove it.

## Pending review

(empty — newly extracted learnings appear here, awaiting human triage)

## Archive

### GA4 migration is overdue (superseded 2026-11-18)
- Universal Analytics `UA-143690680-1` was removed. The replacement is
  Cloudflare Web Analytics, not GA4. See the active lesson above.

# Bout Labs Website — Lessons

Project-specific gotchas the agents should know about. Generic stack gotchas live in the cornerman stack preset under `known_gotchas`; this file is for things specific to *this* project.

The `learnings-extractor` agent writes new entries to `## Pending review` after CI investigations and PR merges; a human promotes them to `## Active` after triage. Entries older than `cornerman.learning_expiry_days` (default 90) rotate to `## Archive`. See `.claude/plugins/cornerman/docs/lessons-format.md` for the entry format.

## Active

### GA4 migration is overdue
- **Symptom**: `_config.yml` still references `google_tracking_id: UA-143690680-1`
- **Why it matters**: Universal Analytics properties were sunset by Google in
  2023; the UA tag silently no-ops. Any "analytics aren't working" report
  almost certainly traces back to this.
- **Fix direction**: migrate to a GA4 measurement ID (or another analytics
  provider) and update the include that injects the tracking snippet.

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

(empty — Active entries rotate here after expiry)

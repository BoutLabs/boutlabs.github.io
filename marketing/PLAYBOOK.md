# Playbook — Bout Labs

What works, what doesn't, with provenance + half-life.

This file is **written by `playbook-updater`** (v0.2+) after each
campaign hits a measurement window. Strategist and copywriter read it on
every run and bias toward proven patterns. Brand-reviewer reads it to
catch quarantined approaches before they ship again.

In v0.1, this file is empty — `playbook-updater` lands in v0.2. Until
then, you can hand-author entries here using the schema below. They'll
be honored by strategist + copywriter the same way.

## Entry schema

Each entry is a YAML block inside this file. Schema:

```yaml
- id: <kebab-case identifier — channel-persona-pattern-yyyymm>
  learning: "<one-sentence claim, observable and falsifiable>"
  evidence:
    - campaign: <campaign slug>
      <metric>: <value>
      <metric>: <value>
  confidence: low | medium | high
  status: active | quarantined | expired
  expires: <YYYY-MM-DD>           # auto-set to capture_date + 90 days
  applies_to:
    channel: <x | linkedin | blog | email | landing-page>
    persona: <ICP slug — match a file in marketing/icps/>
    format: <blog | x-thread | linkedin | email | landing-headline | demo-script>
  source: <playbook-updater run_id, or "manual" for hand-authored>
```

Statuses:

- **active** — copywriter + strategist actively bias toward this pattern
- **quarantined** — brand-reviewer blocks if the draft uses this pattern
- **expired** — the entry passed its `expires` date without re-validation

## Active entries

<!-- playbook-updater writes here. Empty at bootstrap — no shipped campaigns yet. -->

## Quarantined entries

<!-- Patterns that previously worked but recent campaigns underperformed. -->

## Expired entries

<!-- Patterns past their `expires` date; kept for historical reference. -->

---

## How playbook entries get used

**Strategist** reads active entries when drafting a brief. When a proven
hook / format / cadence applies to the campaign's channel + persona, it
gets cited inline.

**Copywriter** reads active entries when drafting. Same citation pattern
in `<!-- copywriter:note -->` comments.

**Brand-reviewer** reads quarantined entries on every review. If the
draft uses a quarantined pattern, that's an automatic blocker.

**Playbook-updater** (v0.2) writes new entries after each campaign's
measurement window closes.

## Half-life intuition

The default 90-day expiry is calibrated for platform churn. For
brand-fundamentals patterns (voice, do_not_say), put them in `VOICE.md`
where they won't expire.

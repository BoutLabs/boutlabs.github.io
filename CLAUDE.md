# Bout Labs Website — working notes for AI agents

This file captures how the Bout Labs marketing site gets built, so any agent
(Claude, the API SDK, a future contributor's tool of choice) can land work
without re-asking. Humans benefit too — it's a fast read of the conventions.

Sections marked `<!-- cornerman:... -->` are **managed by the cornerman
plugin** — refreshed by `/cornerman upgrade`. Don't hand-edit those; edit the
plugin templates instead. Everything else is project-owned and yours to evolve.

If something here is wrong, fix it; if something here is *missing*, add it.

## What this is

Bout Labs marketing site — Jekyll static site deployed via GitHub Pages from
`master`. There's no PRD; product direction is marketing-driven and the
roadmap lives in GitHub Issues. User-motivation context lives in
[`jtbd/`](./jtbd/) when applicable.

## Stack

<!-- cornerman:stack-hints:start v=1 -->
`custom` preset (no Jekyll preset shipped in cornerman v0.3). Site is Jekyll
4.2 on Ruby 3.0.1 (see `.tool-versions`). Pre-push gate:
`bundle exec rake test` — that task builds the site and runs `html-proofer`
across `_site/`.
<!-- cornerman:stack-hints:end -->

Project-specific stack notes:

- **Jekyll 4.2**, theme `minima ~> 2.0`, plugin `jekyll-feed`
- **Ruby 3.0.1** (pinned via `.tool-versions` — use `asdf` or your Ruby version manager)
- **`html-proofer`** runs as the test step; LinkedIn company URLs are
  intentionally url-ignored (see `Rakefile`)
- **Deploy**: GitHub Pages auto-deploys from `master`. There is no separate
  staging — what's on master is what's live at https://www.boutlabs.com.
- **CNAME**: `www.boutlabs.com` (see `CNAME` file at repo root)

## Commands

```bash
bundle install                  # one-time / after Gemfile changes
bundle exec jekyll serve        # local preview at http://127.0.0.1:4000
bundle exec jekyll build        # produces _site/
bundle exec rake test           # build + html-proofer (CI gate)
```

Run the rake task locally before pushing — that's exactly what CI runs.

<!-- cornerman:github-tooling:start v=1 -->
## GitHub tooling

Default to the **GitHub MCP server** (`mcp__github__*` tools) for repo
interactions; fall back to **GraphQL/REST via `curl`** for the gaps; reach
for `gh` only when neither works.

The token used for repo writes is **`GITHUB_LOGOS_LEKTON_ACCESS_TOKEN`** — a
GitHub App installation token for the **Logos Lekton** app, minted on demand
by `~/.claude/bin/mint-logos-token.sh` and exported from `.zshrc`. Actions
taken with this token (PR opens, comments, merges) attribute to
`logos-lekton[bot]` rather than to Jesse.

For `curl` examples:

```sh
curl -H "Authorization: bearer $GITHUB_LOGOS_LEKTON_ACCESS_TOKEN" \
  https://api.github.com/repos/BoutLabs/boutlabs.github.io/...
```

The GitHub MCP Docker server expects `GITHUB_PERSONAL_ACCESS_TOKEN`
internally — `.zshrc` aliases both names to the same minted value, so MCP
tools work without further config.

If `$GITHUB_LOGOS_LEKTON_ACCESS_TOKEN` is empty, run the mint script
directly to see the underlying error:

```sh
~/.claude/bin/mint-logos-token.sh | head -c 4   # should print `ghs_`
```

Per-machine prerequisites:

- Logos Lekton private key at `$LOGOS_PRIVATE_KEY` (default `~/.config/logos/logos-lekton.<date>.private-key.pem`)
- `.zshrc` source line for `~/.claude/bin/mint-logos-token.sh`
- App ID + installation ID are env-overridable (`LOGOS_APP_ID`, `LOGOS_INSTALLATION_ID`); defaults match the BoutLabs Logos Lekton install
<!-- cornerman:github-tooling:end -->

<!-- cornerman:branching:start v=1 -->
## Branching, commits, PRs

- **Main branch is `master`.** Branch off it; never commit directly. There
  is no separate release branch — master is both default and release, since
  GitHub Pages deploys directly from it.
- **One feature per PR.** Small, focused, independently mergeable.
- **Conventional commits with a scope**:
  - `feat(home): add new services hero`
  - `fix(layouts): re-flow nav on narrow viewports`
  - `chore(deps): bump jekyll-feed`
  - `ci(speed-up): cache bundler install`
- **squash merge.** The PR title becomes the merge commit message.
- **Co-author footer** on every commit when an agent authors:
  ```
  Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
  ```
- **PR body**: `## Summary` (1–3 bullets) + `## Test plan` (checklist). Reference
  the closing issue with `Closes #N` so it auto-closes on merge.
<!-- cornerman:branching:end -->

<!-- cornerman:merge-policy:start v=1 -->
## Merge policy

PRs merge **manually**, not via GitHub auto-merge. Sequence:

1. **CI is green** — required checks pass on the head SHA
2. **Branch is up to date with `master`** — rebase + force-push-with-lease if behind
3. **Any required reviews are approved**
4. **Linked issue's `Closes #N` keyword is present** in the PR body
5. **Then merge** — squash via `mcp__github__merge_pull_request`

Agents that open PRs **stop at PR-open**. They report the URL and what
they verified, then defer the merge to the human. This matters more here
than on most repos — a merge to `master` ships live to production.
<!-- cornerman:merge-policy:end -->

<!-- cornerman:issues:start v=1 -->
## Issues

Every new issue gets type + milestone (and blocked-by / parent when
applicable) set **at create time** — not after.

- **Type** — Feature / Task / Bug (org-level Issue Types)
- **Milestone** — required when one exists; this repo currently has no open
  milestones — file the issue without one and ask before creating new ones
- **Blocked-by** — direct deps only; not transitive
- **Parent / sub-issue** — for umbrella → sub-task relationships
- **`question` label** — for issues waiting on the human's input

The `spec-issue-file` skill applies all metadata at create time.
<!-- cornerman:issues:end -->

<!-- cornerman:agent-pipeline:start v=1 -->
## Working loop with an agent

```
ideation / research-discovery / feedback-discovery
  → evaluator
    → spec-writer
      → architect          (technical guidance pass)
        → implementer
          → pr-reviewer    (independent pre-merge review)
            → ci-fixer     (reactive — only fires on red CI)
```

`architect` and `pr-reviewer` are *optional* gates — skip for trivial work,
use for anything non-trivial.

**For each piece of work**:

1. **Pick from the `Ready` lane on the project board**, not the raw issue list
   (this repo currently has no project board — work straight off the issue list
   and label-filter; revisit if a board gets added)
2. **(Optional) Run `architect`** if the issue is non-trivial and doesn't yet
   have a `## Technical architecture` section
3. **Claim by assigning yourself**
4. **Branch off the latest `master`**
5. **Write the change.** Local rails — `bundle exec rake test` — pass before push
6. **Push and open the PR** with `Closes #N`
7. **Run `pr-reviewer` against the open PR**
8. **Wait for CI + reviewer approval.** Then merge manually
9. **If you walk away mid-flight**, un-assign yourself

**What makes the loop work**:

- **Course-correct, don't micromanage.**
- **Surface decisions, don't speak for the human.**
- **Background tasks don't block the conversation.**
- **Each PR gets its own CI confirmation.**
- **Independent review beats self-review.**
- **Architecture before tactics.**
<!-- cornerman:agent-pipeline:end -->

<!-- cornerman:inter-agent-comms:start v=1 -->
## Inter-agent comms

`AGENT_COMMS.log` at the repo root is a flat-file message bus for short-lived
state that doesn't belong in a commit message or issue comment but matters to
whoever picks up next. It's `.gitignored` — local to the machine.

Before doing something others should know about, append one line:

```bash
echo "<agent-id>/<scope>: <message>" >> AGENT_COMMS.log
```

Examples:

```
implementer/#211: starting impl, worktree at .claude/worktrees/agent-abc
pr-reviewer/#213: posted COMMENT review (5 suggestions, 3 praise); no blockers
architect/#214: appended Technical architecture section
```

At the start of meaningful work, read the last few lines:

```bash
tail -n 50 AGENT_COMMS.log 2>/dev/null
```

Format rules:
- **One line per message** (multi-line goes in an issue comment or PR description)
- **Past-tense or present-progressive**, not future
- **`>>` is atomic** for short lines — keep messages tight (< 200 chars)
<!-- cornerman:inter-agent-comms:end -->

## Project-specific quirks

- **Master is production.** This is GitHub Pages — a merge to `master` is a
  deploy. Treat every merge like a release; no separate staging step.
- **`html-proofer` ignores LinkedIn company URLs** because LinkedIn 999s
  automated requests. Don't try to "fix" that ignore — see `Rakefile`.
- **Ruby 3.0.1 is pinned via `.tool-versions`.** GH Actions caches the
  bundler install via `ruby/setup-ruby@v1` with `bundler-cache: true`.
- **Several long-lived feature branches exist** (`add-blockchain-dev`,
  `landing-page`, `calendly`, etc.) — most are stale. Don't assume they're
  in flight; check with the human before reviving one.
- **The site has a Capsule CRM webform key in `_config.yml`** — that's
  intentional and public-safe (it's a form ID, not a secret).
- **Google Analytics UA-143690680-1** is still wired up in `_config.yml`;
  UA properties were sunset in 2023 — there's a latent task to migrate to GA4.

<!-- hypeman:campaign-loop:start v=1 -->
## Marketing & promotion (hypeman)

This repo has hypeman installed. The marketing manifest lives in
`.claude/project.yaml#marketing`. Brand voice is at
`marketing/VOICE.md`; ICPs are under `marketing/icps/`.

The campaign loop (v0.1 ships the first three steps):

```
signal-scout → audience-profiler → strategist → content-architect →
copywriter → brand-reviewer → distributor → analyst → playbook-updater
```

To file a campaign brief from a signal:

```
/hypeman:campaign-file <signal>
```

To draft content for a hand-off-ready brief: spawn `copywriter` directly
in v0.1. v0.2 ships `/content-draft`.

To re-ground the brand voice against shipped content:

```
/hypeman:voice-define
```

The playbook lives at `marketing/PLAYBOOK.md` — strategist and copywriter
read it on every run; brand-reviewer enforces quarantined entries as
blockers.

**Publishing has high blast radius.** v0.1 defaults `auto_publish:
false` and `require_brand_review: true`. Don't loosen these without a
deliberate decision; an unsanctioned post is hard to retract.

**This repo's special blast-radius case**: master is production for the
website. Anything `requires_pr: true` on the blog channel ships through
the cornerman PR pipeline — a merge to master deploys publicly within
~1–2 minutes. Treat blog publishing accordingly.
<!-- hypeman:campaign-loop:end -->

<!-- hypeman:channel-policy:start v=1 -->
## Channel policy

Bout Labs runs two voice registers across channels:

- **Personal voice** (blog, X) — Jesse's natural voice: casual, sharp,
  numbers-first, dry. Pulls toward Patrick McKenzie / 37signals / Stratechery.
- **Biz-dev voice** (LinkedIn, email) — a calmer, slightly-more-consultancy
  register. Same person, suit on. Still no buzzwords.

Enabled channels: **blog, linkedin, x**.

Tokens for publishing are read from env vars named in the manifest's
`marketing.channels.<channel>.token_env`. Hypeman never asks for token
*values* — only the env var names — to keep secrets out of the repo and
out of agent transcripts.

The LinkedIn page ID, X account ID, and corresponding tokens are not yet
set on this machine — flagged at bootstrap as a follow-up before any
channel-publish flow can run end-to-end. Drafts can be authored without them.
<!-- hypeman:channel-policy:end -->

## Documentation

Docs live in **`docs/`** at the repo root. Pages:

- `docs/ARCHITECTURE.md` — patterns, layering, DI, persistence, threading. Owned by the `architect` agent.
- `docs/WORKFLOW.md` — how to develop in this repo end-to-end.
- `docs/GLOSSARY.md` — project vocabulary.
- `docs/DECISION_LOG.md` — load-bearing calls and reasoning.
- `docs/LESSONS.md` — project-specific gotchas the agents should know about.

<!-- cornerman:voice:start v=1 -->
## Voice

When writing on the team's behalf — PR descriptions, issue comments, doc edits:

- Casual and conversational. Contractions are fine; no corporate-speak.
- Short and punchy. One sentence when one sentence will do.
- Dry humor and light sarcasm are welcome — natural, not forced.
- Em-dashes (—), not double-hyphens. Curly quotes preferred when not in monospace.
- "Not a blocker, but " for minor PR-comment suggestions, not "Nit: ".
- Sign emails / external messages "Best,". Greet by first name, never "Dear".
- Be transparent about uncertainty — "things are still a little squishy" beats fake confidence.

When writing **code comments**:

- Default to writing none. Only add a comment when the *why* is non-obvious.
- Never reference the current task / fix / caller — those belong in the PR description.
- One short line max for explanatory comments.
<!-- cornerman:voice:end -->

---

_Powered by [cornerman](https://github.com/BoutLabs/cornerman-claude-plugin) — refresh managed sections with `/cornerman upgrade`._

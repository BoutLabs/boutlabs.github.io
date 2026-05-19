# Bout Labs Website — Workflow

End-to-end "how to develop in this repo." Skim once, refer back as needed.

## Picking work

This repo has no project board today, so:

1. Look at open issues filtered by label (`enhancement`, `bug`, etc.)
2. Skip anything assigned — that's the "someone's on it" signal
3. If nothing's open that fits, the queue is empty — propose new work via
   the `spec-writer` agent
4. Claim by assigning yourself

## Branching

- Off the latest `master`
- Naming: `<type>/<short-slug>-<issue-number>` (e.g., `feat/services-revamp-42`)
- One feature per branch
- **Note**: several long-lived branches exist on origin (`landing-page`,
  `add-blockchain-dev`, etc.) — most are stale; check before reviving one

## Local rails

Before push:

```bash
bundle exec rake test
```

That builds the site and runs `html-proofer` over `_site/`. CI runs the same
thing — passing locally first is much faster than finding out from a red PR.

## Opening the PR

PR body:

```
## Summary
- 1-3 bullets

## Test plan
- [ ] verified X in `bundle exec jekyll serve` locally
- [ ] `bundle exec rake test` passes

Closes #N
```

`squash` merge. PR title becomes the merge commit message — make it a good
conventional commit.

## Code review

- Independent pre-merge review via the `pr-reviewer` agent (or a human reviewer)
- Use "Not a blocker, but " for minor suggestions
- Em-dashes, not double-hyphens
- Leave positive line-level notes too — not just critique

## CI

`.github/workflows/checks.yml` runs `bundle exec rake test` on Ubuntu with
Ruby cached via `ruby/setup-ruby@v1`. The job name is `checks` — that's the
required check for merge.

If `html-proofer` flags a link, the most common causes are:

- Mistyped path in markdown
- External URL gating automated requests (LinkedIn is already ignored — see Rakefile)
- Missing `assume_extension` case (Rakefile sets it true; rare to hit)

## Merging

Per [`CLAUDE.md`'s Merge policy](../CLAUDE.md#merge-policy):

1. CI green
2. Branch up to date with `master`
3. Required reviews approved
4. `Closes #N` in PR body
5. Manual merge — **a merge to master deploys live**

## After merge

- GitHub Pages picks up the change in ~1–2 minutes — verify on
  https://www.boutlabs.com if the change is user-visible
- Worktrees become orphan-state — sweep periodically with `git worktree prune`

## Documentation as you go

- New load-bearing decision? → `docs/DECISION_LOG.md` entry
- Surprising gotcha? → `docs/LESSONS.md` entry (so agents read it next time)
- Pattern confirmed across multiple issues? → `docs/ARCHITECTURE.md` (architect's call)

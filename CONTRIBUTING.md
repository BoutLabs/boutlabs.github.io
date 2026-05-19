# Contributing to the Bout Labs Website

Welcome. The fast version:

1. Branch off `master`
2. Conventional commits with scope (`feat(scope): summary`)
3. Run `bundle exec rake test` locally before pushing
4. PR body has `## Summary` + `## Test plan` + `Closes #N`
5. squash merge on green CI + approved review

Full conventions live in [`CLAUDE.md`](./CLAUDE.md) — those notes are for AI
agents, but humans benefit from skimming them too.

## Development setup

- Ruby 3.0.1 (pinned in `.tool-versions`) — easiest via `asdf install`
- `bundle install` — installs Jekyll + html-proofer + the dev gems
- `bundle exec jekyll serve` — local preview at http://127.0.0.1:4000

## Pre-push gate

```bash
bundle exec rake test
```

That task builds the site and runs `html-proofer` over `_site/` — same thing
CI runs, so passing locally first saves a CI round-trip.

## Filing an issue

Use the [Bout Labs issue conventions](./CLAUDE.md#issues):

- Type at create time (Feature / Task / Bug)
- Milestone at create time (when any exist — this repo currently has none open)
- Blocked-by deps registered at create time
- Don't add the `question` label unless waiting on a specific person

The fastest path: from inside a Claude Code session, ask the
`spec-writer` agent. It'll produce a hand-off-ready issue with full metadata.

## Opening a PR

```
## Summary
- bullet
- bullet

## Test plan
- [ ] thing verified
- [ ] another thing

Closes #N
```

Skip the `Closes #N` and the linked issue won't auto-close on merge — minor
but annoying.

## Voice in PR comments

- "Not a blocker, but " for minor suggestions, never "Nit:"
- Em-dashes (—), not double-hyphens (--)
- Balance constructive feedback with line-level positive comments

See [`CLAUDE.md`'s Voice section](./CLAUDE.md#voice) for the full set.

## Releases

There are no tagged releases. `master` is production: every merge auto-deploys
to https://www.boutlabs.com via GitHub Pages. Treat every merge accordingly —
no "we'll fix it in the next release" since the next release is the next merge.

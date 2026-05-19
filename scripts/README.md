# Scripts

Project-specific shell scripts. Anything that gets run more than twice and isn't part of the standard build/test/lint flow probably belongs here.

## Conventions

- One script per file. Name it for the verb (`release.sh`, `bootstrap-dev-env.sh`).
- Header comment with: what it does, when to run it, prerequisites.
- `set -euo pipefail` at the top. No silent failures.
- Print what you're about to do before doing it. Print results.
- Don't take destructive action without prompting unless the prompt is in the script's filename (e.g., `rm-build-cache.sh`).

## What goes here

- Local dev setup
- Release management
- One-off data migrations
- CI-adjacent helpers that aren't part of the main workflow

## What doesn't go here

- The standard build/test/lint flow (those live in the stack preset, or for this repo, in the `Rakefile`)
- CI workflow logic (that lives in `.github/workflows/`)
- Production deployment (GitHub Pages auto-deploys on push to master — no script needed)

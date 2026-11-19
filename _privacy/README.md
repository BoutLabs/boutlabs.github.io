# Privacy pages

Published pages:

| URL | Source |
|---|---|
| `/privacy/` | `privacy.md` |
| `/herenotes/privacy/` | `herenotes/privacy.md` |

Bout Fitness and Booty Babez stubs in this folder are **not pages**. Jekyll skips `_privacy/` (leading underscore, and it is listed in `_config.yml` `exclude`). Do not link them until a real audit replaces the stub.

## Why one include, not a copied block

The standard terms live in a single file, `_includes/privacy-shared-core.md`. Each published page ends with:

```
{% include privacy-shared-core.md %}
```

Jekyll runs Liquid before Markdown, so the include is inserted as Markdown and rendered with the rest of the page. There is no second copy on the live pages to drift.

`sync-shared.py` still exists for the unpublished stubs. It copies the include into each `*-privacy.md` file between the shared-core markers, and `--check` fails if:

* a published privacy page drops the include or pastes the core in by hand
* the core or a published page would render an `[OPEN` or `⚠` marker
* a stub's embedded core does not match the include

```
python3 _privacy/sync-shared.py            # rewrite drifted stubs
python3 _privacy/sync-shared.py --check    # report only; exit 1 on drift
python3 _privacy/sync-shared.py --diff     # --check, plus a diff
```

`bundle exec rake test` runs `--check`.

Counsel notes and `[OPEN]` items are not in the include. They are listed in `OPEN-ITEMS.md` and in the pull request that added these pages. The version line inside the include says `0.4-draft` (contact model change, Nov 19, 2026) until that review is done.

The inactive HereNotes analytics paragraph (PostHog) is not in the repo. It stays unpublished until that feature actually ships.

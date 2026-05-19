# Bout Labs Website — Architecture

This doc is owned by the `architect` agent and refreshed as patterns get
confirmed across multiple issues. Don't promote a one-off pattern here — wait
until it's appeared in at least 2 issues and feels load-bearing.

## Layering

This is a Jekyll static site, not an application — there are no real "layers"
in the app-architecture sense. The structural pieces are:

- **`_config.yml`** — site-wide config, plugins, collection registration
- **`_layouts/`** — top-level page shells (default, post, page, etc.)
- **`_includes/`** — composable partials (header, footer, hero, service tile)
- **`_sass/`** — partial-based SCSS; entrypoints in `assets/`
- **`_posts/`** — dated markdown for the news/blog
- **`_services/`** — the `services` collection (one markdown file per service)
- **Top-level `*.html`** — landing pages (`index.html`, `thank-you.html`, `404.html`)
- **`assets/`** — images, fonts, compiled CSS entrypoints

The build pipeline is whatever `jekyll build` does — markdown → HTML, SCSS →
CSS, Liquid template expansion. There is no JS bundler.

## State management

n/a — static site. The closest things to "state" are:

- **Form state** — the contact form posts to Capsule CRM via a webform key
  (see `_config.yml#capsule_webform_key`). Capsule owns the submission state;
  we hand off and link to `thank-you.html`.
- **Analytics** — Google Analytics (UA-143690680-1, see Lessons re: GA4 migration).

## Persistence

n/a — no database. All content is markdown in-repo. Form submissions
persist in Capsule, not here.

## Threading & concurrency

n/a — single-pass static build.

## Cross-cutting concerns

- **Logging**: n/a — static site. CI logs go to GitHub Actions.
- **Analytics**: Google Analytics tracking ID lives in `_config.yml`; injected
  via `_includes/google-analytics.html` (or equivalent).
- **Error handling**: `404.html` is the only custom error page; the rest is
  whatever GitHub Pages returns by default.
- **Feature flags**: none — change ships immediately on merge.

## Patterns intentionally not used

- **No JS framework / bundler.** This is intentional — Jekyll renders to
  static HTML and the site has zero interactive state beyond the Capsule
  contact form. Don't introduce React / Vue / esbuild "to make things easier."
- **No CMS.** Content lives in markdown and gets reviewed in PRs. Keeps the
  diff trail clean and avoids running another service.
- **No separate staging environment.** Master is production. PR previews
  via the GitHub Pages preview URL feature are not enabled (gh-pages doesn't
  do per-branch deploys for a project site without extra config).

---

_Managed by `architect`. Promote patterns here only after confirming across 2+ issues._

---
layout: post
title:  "We audited our own conversion funnel — and shipped nine fixes the same afternoon"
date:   2026-07-21 09:00:00 -0400
categories: [news]
tags: [ai-enablement, engineering, case-study]
hero: /assets/images/posts/we-audited-our-own-site-header.jpg
---

Thirteen findings. Nine fixes merged the same day. Zero manual conflict resolution, even though four of those nine PRs independently touched the same file. Those are the numbers. The site they're about is this one.

We ran a conversion-rate audit against boutlabs.github.io — the marketing site you're reading right now — the same way we'd run one for a client: read every page like a first-time visitor, read the templates like an engineer, write down what's actually wrong instead of what feels wrong. Then we fixed what didn't need a human decision, and left what did.

This post is the after-action report. Not because the bugs were exotic — they weren't — but because the *process* is the part worth writing down. It's the same three-rails discipline from an earlier post in this series, applied to the lowest-stakes, highest-visibility target we have: our own site, where a bad merge is visible to every prospect who loads the homepage.

## What the audit found

Some of these are embarrassing. That's kind of the point.

**The canonical URL tag was hardcoded to the homepage. On every page.** Every blog post, every project page, all pointing their `<link rel="canonical">` at `https://www.boutlabs.com`. Which means every piece of content on the site had been telling Google, for as long as that line of template code existed, "I'm a duplicate of the homepage, don't bother indexing me separately." One line in one include file. We have no way to know how much search equity that quietly cost us, because —

**Analytics had been broken for three years.** The tracking ID was still a Universal Analytics property — a format Google turned off in July 2023. The site had been collecting zero usable data since then. Nobody noticed, because nothing was watching the thing that was supposed to tell us something was wrong. That's the actual lesson, not "remember to migrate to GA4": a metric with no alert on it isn't a metric, it's a decoration.

**A 2019 blog post was live with "TODO" as its entire body.** Title: "Shaders in WebGL." Publicly indexed, reachable from the news page, sitting there for seven years. Nobody's fault in particular — just the kind of thing that survives indefinitely once nobody's looking at it, which is most content, most of the time.

Smaller things stacked on top: no sitemap.xml, no robots.txt, six `<h1>` tags on the homepage where there should have been one, an Open Graph image fallback pointing at a file that didn't exist so social previews were probably broken, render-blocking JS with no `defer`. None of it was hard to find. All of it had been sitting there long enough that "hard to find" wasn't the problem — nobody had looked.

Thirteen findings total, filed as individual GitHub issues, each one specific enough that fixing it didn't require re-deciding what "fixed" meant.

## The part that's actually a process story

Nine of the thirteen didn't need a product decision — a canonical tag either points at the right URL or it doesn't, a sitemap either exists or it doesn't. Those nine went to independent implementer agents, each working in its own isolated git worktree, in parallel. One agent per issue. One branch per agent. Nobody sharing a working directory with anybody else.

That last part matters more than it sounds like it should. Four of those nine issues touched the homepage template independently — a hero button here, a heading-tag fix there, a lazy-load attribute somewhere else, a meta-description change in the front matter. Four separate agents, four separate branches, all editing the same file, none of them aware the others existed. If they'd shared a working tree, that's the recipe for exactly the kind of workspace-bleed failure mode we've written about before — one agent's half-finished edit showing up in another agent's branch. They didn't share one. Each rebased onto master right before merge, in sequence, and every single one applied clean. No conflict markers, no manual merge resolution, just routine rebases — the kind of unglamorous git housekeeping that's easy to skip writing about and is exactly the detail that tells you the isolation actually worked.

All nine passed CI. All nine merged the same afternoon. The whole batch — thirteen issues filed, nine implemented, tested, reviewed, and shipped — happened faster than a single old-fashioned "let's schedule a site audit" meeting would have taken to schedule.

The fourth issue on the list underneath all of this: the site deploys straight to production from `master`. There's no staging environment, no second gate. Which is exactly why every one of those nine PRs still went through the normal review motion — CI green, mergeable, a human looking at the diff before it went out — even on a Tuesday-afternoon batch of what were, individually, small changes. Fast doesn't mean unreviewed. It means the review didn't have to be the bottleneck.

## What we didn't fix

Four of the thirteen findings are still open, and they're staying open on purpose.

They need things only a human can provide — a real GA4 property ID, an actual email address and scheduling link for the contact page, real bio copy for an About page that doesn't exist yet, real client testimonials with permission to use them. An agent could have generated plausible-sounding placeholder text for all four. That would have been worse than doing nothing. A fake testimonial is a lie with a byline. A guessed contact email is worse than no contact email, because someone might actually send something to it.

So those four got filed as their own issues, labeled the way this repo labels anything waiting on a decision only the human can make, and left alone. The discipline that made the other nine fast is the same discipline that made these four wait: know which kind of problem you're looking at before you touch it.

## The rails, applied to ourselves

Bounded scope, visible state, independent review — the same three things from the earlier post, holding up under the least forgiving test we could run them against: our own storefront, fixed by agents, on a site with no safety net between "merged" and "live."

Nothing here is a new idea. It's the old idea, applied to the target most consultancies are laziest about — the site making the pitch for outside work while running years behind on maintaining itself. We'd rather be the shop that found its own broken canonical tag before a client had to point it out.

If you're wondering what a CRO or technical audit would actually surface on your own site, we're not guessing — we just ran the checklist against ourselves and published the results. [Let's talk](/contact-us/). Bring us something as broken as ours was; we've clearly got no room to be precious about it.

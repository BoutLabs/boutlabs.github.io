---
layout: project
title: Lil Peewee
permalink: /projects/lil-peewee/
order: 2
kind: Web app
hero: /assets/images/projects/lil-peewee.png
pitch: A parent-facing potty-training resource. Calm, evidence-driven, and free where it matters most.
stack: Next.js 16 (App Router) + React 19, Tailwind v4, Cloudflare Workers, Neon Postgres + Drizzle, Stripe Checkout
role: Built end-to-end at Bout Labs
status: In active development
links: []
---

Most parenting content online is either an ad with a paragraph attached, or a 12-minute video that could have been three sentences. Lil Peewee picks a deliberate middle: clear, evidence-aware guidance for one specific job &mdash; potty training a small human &mdash; in a format parents can actually read at 6:30 AM with one eye open.

## Why we built it

A direct response to one of our own situations and the friction we saw. Potty-training advice is the kind of content that's high-stakes for the family and low-quality on the web. There's a gap between the academic literature, the pediatrician's two-sentence handout, and the wellness-influencer ecosystem. Lil Peewee aims to be the resource we wished we had &mdash; specific, free for the load-bearing parts, and honest about what works and what doesn't.

## What's in it

- A curated set of evidence-aware guides for the major decision points: when to start, how to set up the bathroom, what to do when it stalls, how to handle regressions
- A short, opt-in email series that delivers the right content at the right moment (Loops for marketing series, Resend for transactional)
- Stripe Checkout for the paid tier &mdash; ad-free, longer-form, downloadable guides
- Cloudflare Workers hosting via the OpenNext adapter &mdash; cheap at scale, fast everywhere
- Plausible for analytics &mdash; anonymous, cookieless, owned

## What we learned shipping it

(To be written as the product matures. The interesting notes here will be the Cloudflare-Workers-runtime parity work, the analytics-versus-privacy decisions, and the content-curation approach for a topic where "evidence-based" is doing a lot of heavy lifting.)

---
layout: post
title:  "Five questions that catch an expensive SaaS mistake before you sign"
date:   2026-07-21 09:00:00 -0400
categories: [news]
tags: [technology-consulting, business, leadership]
hero: /assets/images/posts/saas-due-diligence-questions-header.jpg
---

A mid-market ops team signed a three-year, six-figure contract for a scheduling platform to replace a system three people privately hated maintaining. The demo was clean, the sales engineer was sharp, and the pricing page said "unlimited API calls." Four months in, a webhook integration that mattered to the business — real-time sync with a field-service app their techs used daily — started tripping a rate limit nobody had mentioned in the sales cycle. "Unlimited" turned out to mean unlimited requests, not unlimited *concurrent* webhook deliveries, and the difference cost them 40% of the contract's first-year value in overage fees before anyone caught it.

Nobody lied in that sales cycle. The salesperson answered every question honestly. The problem is that nobody on the buying side asked the one question that would have surfaced the gap — and the sales process isn't built to volunteer it.

That's the pattern behind most SaaS mistakes we see: not fraud, not incompetence, just an information asymmetry the buying process never corrects. The vendor knows exactly where their platform's edges are. The buyer is optimizing for "does this solve my problem," not "where does this platform quietly stop matching my assumptions." Technical due diligence exists to close that gap before the signature — which is also the only time it's cheap to close.

## The five questions that actually matter

Most SaaS evaluation checklists ask "does it have SSO," "is it SOC2 compliant," "what's the uptime SLA." Those questions matter, but they're also the ones a good sales team has already prepared a clean answer for. The questions that catch real problems are the ones that ask the vendor to be specific about the thing their deck was vague about.

**What happens to our data, contractually, the day we cancel?** Not "can we export our data" — every vendor says yes to that. The real question is what format, what completeness, and what timeline the contract commits to in writing, versus what the sales team promises verbally. We've seen "data export" mean a CSV of three of the twelve fields that actually mattered, delivered forty-five days after a support ticket. If the contract doesn't name the format and the SLA, the promise isn't a promise.

**Who owns the roadmap item we're betting this integration on?** Every eval cycle has a moment where the vendor says "that feature's coming next quarter" to close a gap in the current product. Sometimes it ships. Sometimes "next quarter" is a sales incentive, not a committed roadmap line, and the team that owns it gets reprioritized the month after the contract closes. Ask who owns it internally. Get it in writing if the purchase decision depends on it. Assume it doesn't ship if the vendor won't commit it to paper.

**What does the compliance report actually cover, versus what the deck implies?** A SOC2 badge on a landing page and an actual SOC2 report are different documents. The badge tells you a report exists. The report tells you which systems and controls were in scope — and it's common for a vendor's report to cover their core platform while excluding the specific integration layer or sub-processor your data will actually touch. Read the report. Not the marketing page about the report.

**What's the real rate limit and SLA, in the contract, not the docs page?** Docs pages get optimistic. Contracts get precise, because someone's legal team made them precise. If the number that matters to your actual usage pattern — API calls per minute, concurrent webhook deliveries, whatever your integration depends on — isn't in the contract's SLA section, it isn't guaranteed. It's a docs page, and docs pages change without renegotiating your price.

**Has anyone tested this at your real volume, not the vendor's demo volume?** A demo environment is provisioned for a demo. Sales-cycle proofs-of-concept often run at a fraction of production load, over a few days, with a vendor SE quietly making sure nothing goes wrong. The number that matters is what happens at your actual peak — Black Friday volume, month-end close, whatever your business's load pattern looks like — not the friendly number from the trial period.

None of these five are exotic. They're the ones a technical reviewer asks by habit, because the pattern — the gap was always there, nobody asked about it — repeats across almost every vendor category we've evaluated. Scheduling, payments, data infrastructure, support tooling. Doesn't matter.

## What due diligence can't catch

Overselling due diligence is its own kind of dishonesty, so it's worth being straight about the limits. Some risks are structurally impossible to catch pre-signature.

A vendor's own roadmap prioritization can shift for reasons that have nothing to do with your contract — a new VP of product, an acquisition, a board that decides your segment isn't worth serving anymore. No amount of pre-signature questioning surfaces a decision the vendor hasn't made yet. The best you can do is structure the contract so a roadmap shift doesn't trap you — shorter terms, clear exit clauses, no irreversible data lock-in.

A future acquisition can change the pricing model, the support quality, or the product direction entirely, at any point in a multi-year term. This is unknowable at signature. It's a reason to weight shorter commitments and real exit costs more heavily than the discount a longer term buys you.

And no amount of due diligence substitutes for actually using the product at scale, for a real stretch of time. A month-long pilot at reduced volume will always look better than year two at full volume. The gap between the two is exactly where the expensive surprises live. The only real defense is structuring the contract so the first few months are cheap to be wrong about.

## The actual value of an outside technical review

The honest pitch here isn't "we catch every risk." Nobody does. The honest pitch is narrower: an outside technical reviewer who has run this evaluation dozens of times, with no stake in the sales cycle closing, asks the specific questions a busy internal team — optimizing for solving the immediate problem, not for stress-testing the vendor's edges — usually doesn't think to ask. That's not a checklist you can fully outsource to a form. It's judgment, applied to a contract, by someone whose only incentive is getting the trade-offs right before the signature instead of six months after it.

If you're evaluating a SaaS platform right now and want a second set of eyes on the contract before it's signed, [let's talk](/contact-us/).

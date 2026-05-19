# Brand voice — Bout Labs

Captured: 2026-05-19 · Paths used: A (declared preferences from Jesse's writing-style notes) + B (existing site copy, sparse) + C (aspirational anchors: 37signals, Patrick McKenzie, Anthropic)

This file is the source of truth for the brand's voice. The copywriter
reads it on every campaign; the brand-reviewer enforces it. Update it
deliberately — voice drift is real and expensive.

When new content ships that should be canonical, re-run `/voice-define`
to ground the file against real artifacts instead of stated intent.

## Posture

Calmly opinionated. The audience is people who have to make technology
decisions and want to feel less alone in them — not impressed-into-buying.
Bout Labs has done the work for 15+ years across enterprise, mid-market,
and design-led nonprofits. The voice should sound like someone who's seen
the failure modes and isn't selling anything they don't believe in.

Dry humor is welcome but never forced; warmth is genuine, not performative.
Transparent about uncertainty ("things are still a little squishy" beats
fake confidence). Lead with the answer, then the caveat — not the other
way around.

The site's current corporate-consultancy register ("trusted technology
partner", "human-centered approach", "Maintain your edge") is the **floor**,
not the ceiling. New outbound content should pull toward Jesse's voice —
sharper, more specific, less consultant-flavored.

## Cadence

- **Sentence length**: vary aggressively. Short to punch, long to consider,
  one-word sentences when the line earns it.
- **Paragraphs**: 2–4 sentences in long-form; one-sentence paragraphs are
  fine for emphasis or LinkedIn scannability.
- **Sections**: header + 2–4 paragraphs is the default rhythm for blog;
  shorter for LinkedIn and email.
- **Hooks open with substance.** Never "today I want to talk about" or
  "in this post we'll explore". State the claim, ask the actual question,
  or drop the punchline.

<!-- Path B note: shipped site copy is sparse — three landing-page pillars
(Plan / Build / Pivot) and four service blocks. Re-run /voice-define when
3–5 blog posts have shipped to ground these stats against real text. -->

## Vocabulary

### House words (use freely)

- **"trusted partner"** — load-bearing positioning phrase on the current site; carries 15-year-relationship signal
- **"the right [people / resources / pieces]"** — the consultancy's stated edge is matching, not maximizing. Lean into it.
- **"human-centered"** — design-led nonprofit clients (IDEO, IDEO.org) make this credible, not buzzword-y, when it's used carefully
- **"early and often"** — frames iteration as discipline, not chaos
- **"maintain your edge"** — closing CTA on the Fractional CTO section; reusable as a thread of confident-not-arrogant
- **"squishy"** — Jesse's own — for naming uncertainty without losing trust
- **"specifically"** — anti-platitude marker; force concreteness wherever it appears

### Aspirational anchors

- **37signals (Basecamp / Once / DHH)**: opinionated, contrarian-but-defensible. They take a position and tell you why.
    - Borrow: willingness to say "this is wrong" or "we don't do that" without softening it
    - Sources: signalvnoise.com long-form essays
- **Patrick McKenzie (patio11)**: dense, specific, gives away the actual numbers and the actual reasoning
    - Borrow: numbers in the lede; never asserting without showing the work
    - Sources: kalzumeus.com long-form
- **Anthropic (the company that builds Claude)**: helpful as positioning. Explainers that respect the reader's time and intelligence.
    - Borrow: structured clarity, calm tone, willingness to over-explain when the topic genuinely needs it
    - Sources: anthropic.com/news long-form announcements, model cards

### do_not_say

Mirrored into `marketing.brand.do_not_say` in `.claude/project.yaml`. The
copywriter never uses these; brand-reviewer blocks if they appear.

- **revolutionary, game-changer, world-class, best-in-class** — adjective inflation; consultants who haven't shipped use these
- **leverage** (the verb) — say "use" or be more specific
- **synergy, circle back, move the needle, low-hanging fruit, at the end of the day** — corporate-speak; reads as effort to *sound* serious instead of *being* serious
- **delight, unlock, 10x** — startup-deck cliché; a consulting brand using these reads as costume
- **rockstar, ninja, thought leader** — embarrassing in 2026
- **"We're excited to announce"** — the audience isn't excited until they know what's coming

## Stylistic moves

- **Em-dashes over parentheticals** — softer, more conversational
- **Lowercase starts in casual contexts** (Slack-like blurbs, short X posts) — never in long-form blog headlines
- **Sentence case, not Title Case** for blog headlines: "How we'd think about a healthcare data migration" not "How We'd Think About A Healthcare Data Migration"
- **Numbers and durations early** — "15 years across 17 industries" beats "decades of broad experience"
- **Show-the-work asides**: "(here's the part where most teams skip ahead — don't.)"
- **One concrete client situation > three abstract claims** — but **NEVER name a client without explicit clearance** (see Notes for brand-reviewer)
- **"Not a blocker, but"** for soft suggestions, never "Nit:" — extends Jesse's code-review voice into prose

## Hook patterns

### Blog

State the answer in the first sentence. The second sentence raises the
complication that earns the rest of the post. Examples of the move:

- *"The hardest part of a fractional-CTO engagement isn't the strategy. It's the first 90 days, when no one yet trusts you to disagree."*
- *"Most healthcare data migrations fail in the same place — and it's not the migration."*

What to avoid: any opener that starts with "In this post...", "I want to
talk about...", or "Have you ever wondered..."

### X / Twitter

Standalone hook in tweet 1. Substance, number, or contrarian claim — never
"thread, here's everything I learned 🧵👇 1/".

- *"Software-development engagements get cheaper when the client owns the spec. The pattern: who writes the spec is who owns the change-budget."*

CTA / link goes in the *last* tweet, not inline.

### LinkedIn

Hook + line break + body, structured for scannability. **Never put a
primary link in the body** — LinkedIn deprioritizes link-bearing posts.
End the post with "↓ link in the comments" or a Q-style hook that drives
engagement before the link drop.

LinkedIn audience for Bout Labs is biz-dev: founders, COOs, design-led
nonprofit leadership. Pull the consultancy register up slightly here vs.
X; this is where Bout Labs gets RFPs.

### Email

Greet by first name (when the platform supports merge). Sign off "Best,"
or "Jesse + the team" depending on the touchpoint. No "Dear", no "Regards".
Always offer a specific next step ("happy to hop on a call to clarify",
"reach out if you'd like me to walk through how we'd approach this").

## CTA patterns

Bout Labs' CTAs are conversation, not conversion. The brand sells
relationships, not signups. Default CTA framings:

- **"Let's talk."** — for substantive prospects
- **"Here's how I'd approach yours."** — for content where the bait is a
  worked example
- **"Tell me where this lands wrong."** — for opinion pieces that want
  pushback to surface signal
- **No "BOOK A DEMO"** buttons, no "Click here to learn more", no
  GIF-bait. The audience is sophisticated enough to feel the manipulation.

## Positive exemplars

Sparse on shipped artifacts right now. Until 3–5 blog posts ship, the
canonical exemplars are:

- The landing-page Plan / Build / Pivot section in `index.html` — *the
  shape of the framing*, not the prose (which is older consultancy-tone)
- The Fractional CTO service block ("Maintain your edge.") — short close,
  clean line, confidence without bragging
- Jesse's writing-style note in `~/.claude/CLAUDE.md` — voice description
  used as the de-facto canonical exemplar for personal-voice content

## Negative exemplars (what we're NOT)

- **"We're a top-tier digital transformation partner accelerating your enterprise journey"** — generic Big Consulting Boilerplate. No one believes this and no one acts on it.
- **"Why we built BoutLabs"-style origin posts dressed as engineering content** — fine to write, but don't pretend they're the product
- **Twitter threads that count tweets, use 🧵👇 openers, or screenshot one paragraph and tease "the rest"** — engagement-bait erodes consultancy credibility
- **LinkedIn humblebrags** — "Beyond grateful to share that we just..." (no.)

## Notes for the copywriter

- **Lead with the answer, not the question.** State the claim first, raise the complication second, deliver the body third.
- **Numbers in the first sentence whenever they exist.** "15 years", "3 projects in 6 months", "$1.2M ARR" — concrete beats adjective every time.
- **Bout Labs sells judgement, not deliverables.** Frame engagements as decisions made together, not features shipped.
- **Never name a client by name without checking.** The client list is real and impressive, and that's exactly why it's protected territory.
- **Don't pad short answers.** "Got it.", "Ship it.", "Yep — same call we'd make." are valid sign-offs.
- **Em-dashes (—), not double-hyphens (--). Curly quotes in long-form, straight quotes in code.**
- **When unsure, write less.** Bout Labs gets to look thoughtful when it doesn't overclaim.

## Notes for the brand-reviewer

In addition to the default checklist:

- **Hard-block any client name** (OneWorld Observatory, IDEO, IDEO.org, IdealImage, water.org, SwissLife, Bake'n Babes, Hillsborough County Tax Collector, Addaday, Rock'n'Roll Marathons, 1848 Ventures, THQ, Moffitt Cancer Center, Parathyroid.com, Disney, NYSE, BayCare Health Systems) unless the draft includes the marker `<!-- client-name-cleared:<name>:<who-approved>:<when> -->`. The client list is in the site footer for design — public naming in marketing copy is a separate decision per relationship.
- **Hard-block performance / outcome claims** ("we reduced costs by 40%", "shipped in 6 weeks") without a `<!-- case-study-cleared -->` marker and a link to the public case study or quote.
- **Suggestion-flag any adjective inflation** — "world-class team", "best-in-class process", "deep expertise" — push toward specific evidence instead.
- **Suggestion-flag any opener starting with "In this post"**, "Today I want to", "Have you ever wondered" — see hook patterns.
- **Hard-block "Nit:" in PR-style review comments** — voice rule, applies anywhere Bout Labs is the speaker.
- **Watch for tone leak**: corporate-consultancy register in personal-voice content (blog/X) is a regression; personal-voice register in LinkedIn biz-dev is also a miss. The brand has two registers and the copywriter must match the channel.

---

*Last grounded against shipped content: 2026-05-19 (bootstrap — minimal shipped corpus). Re-run `/voice-define` when 5–10 new campaigns have shipped, or when the brand consciously evolves.*

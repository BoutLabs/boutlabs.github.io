# Style — Bout Labs

Visual and formatting rules. The fine-grained stuff that VOICE.md doesn't
cover. Brand-reviewer treats these as suggestions, not blockers — but
consistent style is what makes a voice feel professional rather than
improvised.

## Typography

- Em-dashes (—), not double hyphens (--)
- Curly quotes ("smart") in long-form, straight quotes in code
- Oxford commas: yes
- Sentence case for headlines, not title case
- HTML-encoded apostrophes (`&apos;`) in the existing `index.html` are a
  Liquid/Jekyll-era holdover — when editing, prefer real characters in
  source; let Jekyll handle escaping

## Code in prose

- Inline code with backticks: `like this`
- Code blocks fenced with language hints:
  ```ruby
  Jekyll::Hooks.register :site, :after_init do |site|
    # ...
  end
  ```
- For X / Twitter: code blocks become screenshots with a monospace font.
  Don't paste raw code into a tweet — it breaks rendering.

## Links

- Blog: full URL on first reference, descriptive anchor text after
- X / Twitter: append the link as the *last* tweet, not inline
- LinkedIn: **never** put the primary link in the post body — LinkedIn
  throttles posts with outbound links. Put it in the first comment, with
  a "↓ link in the comments" gesture in the post itself
- Email: descriptive anchor text, never "click here"

## Line breaks

- Blog: standard paragraphs, no double-spacing
- X / Twitter: tweets break at natural beats — never split a sentence
  across tweets unless the cliffhanger is the point
- LinkedIn: liberal line breaks for scannability (one-sentence
  paragraphs read well on the platform)
- Email: paragraph breaks every 2–4 sentences for mobile

## Emoji policy

**None in long-form** (blog, LinkedIn body, email body). **Rare elsewhere**
— at most one per X post, always meaningful, never decorative. Bout Labs'
audience is mid-market and enterprise consulting buyers; emoji-heavy copy
reads as costume.

The site's bootstrap-icons SVG sprites (`calendar-range`, `tools`,
`signpost-split`) are visual UI, not emoji — they're fine.

## Numbers

- Spell out one through nine; numerals from 10 up (long-form)
- Always use numerals for measurements, percentages, money, time, years
- Numbers in headlines and hooks are good — "15 years across 17 industries"
  beats "decades of broad experience"

## Capitalization

- Product name: **Bout Labs** (two words, both capitalized) — never
  "BoutLabs", "boutlabs", or "Boutlabs" in marketing copy. The GitHub
  org is `BoutLabs` and the domain is `boutlabs.com` — those don't change.
- "Fractional CTO" capitalized when used as a proper service name; lowercase
  in running prose ("a fractional-CTO engagement")
- Technical terms: lowercase unless the term is a proper noun
- No SHOUTING for emphasis

## Lists vs. prose

- Lists earn their bullets — if items are conjunction-connected ideas,
  use prose
- Numbered lists imply order; bulleted lists imply parity
- Long lists (>7 items) usually mean the writing hasn't found the
  through-line yet — push back

## Visuals

- Hero images: existing site uses `assets/images/*-header.jpg` for landing
  hero treatment, with `*-xs.jpg` variants for mobile. New blog hero
  imagery should follow the same naming convention.
- Diagrams: prefer hand-drawn-tone over corporate flat-icon. If a diagram
  is load-bearing for the argument, give it a caption that summarizes
  the diagram in one sentence — for accessibility and for screenshots-of-thread.
- Screenshots: annotate them; raw screenshots without context are wasted
- Logo: `assets/images/bout-labs-logotype.svg` is the canonical wordmark;
  `bout-labs-circle.svg`/`bout-labs-circle.png` are the icon mark

## Brand-specific overrides

- **Client logo strip** at the bottom of `index.html` is the only public
  surface where client names appear. Adding or removing logos there is a
  business-decision PR, not a marketing edit — treat changes to it as
  needing explicit sign-off from Jesse.
- **Closing sign-off on emails** is "Best," (per Jesse's writing-style notes)
  or "Jesse + the team" — never "Regards," "Sincerely," or "Cheers".
- **CTAs are conversational, never imperative.** "Let's talk." not "BOOK A DEMO".
- **Headlines on the existing site use `display-5 fw-bold`** with the
  Bootstrap 5 grid; treat that as the marketing-page typography contract.
- **No exclamation marks in marketing copy.** Period — the brand's
  confidence reads from the claim, not the punctuation.

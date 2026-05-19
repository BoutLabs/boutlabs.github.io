# Jobs to be Done

User-motivation context for the Bout Labs Website. When designing a feature
or evaluating a roadmap candidate, read the relevant JTBD first — these are
the artifacts the agents reach for to anchor product decisions.

## Format

One markdown file per JTBD. Filename: `<persona-or-job-slug>.md`. Each file
covers:

```markdown
# <Job title>

**When**: the triggering situation

**I want to**: the job they're trying to get done

**So I can**: the underlying motivation / payoff

## Forces

- **Push**: what's making the current solution painful
- **Pull**: what's attractive about a new solution
- **Anxiety**: what could go wrong if they switch
- **Habit**: what makes them stick with what they have

## Outcome metrics

- (How would the user know they got the job done?)

## Notes

- (Anything specific to this persona / job that doesn't fit above)
```

## When to write a new JTBD

- A new persona emerges from research and isn't covered by existing JTBDs
- A new use-case shifts the forces analysis enough that the original JTBD
  doesn't anchor the decisions cleanly anymore
- An assumption baked into product decisions turns out to be wrong (revise
  the relevant JTBD with the corrected forces)

## When NOT to write a new JTBD

- For internal stakeholders (PM, eng, design) — those go in the PRD's
  personas section, not here
- For a single feature — JTBDs are about the user's situation, not the feature
- For a hypothetical user — only write a JTBD with evidence (interview,
  observation, survey signal)

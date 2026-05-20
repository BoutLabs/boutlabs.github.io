---
layout: post
title:  "The three rails every AI development loop needs"
date:   2026-05-19 09:00:00 -0400
categories: [news]
tags: [ai-enablement, engineering]
hero: /assets/images/posts/three-rails-ai-loop-header.png
---

The first time an AI coding agent silently lied to us, it cost about four hours. The wrapper reported "running in the background, I'll notify you when it's done." It never notified. The agent had stalled inside its own sandbox, half a commit deep, with uncommitted files smeared across two ticket branches because three parallel runs were sharing one working tree. By the time we untangled it, we'd touched five PRs and salvaged maybe 60% of what the agent had actually produced.

That's the failure mode. Not the agent being wrong — the agent being out of view while it's wrong.

We've spent the last several months running AI coding agents against real BoutLabs projects: an iOS app, a couple of small web services, the marketing site you're reading. Across those engagements, the pattern that consistently ships clean work isn't a better model or a fancier prompt. It's three rails: **bounded scope**, **visible state**, and **independent review**. Without them, the agent's speed becomes the team's liability. With them, the same model that burned four hours can land a credible PR in twenty minutes and let a human spend the rest of the day on judgement instead of cleanup.

This post is about those three rails — specifically, why each one exists, what it costs to skip, and how we wire them up in practice.

## Rail 1: bounded scope

The first rail is that every piece of work the agent touches arrives as one hand-off-ready issue. Not "go build me the dashboard." A specific issue with a thesis, a file list, acceptance criteria, and a definition of done that another human could verify in five minutes.

This is project-management hygiene — the same patterns that help humans share context across distributed teams help agents do it too. What's new with agents is the speed at which a fuzzy spec turns into committed code nobody asked for, and the cost of unwinding it once it has.

Here's what happens when scope is loose. The agent reads the request, infers the intent, fills the gaps with whatever its training distribution thinks is reasonable, and starts editing. Most of the gap-filling is fine. Some of it is subtly wrong — a naming convention that doesn't match the rest of the repo, a library choice that conflicts with an existing one, an abstraction introduced where the codebase had been deliberately flat. The wrongness compounds across files. By the time a human reviews the PR, the cost of unwinding is higher than the cost of throwing it out and starting over.

A tight issue prevents this by making the gap-filling explicit. *These files. This acceptance criteria. These specific edge cases. If you discover adjacent work, file a follow-up issue — do not grow this one.* The agent now has a contract it can be measured against, and the human reviewer has a known shape to diff the PR against.

What "hand-off-ready" looks like, concretely, in the way we file issues:

- A **why** paragraph that names the user (or system) being served and the problem being solved
- A **file list** — sometimes precise, sometimes "around here," but always a starting point
- **Acceptance criteria** as a checklist, not prose. The agent and the reviewer both consult this.
- An **out of scope** section. Counterintuitively, this is the most important field. It's the place where you tell the agent which adjacent improvements to *not* make.

The discipline of writing that issue forces a decision that used to happen mid-implementation, in a Slack thread, by accident. The decision moves earlier. The agent moves faster. And — this is the part that surprises people the first time — the team starts to like writing issues, because the issues become the substrate for working with the agent at all.

## Rail 2: visible state

The second rail is that the agent's progress has to be visible — to humans and to other agents — at every step.

The four-hour stall I opened with was, in retrospect, a visibility problem. The agent had a runtime. The runtime had logs. But the wrapper that invoked the agent didn't surface those logs to the human, and the human had no other signal to check. "It said it would notify me" became the only available status, and that status was a lie.

We fix this with three habits.

First, **every non-trivial agent run gets its own git worktree** under a known path (we use `.claude/worktrees/<run-id>/`). One agent, one tree. Parallel runs get parallel trees. No two writers ever share a tree, because workspace bleed is a category of bug that doesn't surface in tests — it surfaces in a teammate's "wait, why is that file in this branch?" message a day later. Worktrees are nearly free in git. The bleed is not.

Second, **the agent appends a one-line status to a flat file** — `AGENT_COMMS.log` at the repo root — whenever it transitions state (started, blocked, finished, handed off). That file is the team's tail-friendly status board. `tail -f AGENT_COMMS.log` from any terminal tells you what every active agent thinks it's doing. When something stalls, the absence of new lines is the signal.

Third, **incidents leave a paper trail**. When an agent run times out, the watchdog dumps a directory under `.claude/incidents/<run-id>/` with the last 500 lines of output, the working-directory diff, and the runtime metadata. That directory is what a human looks at when they take the work back, and it's what the next agent reads if the task is retried.

None of this is fancy. It's the same observability discipline you'd want around any background worker. The novelty is just remembering that an AI agent is a background worker, and that "the chat window says it's done" is not a status check.

There's a second-order benefit, too. Visible state is what makes the loop debuggable specifically. When something goes sideways, you have an artifact to point at — *here's the commit it landed on, here's the comms-log line that said it was done, here's the diff that proves it wasn't.* That's the difference between "the AI is unreliable" (a vibe) and "this specific run timed out at this specific step, and here's what to do about it" (a fix).

## Rail 3: independent review

The third rail is the one that takes the longest to internalize: the agent that wrote the code does not approve it.

This rule exists because the same model that writes the code is also the one most likely to rationalize it. Ask an agent to review its own PR and you'll get a thoughtful checklist, a "looks good to me," and a missed bug that a fresh pair of eyes would have caught in fifteen seconds. The agent isn't lying — it's just not the right reviewer for its own work. The same way human engineers aren't.

So we put a gate in front of every PR. The gate has three layers, applied in order — cheap first, expensive last.

**The deterministic layer goes first.** Format, lint, type check, static analysis, automated tests. These catch the things that are obviously wrong before any reviewer — agent or human — wastes a minute on them. None of it requires judgment, all of it runs in seconds, and an agent that consistently produces work that fails these checks is an agent that needs its prompt rewritten, not its output reviewed. We don't ship a PR — agent-written or otherwise — that hasn't cleared the deterministic gate locally. CI is for confirming, not for discovering.

**For low-risk changes** — content edits, isolated refactors, dependency bumps — a second agent reviews above the deterministic layer. Same model, different context window, different system prompt focused on diff review. It catches roughly the same class of issues a junior reviewer would: a missing test, an obviously wrong assumption, a function that shadows another, an Edit that didn't actually apply because the file changed mid-chain. Of the agent-on-agent reviews we've run in the last three months, the reviewer agent blocked a non-trivial issue on roughly a third of the PRs. The other two-thirds it stamped approve, and the humans agreed.

**For higher-risk changes** — schema changes, anything touching auth, any public-API surface — a human reviews, full stop. The reviewer agent's first job there is to summarize the diff for the human, not to gate it. We're not trying to take humans out of the loop. We're trying to spend their attention where it matters.

The discipline that makes this work is matching the gate to the risk. Putting a human in front of every dependency bump burns trust and goodwill. Putting a reviewer agent in front of a schema migration is malpractice. The team has to be honest about which is which — and the issue's labels are usually a good proxy. A `feat:` issue with a `security` label gets a human. A `chore(deps):` gets the agent.

One sharp edge worth naming: reviewing AI-written code is still real engineering work. We've seen typecheck failures slip past the reviewer agent. We've seen dynamic-import shims that worked in dev and exploded in the test runner. We've seen named-vs-default export drift in a dependency that the agent didn't think to verify. Don't ship AI work without the gate, and don't trust the gate to substitute for the deterministic layer underneath — format, lint, build, test, all four, in order, before the PR goes up.

## What happens when you skip a rail

Each rail prevents a specific failure mode. Skipping one doesn't break the loop immediately — it just shifts the cost downstream, where the cleanup is more expensive.

**Skip bounded scope and you get scope drift.** The agent ships a PR that's technically correct against the request as stated and architecturally wrong against the codebase as it exists. Cleanup is a rewrite, not a fixup.

**Skip visible state and you get silent stalls.** The agent reports done. The agent is not done. You find out by accident — a teammate notices the file in the wrong branch, or a CI run goes red on something that should have been caught locally. The recovery cost scales with how long the lie has been in flight.

**Skip independent review and you get rationalized bugs.** The agent's PR description sounds confident. The diff looks plausible. The bug ships. Production catches it, which is the worst possible place to catch it.

The rails are cheap. Writing a good issue takes ten minutes. Worktrees take one command. A reviewer agent runs in a couple of minutes. The alternative — chasing down half-shipped work after the fact — is the most expensive way to use the model.

## A note on the failure modes that don't have a rail yet

We're being honest about the rails we have. Things are still a little squishy in a few spots.

The reviewer-agent gate works well on small diffs and gets less reliable on diffs over about 400 lines — the reviewer's context budget starts losing the thread. We're experimenting with structured plan-then-diff reviews to fix that, but it's not solved.

Cross-PR coordination — two agents working on adjacent issues that conflict in the same file — is still mostly a human's job. We've been filing pre-flight conflict notes on issues that touch shared surfaces, but the loop isn't tight yet.

And the agent's own self-reporting is improving, but it's still the place we trust least. The comms log and the watchdog are how we work around it. The day we trust the agent to say "I'm stuck" honestly is probably the day we can drop a rail. We're not there.

## The loop, briefly

Three rails. Each cheap. Each prevents a specific, expensive failure mode. The agent's speed compounds into team throughput exactly when those rails are in place, and decays into team liability the moment any one of them is missing.

If you're running an AI development loop today and the work is shipping clean, you probably already have these — possibly under different names. If the work is shipping rough, the question to ask is which rail is missing, not which model to try next.

Want to talk through your own loop? [Let&rsquo;s talk](/contact-us/).

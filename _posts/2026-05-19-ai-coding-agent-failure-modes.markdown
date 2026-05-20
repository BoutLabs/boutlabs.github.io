---
layout: post
title:  "A field guide to AI coding-agent failure modes"
date:   2026-05-19 09:00:00 -0400
categories: [news]
tags: [ai-enablement, engineering]
hero: /assets/images/posts/ai-coding-agent-failure-modes-header.jpg
---

The first time we lost four hours to a silent stall, it felt like a fluke. The second time it happened, we named it. The third time, we had a watchdog wired up and a one-line entry in `AGENT_COMMS.log` told us within ninety seconds where the run was actually parked. That's the difference naming makes — "the AI is being weird" becomes "this is a silent stall, here's the recovery move," and the conversation gets twenty minutes shorter.

After about a year of running coding agents against real BoutLabs work — an iOS app, a couple of small web services, this site, a few client engagements that won't be named here — the same handful of failure modes have shown up over and over. They have shapes. They have tells. They have recovery patterns. This is the field guide we wish we'd had a year ago.

A word on what this post is not. It's not a list of model bugs. The frontier models change every few months, and the bug list churns with them. The failure modes below are about the *loop* — what happens when a probabilistic worker drives a deterministic toolchain. Those failures are mostly invariant under model upgrades, which is why naming them is worth the trouble.

## Why a taxonomy matters

The cheap reason is shared vocabulary. When a teammate says "I think the agent is in a tool-call loop on the auth refactor," everyone on the call knows what to check first. The diagnostic conversation gets specific in a way that "Claude is acting weird" never does.

The deeper reason is that named failures invite escape hatches. Once a failure has a name, the team can decide whether to write a guardrail for it, route around it, or accept the cost and move on. Unnamed failures get rediscovered every Tuesday. Named ones get a slot in the loop's design — a watchdog, a comms-log line, a pre-flight check — and stop costing real time.

Most of these failures share a property worth saying up front: they are *quiet*. The bug isn't usually a crash. It's a confidently-wrong report that looks correct until someone checks the artifact. Build for that.

## The named failures

### Silent stall

**The tell.** The agent reports it's running. Then nothing. No output, no error, no commit. The chat window says "I'll notify you when it's done." It doesn't.

**Where it shows up.** Long-running sandboxed runs, especially through wrapper agents that delegate to a sub-runtime. The wrapper's "background" notification path is unreliable, so the parent never hears that the child stalled mid-step. We've seen this most often with Codex CLI invoked from inside another agent.

**The recovery move.** Set a watchdog timeout on every non-trivial run. Ours dumps the last 500 lines of output, the working-directory diff, and the runtime metadata to `.claude/incidents/<run-id>/` on timeout. From there you can decide whether to resume, restart, or fall back to implementing inline. The other half of the recovery is structural: one-line state transitions to a flat `AGENT_COMMS.log` so the absence of new lines is itself a signal.

### Eager refactor

**The tell.** You asked the agent to fix one function. The diff touches eleven files. Most of the extra changes are reasonable in isolation — a variable renamed for clarity, a helper extracted, a couple of comments tidied. None of them are what you asked for.

**Where it shows up.** Underspecified issues with a vague file list, or issues that don't include an explicit out-of-scope section. The agent reads the request, infers a broader intent than you held, and starts "improving" adjacent code. Most of the time the changes are fine. Some of the time they break naming conventions, conflict with an in-flight branch, or introduce abstractions the codebase had deliberately avoided.

**The recovery move.** Two layers. At review time, scope-shrink the PR before merge — `git reset` the unscoped files and ask the agent to re-PR with the original task only. At issue-write time, add an explicit *out of scope* section to every issue. Counterintuitively, the out-of-scope field is more important than the file list. It's the place where you tell the agent which adjacent improvements *not* to make. Discovered work becomes a new issue, not a bigger PR.

### Hallucinated API

**The tell.** The code looks right. It imports a function that sounds like it should exist. It does not exist. The test run blows up on an import error, or — worse — the function name shadows a real one and the call silently returns the wrong shape.

**Where it shows up.** Libraries with overlapping naming patterns, recently-renamed methods, or any library whose major-version migration changed import paths. Also common when the agent is reaching for a method it half-remembers from a sibling library — `lodash.chunk` showing up in a project that only has `ramda`, that flavor.

**The recovery move.** Make this a deterministic-layer problem, not a review problem. Format, lint, and type-check on every PR — see the [deterministic-checks rail](/news/2026/05/19/three-rails-ai-loop/) — and an agent that consistently hallucinates APIs is one whose prompt needs to say "read the actual imports before you write the call." If the hallucination is in a test mock and the test still passes, you have a different kind of problem; this is one place where mutation testing pays for itself.

### Confident-but-wrong assertion

**The tell.** The chat window says "all green, tests pass, PR is up." Check the artifact: the PR isn't open, or it's open with no commits, or the tests didn't actually run, or one of the Edits in the chain failed and the agent didn't notice. The summary message and the reality have drifted.

**Where it shows up.** Long, chained tool-use sequences where an early step fails silently and downstream steps run against stale state. We saw this in PR #55 of an internal project — the CHANGELOG entry didn't make it in because an Edit failed mid-chain and the commit went up anyway. The agent's final message was "shipped, here's the link."

**The recovery move.** Verify the mutation, not the message. Every state-changing claim in the agent's transcript should be checkable against an artifact — `git log`, `gh pr view`, a file diff, the GitHub API. We added a small `verify.sh` helper to our loop that registers each mutation claim and confirms it landed before the run ends. When the message and the artifact disagree, trust the artifact. Always.

### Worktree bleed

**The tell.** A file shows up in the wrong branch. Or two PRs both contain the same unrelated change. Or a teammate asks "wait, why did the auth refactor land in the marketing-site PR?"

**Where it shows up.** Parallel agent runs sharing one working tree. Each agent thinks it has the directory to itself. They don't. The git index is shared state, and two writers stomping on it produce branches with each other's uncommitted work mixed in. We've also seen the simpler variant — one agent runs commands from the repo root when it thinks it's in a worktree subdirectory.

**The recovery move.** One agent, one worktree. Every non-trivial run gets its own tree under a known path — we use `.claude/worktrees/<run-id>/`. The agent confirms `pwd` and `git branch --show-current` *before* its first edit; if either looks wrong, switch before touching anything. Worktrees are nearly free in git. The bleed is not. When it does happen, the cleanup is usually a careful `git restore --source` per file, not a reset — you want to keep the work, just untangle it.

### Context-window amnesia

**The tell.** Three quarters of the way through a long session, the agent forgets a constraint you gave it at the top. The instruction reappears at the bottom of the transcript, sometimes verbatim, as if discovered fresh. Style guides drift. The voice rule you established in turn three is gone by turn forty.

**Where it shows up.** Long-running tasks that exceed the model's effective working memory — which is usually well below the advertised context window. Also common when the system prompt is large and competes with the task for attention. Multi-step refactors are the prime offender.

**The recovery move.** Externalize the constraints. Anything you'd be unhappy to see violated goes in a project file the agent re-reads at every meaningful checkpoint — `CLAUDE.md`, a `VOICE.md`, an issue body's acceptance-criteria block. The discipline isn't to remind the agent; it's to make the constraint a re-readable artifact instead of a chat message. The corollary: keep sessions shorter than you think. A fresh session that re-reads the context is usually faster than a long session that's lost the thread.

### Sandbox-policy block

**The tell.** The agent says the file is written. The file isn't there. Or the agent reports a permission denied error, retries, reports success, and the file still isn't there. The wrapper says "completed." The disk disagrees.

**Where it shows up.** Codex-flavored sandboxes that restrict writes outside the main repo root, and especially sibling git worktrees that the sandbox policy doesn't reach. We've also seen this with MCP filesystem servers configured against a narrower path than the agent expected.

**The recovery move.** Pre-flight the path. Before delegating any write-heavy task to a sandboxed runtime, confirm the target directory is on the runtime's allowed list — most runtimes will tell you if you ask. When it does happen, fall back to inline implementation rather than retrying the same sandbox call. We learned the hard way that "the recovery overhead can exceed the cost of just implementing inline" is the right framing; budget time for verification, then make the cheap call.

## What the failures have in common

Six of the seven above are *quiet failures*. The agent doesn't crash. It doesn't shout. It writes a confident summary, and the summary doesn't match the artifact. The exception is the hallucinated API, which usually announces itself loudly at test time — and is also the one we worry about least, because the deterministic layer catches it.

That asymmetry is the load-bearing observation in this whole post. The expensive failures are the ones that look like success. They're expensive precisely because the human signal — "the chat says it's done" — is the wrong signal. The right signal is the artifact, and the work of an AI development loop is mostly about making that artifact visible, diffable, and verifiable.

A related point: most of these are not model bugs. They're integration bugs between a probabilistic worker and a deterministic toolchain. A better model helps a little. A better loop helps a lot more. Which is why the rest of this series has spent so much time on harnesses and guardrails — the model isn't the bottleneck.

## Building for these

Each failure above has a structural answer in the loop:

- **Silent stalls** are answered by watchdogs and a flat comms log.
- **Eager refactors** are answered by tight issues with explicit out-of-scope sections.
- **Hallucinated APIs** are answered by the [deterministic-checks rail](/news/2026/05/19/three-rails-ai-loop/) — format, lint, type, test, every PR.
- **Confident-but-wrong assertions** are answered by verifying mutations against artifacts rather than transcripts.
- **Worktree bleed** is answered by one-agent-one-tree, every time.
- **Context-window amnesia** is answered by externalized constraints in re-readable project files.
- **Sandbox-policy blocks** are answered by pre-flighting paths and falling back to inline implementation when the sandbox is the wrong tool.

None of this is novel. It's the same observability and review discipline you'd want around any background worker that ships code. The novelty is just remembering that an AI agent is a background worker, and that the chat window's summary is not a status check. The [independent-review rail](/news/2026/05/19/three-rails-ai-loop/) is the other half of that — the agent that wrote the code does not approve it, because the model that produced the work is also the one most likely to rationalize it.

A last bit of honest framing: this list is incomplete. Two failure modes we're watching but haven't named cleanly yet are *reviewer-agent fatigue* on diffs over about 400 lines, where the reviewer's context budget loses the thread, and *cross-PR conflict drift*, where two agents working on adjacent issues touch the same file without coordination. We have workarounds for both — structured plan-then-diff reviews, pre-flight conflict notes on shared-surface issues — but the names aren't earned yet. We'll come back to them when they are.

If you're running an AI development loop today and a failure on this list sounds familiar but the recovery move doesn't, [let's talk](/contact-us/). Specifically.

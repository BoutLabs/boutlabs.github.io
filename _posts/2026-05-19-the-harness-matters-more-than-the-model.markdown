---
layout: post
title:  "The harness matters more than the model"
date:   2026-05-19 09:00:00 -0400
categories: [news]
tags: [ai-enablement, technology, engineering]
---

Two agents, same model, same prompt — one ships the change and reports back in 14 minutes, the other quietly idles in a worktree for an hour and leaves uncommitted files spread across two branches. The only difference between them is the harness. That experience has repeated enough across Bout Labs work over the last six months that we have stopped recommending coding tools by model and started recommending them by harness — Claude Code, Cursor, Codex CLI, Aider, Continue, and whatever ships next.

This is the post that argues why.

## The model is not the bottleneck

Most "which AI tool should I use" conversations spend 80% of their time on the model — Claude vs. GPT vs. Gemini, benchmarks, context window length, the latest evals. In practice, for actual day-to-day coding work, the frontier models are roughly interchangeable. They all hallucinate APIs that don't exist. They all write a perfectly reasonable function that calls a perfectly imaginary library. They all need to be told to read a file before they edit it.

What is not interchangeable is the harness sitting around the model. The harness is the part that decides *when* to call the model, *what* context to give it, *which* tools it can reach for, and *what to do when something goes wrong*. The model generates tokens. The harness runs the actual engineering workflow.

If you have been frustrated by an AI coding tool, the odds are very high that you were frustrated by the harness — not the model behind it.

## What the harness actually does

Strip away the marketing and a coding harness is doing about seven things, all of them load-bearing:

- **Context assembly.** Reading the right files, in the right order, before the model sees the prompt. Some harnesses do this with a watcher and a live index; some do it on demand; some make you paste the file in by hand.
- **Tool orchestration.** Shell, file I/O, search, git, network. Plus the ergonomics of extending the surface — Model Context Protocol servers, custom tools, plugins. The model can only do what the harness exposes.
- **Loop control.** When the model returns a tool call, does the harness execute it and feed the result back? In a tight enough loop to feel responsive, but not so tight it burns 30,000 tokens on a hallucinated grep? That choice — when to call the model again versus when to stop and ask — is most of the difference between a useful agent and an expensive one.
- **Context window management.** What does the harness do when the conversation gets long? Truncate? Summarize? Hand off to a subagent with a clean window? Each option has a failure mode.
- **Error handling.** A command fails. A test times out. A file does not exist. The harness has to notice, surface, and either retry sensibly or hand back to a human.
- **Visibility.** Can you see what it is doing in real time, or are you watching a spinner? When it gets stuck, does it tell you it is stuck?
- **Recovery.** When the agent goes off the rails — and it will — how cleanly can you undo, take over, or steer? Worktrees, branches, git state, partial commits, half-applied edits. The harness either keeps this hygienic or it does not.

A model that scores 90 on a benchmark inside a harness that loses context every 12 turns ships worse code than a model that scores 85 inside a harness that holds context cleanly through a four-hour session. We have watched this exact substitution play out, more than once.

## The dimensions that actually separate harnesses

Once you stop comparing harnesses by their underlying model, the comparison gets sharper. These are the dimensions we use in practice when we are picking one for a client engagement.

### Failure modes

Every harness fails. The question is *how*. When the model hallucinates a function name, does the harness blindly write it and hand you a broken file, or does it run the test suite and notice? When a long-running command hangs, does the harness time it out, or does it sit forever? When a tool returns garbage — a wall of `ls -la` output, say — does the harness know how to keep its head?

Good harnesses fail loudly, with a clean enough state that you can take over. Rough harnesses fail quietly. The quiet failures cost more, every time.

### Visibility

This one is underrated. We have lost real hours to harnesses that report "running in the background, I will notify you" and then never produce a second notification. The agent has either finished, stalled, or crashed — and you cannot tell which without going to look.

The fix is mundane: streaming output, a status indicator that updates as the agent does work, a clear "I am stuck on X, please advise" hand-back when something goes wrong. Most of the perceived productivity gap between two harnesses on the same model comes down to whether you ever have to wonder if the agent is still alive.

### Context discipline

Long sessions are where harnesses split. A four-hour session, two file rewrites, a test failure, a debug detour, and a new feature request — what is still in the context window? The good harnesses know when to summarize, when to drop, when to re-read a file from disk because the in-memory version is stale. The rougher ones lose track of which file is current, edit the wrong version, and overwrite work the developer just did.

The most expensive bug in this category is silent: the agent's mental model of the code drifts away from the code on disk, and the agent does not notice. By the time you notice, you are unwinding 40 minutes of commits.

### Tool surface

Built-in tools matter — file I/O, shell, search, edit, git — but so does the ergonomics of *adding* tools. The Model Context Protocol ecosystem has made this dramatically less painful in the last year, but harness support is uneven. A harness that lets you wire up a Postgres MCP server and a GitHub MCP server in five minutes is a different product from one that requires a custom plugin written in TypeScript.

For our work specifically, the ability to reach external systems — issue trackers, design tools, observability backends — is closer to load-bearing than nice-to-have. The harness is the integration layer.

### Recovery

When the agent does something you did not want — and again, it will — the harness either makes recovery easy or makes it hostile. Easy looks like: agent operates inside a git worktree, every edit is a discrete commit, and "undo this 20 minutes of work" is `git reset` to a known-good SHA. Hostile looks like: uncommitted edits across three files, a half-applied patch in the shell, and a working tree you no longer trust.

We bias toward harnesses that treat git state as a first-class concern. Worktrees, atomic commits, branch-per-task. The recovery story is the part you do not appreciate until you need it, and by then it is too late.

## A field-tested take on a few current harnesses

Specific, not abstract. These are observations from real engagements over the last six months, not vibes from a benchmark.

### Claude Code (Anthropic)

The primary harness for most of our work. Anthropic's [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) is a terminal-first agent with strong context discipline, clean tool orchestration, and a recovery model built around worktrees and atomic commits. The visibility story is excellent — you can see what it is doing as it does it, and when it is uncertain it asks instead of guessing.

Where it has burned us: tool-call loops on ambiguous prompts can get expensive if you do not steer early. A vague "fix the build" can spend 15 minutes reading files before it tries anything. The fix is mostly on the prompter — be specific about what you want first — but a harness that defaulted to "ask before exploring" would save tokens. Subagent fan-out across worktrees is powerful but takes practice to use without creating cross-tree confusion; we have written more than one runbook to keep that clean.

Net: this is the harness we reach for when reliability matters. It rarely surprises us, and when it does, it surprises us by being more careful than we asked for, not less.

### Codex CLI (OpenAI)

We have been actively trying to find a workflow where Codex CLI carries well-specified implementation work in parallel with a Claude Code session. The hypothesis is sound — push "grunt work" to a second harness, preserve the primary session's context for judgement. The execution has been rough.

Specifically: Codex CLI has stalled silently on multi-step refactors, returning a "running in the background" message that was never followed by a completion notification. We have lost time waiting for runs that had already failed. The sandbox path policy can block writes outside the main repo root, which makes sibling-worktree workflows brittle — the agent reports the failure, but the wrapper sometimes still reports "completed." And running multiple Codex sessions sharing one working tree has produced workspace bleed: files from one ticket showing up in another ticket's branch.

None of this is a verdict that Codex CLI is bad. It is a verdict that the failure modes we have hit are the ones that cost the most to recover from — silent stalls and state confusion — and the recovery overhead has, on the runs we have measured, exceeded the cost of just implementing the work inline. We are still looking for the invocation pattern that works for us. If you have one, we would like to compare notes.

### Cursor

Cursor's bet is different: keep the IDE, add an agent that can read, edit, and reason about the codebase from inside it. The integration is excellent for the solo-developer-in-an-editor case. You can highlight a function, ask for a refactor, see the diff inline, accept or reject by chunk. For the kind of work that lives in one repo and one developer's head, that loop is hard to beat.

Where it stretches: multi-repo work, long-running multi-step refactors, and anything that wants a subagent to fan out across files in parallel. The IDE-anchored model is a feature when it fits and a constraint when it does not. The Cursor team has been moving toward more agentic capabilities — that is a separate conversation we will be having when the next iteration ships.

Net: a strong solo-pair harness for IDE-resident developers. We reach for it when the work is bounded and visual feedback matters more than orchestration.

### Aider

Aider is the unfussy option — a [terminal-first agent](https://github.com/Aider-AI/aider) with explicit, declarative context (you tell it which files it can see), a tight edit-test-commit loop, and a refreshingly small surface area. For a developer who already lives in the terminal and wants a coding agent that does the obvious thing without much ceremony, Aider is the right answer surprisingly often.

Where it does less than Claude Code or Cursor: it does not fan out to subagents, it does not orchestrate large multi-file changes the way a heavier harness can, and the tool-surface story is narrower. That is the point. If your work is single-developer, single-repo, and benefits from the developer keeping a tight grip on context, that minimalism is a feature.

### Continue

Continue is the open-source IDE extension that runs across editors and supports a wide range of models. For teams that want a self-hostable, swap-the-model option and are willing to invest in configuration, it slots in cleanly. We have less direct production time with it than with the others above; the right time to recommend it is when the team has firm requirements around hosting, model choice, or governance that the closed harnesses cannot meet.

## The picks for different shapes of work

There is no single best harness — there is a best harness for a given shape of work. The four shapes we see most often:

- **Solo IDE pair, single repo.** Cursor or Continue, in that order if you do not need to self-host the model. The IDE-resident agent is the right tool when the work is bounded and visual feedback matters.
- **Terminal-first multi-step engineering.** Claude Code, with Aider as the lower-ceremony alternative when the scope is tight. This is where most of our client engagement work happens.
- **Single-shot CLI tools.** Both Claude and OpenAI have minimal "ask the model from the shell" interfaces, and these are useful for one-off scripts, code translation, and quick refactors. Not where you want to run an agent.
- **Parallel multi-agent work across worktrees.** This is still squishy. Claude Code with subagent fan-out is the most reliable pattern we have found, but the orchestration overhead is non-trivial. Codex CLI as a second worker has been rough for the reasons above. The "robot army of coding agents" pattern is real, but it is real for teams who have invested in the harness scaffolding around it — not as a default.

The honest summary: pick the harness that matches the shape of the work, not the model that scored highest on the most recent benchmark. The model is the easy part of the decision. The harness is the part that will decide whether your team gets faster or just feels busier.

## The thing nobody tells you

The most expensive harness mistake is not picking the wrong one. It is treating the harness as a vendor lock-in question — picking one, sticking to it, and trying to make it carry every shape of work in every project.

We use multiple harnesses, deliberately. The terminal agent for engineering. The IDE pair for tight refactors. The minimal CLI for one-shots. The harness is part of the workflow, not part of the identity, and the cost of switching is much lower than the cost of forcing the wrong tool against the wrong job.

The model behind the harness will keep getting better. That is the part that is on a fast curve and largely outside your control. The harness — the part that runs the actual workflow around the model — is the part where your team's judgement compounds. Spend time there. Try things. Notice what fails quietly and which tools recover gracefully.

If you are figuring out which harness fits your team and your codebase, [let's talk](/contact-us/). We have opinions, and we have receipts.

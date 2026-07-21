---
layout: post
title:  "How we vet an MCP server before it touches a client's codebase"
date:   2026-07-21 09:00:00 -0400
categories: [news]
tags: [ai-enablement, mcp, security, tooling]
hero: /assets/images/posts/vetting-mcp-servers-header.jpg
---

Every MCP server you install is a program with unreviewed access to whatever the agent can already reach — your filesystem, your git credentials, your production database if you've been careless about scoping. Most teams install them the way they installed npm packages in 2016: the README looked fine, the demo worked, `npm install` and move on.

That trust model didn't survive contact with the npm ecosystem. Typosquatted packages, compromised maintainer accounts, install scripts that phoned home — all of it happened, repeatedly, for a decade, before package registries started taking supply-chain review seriously. The agent-tool ecosystem is running the same experiment again, faster, with more privilege on the table. An MCP server doesn't just run in your build pipeline. It runs *inside the loop the agent uses to make decisions*, with tool descriptions the model trusts by default and, often, filesystem or network access nobody scoped down.

We wrote about [which MCP servers are worth installing](/news/2026/05/19/mcp-servers-worth-installing/) a couple months back. This is the other half — the process we run before any of them get near a client's repo.

## What we're actually checking

Static analysis and registry metadata. Never execute the code to find out what it does — that's the whole point. A few specific things move the needle more than the rest combined:

**Does the install script reach the network before you've asked it to do anything?** A `postinstall` hook that phones home during `npm install` — before the tool has done a single useful thing — is one of the oldest supply-chain tricks in the book, and it still works because almost nobody reads `package.json` scripts before running the install.

**Does the name look like a popular tool with one letter changed?** Typosquatting doesn't need to be clever. It needs one tired engineer at 11pm typing fast.

**Is the code obfuscated or minified with no source to justify it?** A build artifact with no visible source repo, or a repo where the published package doesn't match the visible commits, is a reason to stop, not a reason to dig harder.

**Does the maintainer have any history?** A GitHub account created the same week as a suspiciously well-polished MCP server release is a pattern worth naming, not a coincidence worth ignoring. Real maintainers have a commit history, other projects, and a presence that predates the tool you're looking at.

**Do the permissions match the pitch?** This is the one that catches the most in practice. A "markdown formatter" MCP that requests full filesystem write and outbound network access is asking for more than the job requires. The gap between what a tool claims to do and what it's asking permission to do is the single most useful signal in the whole review — more useful than star count, more useful than how polished the README is.

## The question underneath all of it

Least-privilege thinking, applied to agent tooling the same way you'd apply it to an IAM role: what's the blast radius if this is malicious, and do I actually need that scope?

Most MCP installs skip this question entirely, because the friction is low and the demo is compelling. But the math is the same math you'd run before granting an AWS role `s3:*` when the job only ever needs `s3:GetObject` on one bucket. If a server only needs read access to a single directory, mounting it with write access to the whole filesystem is a decision, not a default — even when the vendor's setup docs make the broader grant the path of least resistance.

This is also where the [bounded-scope rail](/news/2026/05/19/three-rails-ai-loop/) extends past the issue an agent is working on and into the tools it's allowed to use to work on it. A tight issue with a loose tool belt is still a loose belt. Scope the task and scope the toolset — they're the same discipline pointed at two different surfaces.

## Where static review stops working

Here's the honest part. Static review catches a lot. It doesn't catch everything, and pretending otherwise is worse than not reviewing at all, because it buys false confidence.

A tool can behave exactly as advertised during review and change behavior later — a compromised maintainer account pushes a new version, a dependency gets swapped out from under a pinned-but-not-locked install, or the tool is genuinely well-behaved until a specific trigger condition flips it into something else. None of that shows up in a one-time static pass, because a one-time static pass is a snapshot, and the threat is a process.

The mitigation isn't "review harder." It's ongoing vigilance layered on top of the initial vet: pin versions instead of floating on `latest`, watch for supply-chain compromise disclosures the way you'd watch CVEs, and re-review on any version bump that touches permissions or install scripts — not just the ones that touch features. A server that asked for filesystem read on day one and quietly adds network access in a minor-version bump has told you something, if anyone's watching for it.

## What this looks like in practice

Before an MCP server, a Claude Code skill, or a plugin gets anywhere near a client's environment, it goes through the same static pass: install-script review, permission-versus-purpose check, maintainer and repo history, source-versus-artifact match. None of it requires running the code, and all of it is fast enough to do before the demo, not after the incident.

The rule of thumb that's saved the most time: if you can't articulate why a tool needs the access it's asking for, that's the review. You don't need a deeper static-analysis pass to catch a filesystem-write request on a tool that only reads markdown — you need to ask the question out loud.

Things are still a little unsettled at the edges of this. The MCP ecosystem doesn't yet have the equivalent of `npm audit` or a registry-level trust score, and every team is running some version of this review by hand. That's fine for now — the volume of tools any one team mounts is still small enough that hand review scales. It won't stay that way forever, and the tooling will need to catch up before it does.

If you're standing up an agent workflow and want a second set of eyes on what you're about to mount — especially anything touching credentials or a production surface — [let's talk](/contact-us/). Specifically about the blast radius, not just the demo.

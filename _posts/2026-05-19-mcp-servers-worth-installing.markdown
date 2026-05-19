---
layout: post
title:  "The MCP servers worth installing (and the ones that aren't)"
date:   2026-05-19 09:00:00 -0400
categories: [news]
tags: [ai-enablement, mcp, tooling]
---

The right three MCP servers will save you more time than the wrong fifteen. We've installed close to 40 different ones across client engagements in the last year, and the working set we keep coming back to is small — five, maybe six, depending on the project. Everything else either added noise to the agent's tool list, added auth complexity nobody wanted to maintain, or sat unused after the demo wore off.

That gap between "the demo looked great" and "we still have it installed three weeks later" is the only honest filter for an MCP server. So here is the field-tested list — what we keep, what we removed, and why.

## What MCP actually solves

Model Context Protocol — the spec Anthropic shipped in late 2024 — is a standard way for an LLM agent to talk to external tools and data. Before MCP, every agent harness baked its integrations in directly: a Claude Code plugin here, a Cursor extension there, a one-off LangChain tool somewhere else. The integrations didn't move between harnesses, and the harnesses didn't move between models.

MCP fixes that by separating the tool from the agent. An MCP server exposes a set of tools (function-callable verbs) and resources (readable context) over a small JSON-RPC protocol. Any MCP-aware client — Claude Code, Cursor, Continue, a custom SDK app — can mount that server and the agent gains the verbs.

The good news: the protocol is small and the ecosystem is real. The less-good news: the ecosystem is now in its hype-and-noise phase. There are hundreds of MCP servers in the wild as of early 2026, and most of them are toy demos, thin wrappers around an SDK that already worked fine, or marketing artifacts from a vendor who wanted to be in the conversation. The reference list at [modelcontextprotocol.io](https://modelcontextprotocol.io) is a starting point, not a buying guide.

## What we look for in an MCP server

Before naming names, the rubric. We install an MCP when it meets most of these:

- **Tight scope.** Five to fifteen well-named verbs, not fifty. An MCP that exposes every method of an SDK is dumping work on the model — the model still has to figure out which three verbs matter, on every turn.
- **Low token overhead at idle.** Every mounted server contributes its tool descriptions to the system prompt. A chatty server with 40 verbs and prose descriptions can quietly cost you 2,000–4,000 tokens of context on every turn, whether you use it or not. Multiply by however many servers are mounted and the math gets ugly fast.
- **Clear failure surfaces.** When the call fails, does the error tell the model what to do next, or does it dump a 200-line stack trace? Good MCPs fail with structured messages the model can route on.
- **Honest tool descriptions.** The description is the agent's documentation. We've seen MCPs where the description says "use this when you want to query the database" with no schema hints, no examples, and no constraints. The model guesses, the call fails, the turn wastes tokens.
- **Stateless or near-stateless.** MCPs that hold session state across calls — a logged-in browser, a transaction-mid-flight database connection — are fine for narrow use, but they're harder to recover from when the agent gets confused. Prefer servers where each call is self-contained.
- **The integration isn't already free.** If the harness already does the thing well — file reads, shell execution, basic web fetches — adding an MCP that duplicates it is pure noise.

That last criterion eliminates more candidates than the others combined. Most "filesystem MCP" or "shell MCP" servers are reinventing what Claude Code, Cursor, and the Anthropic SDK already do natively. Mounting them clutters the tool list without adding capability.

## The picks that earn their tool slot

These are the MCPs we install on most engagements. Not all five on every project — the right subset depends on what the agent is being asked to do.

### GitHub MCP

The one that ships value on day one. The [official GitHub MCP server](https://github.com/github/github-mcp-server) gives an agent the ability to read issues, create PRs, comment, list checks, merge, and search code across the org. We use it on every project that has any GitHub footprint, which is essentially all of them.

Specifically, the verbs that earn their place: `create_pull_request`, `issue_read`, `add_issue_comment`, `pull_request_read`, `search_code`, `list_pull_requests`. The PR-creation flow alone replaces 15 minutes of git-and-browser shuffling per ticket with a single tool call. Across a sprint, that adds up.

Where it falls short: the search verbs are noisy enough that the agent will sometimes prefer them over a faster local `grep`. We've started prompting agents to default to local code search and only reach for GitHub search when looking across repos. Not a problem with the MCP — a usage pattern worth knowing about.

Auth is a GitHub App installation token or a personal access token. App tokens are the right answer for anything that touches production repos; PATs are fine for sandboxes. Mint scripts that refresh the token on demand keep the auth invisible day-to-day.

### Filesystem MCP — only sometimes

The [reference filesystem server](https://github.com/modelcontextprotocol/servers) does what it says: scoped read and write under a root directory. Useful when the harness can't reach the relevant files itself, or when you want to give an agent access to a sibling directory outside the working tree.

For most engagements, we don't mount it. Claude Code's native file tools already cover the common case, and adding a second filesystem interface just gives the agent two ways to do the same thing — which it will inevitably interleave inconsistently. Where the filesystem MCP earns its slot is multi-repo work where the agent needs to read from one tree and write to another, or sandboxed environments where the native tools are scoped tighter than the workflow needs.

The sandboxing matters here. A filesystem MCP that escapes its root is a security problem; one that's too aggressive about its root is a productivity problem. Test the boundaries on day one, not when you're already in the weeds.

### Playwright MCP — the big one for browser work

If the agent needs to drive a browser at all — QA testing, scraping, dogfooding a deploy, taking annotated screenshots — the [Microsoft Playwright MCP server](https://github.com/microsoft/playwright-mcp) is the one to install. Stable verbs, real selector engine, screenshot support, console-and-network capture, dialog handling, file upload.

This is the MCP where the demo-to-real-use gap is smallest. The demos look great, and the production experience is also good. We've shipped client engagements where an agent runs full QA passes — navigate, interact, screenshot, diff against baseline, file a bug if anything regressed — using only Playwright MCP plus GitHub MCP. It works.

The trap to avoid: don't mount Playwright MCP and also a separate "browser-fetch" MCP and also a screenshot service. Pick one driver and let the agent get good at it. Layering three browser tools means the agent will pick the wrong one on every other turn.

### SQLite MCP — narrow but excellent

The [SQLite reference server](https://github.com/modelcontextprotocol/servers) is one of the underrated picks. Give an agent a SQLite file and the right verbs (`read_query`, `list_tables`, `describe_table`, optionally `write_query` in restricted mode), and it can do real exploratory data analysis without you piping CSVs through pandas by hand.

We use it on engagements that have local analytical workloads — log files dumped into SQLite, exported customer data, a copy-of-prod schema for development. The pattern that works: load the data once, mount the MCP read-only, let the agent explore the schema and write its own queries. Faster than describing the data shape in a prompt, more correct than asking the agent to guess.

The same approach extends to Postgres via the `postgres` MCP server, with the same caveat we apply to every database connection an agent touches: read-only credentials by default. Write access is a separate decision, made deliberately, with a path to undo what the agent does.

### Browser fetch / web search — pick one, mount it, move on

This is the most fungible slot. There are half a dozen "fetch this URL and return the content" MCPs, and they're roughly interchangeable. We've used [the reference `fetch` server](https://github.com/modelcontextprotocol/servers) on most engagements; it does what it says and gets out of the way.

The mistake we've watched teams make: mounting both a fetch MCP and a separate "browser search" MCP and a third "scraping" MCP. The agent picks one inconsistently, and you've spent three tool slots on what could be one. Pick a fetcher, accept its limits (most don't execute JavaScript — that's what Playwright is for), and stop shopping.

## The ones we've removed from our stacks

These are the MCPs that sounded great in the demo and didn't survive contact with real workflows. Not bad servers in isolation — wrong fit for most of the work we do.

### Slack MCP

The auth setup costs more than the workflow saves. Installing a Slack MCP means provisioning a bot user, granting channel scopes, managing the token, and then convincing the agent that "post a message" is a verb it should ever pick. In practice, the agent posts at the wrong moment, or in the wrong channel, or with a tone that doesn't match the team's. We've seen it work in one narrow case: a deploy bot that posts structured status updates to a single channel on a defined event. For anything more freeform, the failure modes are embarrassing and the value is marginal.

The honest framing: most "agent in Slack" workflows are better served by the agent writing a script that posts via the Slack API, run under human review, than by giving the agent a live posting verb.

### Email MCP

Same problem, higher stakes. An email send is a one-way door — once it's out, you can't unsend it. The agents we've worked with are good enough to draft email well; they're not yet reliable enough to be trusted with the send button on a corporate domain. We've removed email MCPs from every engagement we've tried them on. The draft-in-doc, review, send-from-the-human's-client pattern is slower and a lot harder to embarrass yourself with.

### X / social MCPs

We mounted one for two days on a brand-monitoring experiment. The verbs work; the workflows don't. Reading the social timeline gives the agent a steady stream of low-signal content that pollutes its context and biases its reasoning toward whatever's currently trending. Writing to social media has the same one-way-door problem as email, with a public audience. We removed it and never reinstalled.

There's a narrow case for read-only social MCPs in research workflows — pulling specific user timelines for a market analysis, for instance. But the same job is usually done better by an explicit script that pulls a defined slice, not by a live MCP the agent can call whenever it feels like it.

### Vector / embedding MCPs

This one is genuinely useful in the right setting and genuinely wasteful in most others. A vector-store MCP — over Pinecone, Weaviate, Chroma, or pgvector — gives the agent a retrieval verb against an indexed corpus. The setup cost is non-trivial: you have to build the corpus, choose an embedding model, manage updates as documents change, and tune the retrieval before it starts beating a plain keyword search.

For 80% of agent workflows in 2026, you don't need it. The model's native context is long enough for most documentation, and pointed file reads via the filesystem tools beat fuzzy retrieval when you know what you're looking for. We install a vector MCP when the corpus is genuinely large — internal wikis with thousands of pages, support ticket archives, codebases with hundreds of services — and skip it otherwise.

When you do install one, treat the corpus build as the actual project. The MCP is the easy part; the embeddings are where the work lives.

### Calendar, CRM, ticketing wrappers

These come in waves. Every quarter there's a new "Linear MCP" or "Notion MCP" or "Asana MCP" that promises to let the agent manage your work for you. We've tried several. The shape is always the same: the verbs cover the read path well and the write path badly, the agent's mental model of the tool drifts from the team's, and within a week somebody has to clean up a ticket the agent moved into the wrong column.

The pattern that does work: a read-only MCP that exposes the system as context (so the agent can answer questions about the team's work) paired with explicit human-in-the-loop for any write action. Most off-the-shelf wrappers don't split that boundary cleanly, which is why we've removed them.

## Operational notes

A few things that have surprised people on first-MCP installs:

- **Token overhead is real.** Every mounted MCP contributes its tool list to the system prompt on every turn. A "lightweight" server with verbose descriptions can cost more in steady-state tokens than its actual call volume justifies. Audit what's mounted; remove anything you haven't used in a week.
- **Auth is per-server.** There's no shared identity layer across MCPs. Each server you mount comes with its own token, scope, and refresh story. For anything touching production, this is where most of the setup time goes — and where most of the security review should go.
- **Sandboxing varies wildly.** Some MCPs run in-process with the agent; some run in a sandboxed subprocess; some run remote. The security model and the failure modes differ accordingly. Read the deployment doc before you mount one against a sensitive surface.
- **Tool descriptions are the contract.** If you find an MCP whose descriptions are vague, terse, or wrong, that's a sign of how the server will behave under pressure. Good MCPs treat their descriptions as part of the API. Bad ones treat them as afterthoughts.
- **The harness matters.** Claude Code, Cursor, and a custom SDK app will surface the same MCP differently. Test the server in the harness you actually use, not just in whatever demo environment the README assumes.

## The take

Fewer MCPs, picked specifically, beats more MCPs picked broadly. The five servers we install on most engagements — GitHub, Playwright, sometimes filesystem, sometimes SQLite, one fetcher — cover the workflows we actually run. Everything else has been a costume.

If you're standing up an agentic workflow for a real team, the question worth asking isn't "which MCPs should we install?" — it's "which two or three tools, if the agent had them and nothing else, would deliver the work we care about?" Start there. Install those. Resist mounting another until the agent has been doing the work for two weeks and you've watched what it actually reaches for.

We help teams think through that — what to install, what to skip, and how to wire it into a workflow that survives more than the demo. If you're somewhere on that road, [let's talk](/contact-us/). Happy to walk through how we'd approach yours.

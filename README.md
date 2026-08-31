# Grocery Shopping Agent Skill

A reusable, approval-gated agent workflow for maintaining a persistent grocery list, reviewing it on a schedule, finding current deals and coupons, and proposing sensible substitutions.

The agent prepares a review packet.
It does not place orders, submit payments, sign in to shopping accounts, or change account settings.

## What it does

- Maintains recurring, this-week, and one-time grocery items in structured data.
- Supports add, remove, edit, skip, and purchased operations without losing history.
- Runs a configurable weekly review and also supports on-demand checks.
- Compares item price, unit price, coupons, mandatory fees, basket coverage, and estimated delivered total.
- Proposes substitutions only when the item policy permits them.
- Records source URLs, timestamps, confidence, membership requirements, and coupon terms.
- Produces a compact approval queue before any external action.

## Repository layout

```text
.
|-- SKILL.md                       Agent instructions
|-- CLAUDE.md                      Claude-style entrypoint
|-- agents/openai.yaml             ChatGPT/Codex UI metadata
|-- config/grocery.example.json    Safe configuration example
|-- data/sample-grocery-list.json  Fictional grocery state
|-- data/sample-offers.json        Fictional price and coupon evidence
|-- schemas/                       JSON schemas
|-- references/                    Workflow and data-contract details
|-- examples/                      Prompts and a sample review packet
|-- scripts/validate_workspace.py  Dependency-free validator
|-- tests/                         Regression tests
`-- linkedin-post.md               Launch-post draft
```

## Quick start

1. Copy `config/grocery.example.json` to a private working location and edit the non-sensitive preferences.
2. Copy `data/sample-grocery-list.json` to a private state file and replace the fictional rows.
3. Run the validator.

```bash
python3 scripts/validate_workspace.py
python3 -m unittest discover -s tests -v
```

4. In a ChatGPT-style skill environment, install or reference this folder and invoke `$grocery-shopping-agent-skill`.
5. In a Claude-style project, keep `CLAUDE.md` at the repository root and ask Claude to follow the grocery workflow in `SKILL.md`.

Example request:

```text
Review my active grocery list for the next seven days.
Check current public deals, compare delivered totals, and show substitutions separately.
Do not place an order.
```

## Scheduling

The public example defaults to a weekly Saturday review.
The same workflow may run more frequently for price refreshes, but the order authority remains review-only.

Use the scheduler available in your agent environment to invoke a prompt such as:

```text
Use $grocery-shopping-agent-skill to perform the weekly review using my private config and grocery-state files.
Refresh current evidence, append history, and return the approval queue.
Do not place an order or sign in to a retailer.
```

## Safety model

The public repository contains only fictional sample data.
Store real grocery preferences, location details, retailer sessions, and payment data outside the repository.
Do not put an exact street address, access code, credentials, cookies, loyalty identifiers, or payment details in agent-readable state.

See [SECURITY.md](SECURITY.md) and [references/workflow.md](references/workflow.md) before connecting external services.

## Validation

The included validator checks required fields, schedule settings, item state, offer provenance, and common sensitive-key mistakes.
It intentionally uses only the Python standard library.

## Status

This is a release-quality workflow template, not a retailer integration or an autonomous purchasing bot.
Price, availability, taxes, tips, member pricing, and checkout eligibility can change and must be rechecked before purchase.

## License

MIT.

---
name: grocery-shopping-agent-skill
description: Maintain a persistent grocery list, run scheduled reviews, compare current deals and delivered costs, and propose policy-compliant substitutions without placing orders.
---

# Grocery Shopping Agent

Use this skill when the user wants to maintain, review, price-check, or optimize a grocery list.

## Non-negotiable boundaries

- Never place an order, submit payment, sign in, redeem a coupon, change a membership, or modify an external account unless the user separately requests that exact action and confirms it at action time.
- Treat the default workflow as research and review only.
- Never store credentials, cookies, exact street addresses, access codes, payment data, or loyalty identifiers in repository files.
- Never replace a user-owned preference with an inference.
- Never mark an item purchased or an order completed without direct confirmation.

## State ownership

The user-owned fields are item identity, desired state, cadence, quantity, preferred specification, substitution permission, limits, and notes.
Agent-owned fields are current offers, sources, availability, delivered-cost estimates, confidence, timestamps, recommendations, and run history.
Do not overwrite user-owned fields during research.

## Core workflow

1. Read the configuration, active grocery state, latest offer evidence, and prior review state.
2. Apply requested add, remove, edit, skip, or purchased operations while preserving an audit trail.
3. Determine the review horizon from the configured cadence and calculate target quantities from known consumption or explicit user rules.
4. If consumption is unknown, ask or flag the quantity for review instead of inventing a precise amount.
5. Research current price, package size, availability, coupon terms, membership requirements, mandatory fees, and source timestamps for active items.
6. Normalize item and delivered unit prices before comparing options.
7. Prefer a complete basket when practical and show a split-order alternative only when its savings exceed the configured threshold.
8. Consider a substitute only when the item permits substitutions and every protected attribute remains satisfied.
9. State package-size, quantity, quality, dietary, and price differences for every proposed substitute.
10. Produce a review packet with keep, buy, substitute, postpone, unavailable, and needs-input sections.
11. Append price evidence and a run summary without deleting prior evidence.
12. Stop at the approval queue.

## Deal and coupon evidence

Record the source URL, checked time, price, package size, retailer or service, availability, membership requirement, coupon value, expiration when known, and confidence.
Do not describe a promotion as current when its source is stale or its terms cannot be verified.
Keep tips separate from mandatory delivered cost.
Label taxes or checkout-only fees as estimates.

## Substitution decision rule

A candidate is eligible only when substitutions are allowed and it does not violate dietary, allergy, brand, quality, size, or use-case constraints.
Rank eligible candidates by delivered unit cost, basket coverage, confidence, and policy fit.
Require user approval when a protected attribute changes, the exact product is unavailable, or the price change exceeds the configured threshold.

## Weekly review output

Return:

1. Review period and evidence freshness.
2. Changes since the prior review.
3. Recommended basket with delivered total and coverage.
4. Coupons and deal conditions.
5. Substitution proposals shown separately.
6. Items requiring quantity or preference input.
7. Approval queue.
8. Actions explicitly not taken.

## Supporting references

- Read [references/workflow.md](references/workflow.md) for the full state transition and comparison process.
- Read [references/data-contract.md](references/data-contract.md) before changing state formats or connecting a data store.
- Use [examples/prompts.md](examples/prompts.md) for common invocations.

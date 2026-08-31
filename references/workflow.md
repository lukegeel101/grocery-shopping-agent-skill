# Workflow reference

## 1. Load and reconcile state

Read configuration, grocery state, latest offer evidence, and the previous review result.
Reject duplicate item IDs and preserve any unknown fields when updating a record.

Apply user commands as explicit operations:

- `add` creates a new item with a stable ID.
- `edit` changes only named user-owned fields.
- `remove` means deactivate unless the user explicitly requests permanent deletion.
- `skip` keeps the item but excludes it from the current review.
- `purchased` records the event and calculates the next expected review date.

## 2. Build the active horizon

The default review horizon comes from `review.lookahead_days`.
An item is active when it is included, not skipped, and due within the horizon.

Target quantity should use, in order:

1. An explicit user quantity for the review period.
2. A recorded consumption rate multiplied by the review horizon and safety factor.
3. A stable prior purchase cadence.
4. A `needs-input` flag when none of the above exists.

Do not create precise nutrition or consumption assumptions from a broad food description.

## 3. Collect evidence

For every active item and candidate service, record:

- Exact product and package size.
- Item price and visible coupon.
- Mandatory delivery and service fees.
- Checkout-only estimates kept separate.
- Availability and basket coverage.
- Source URL and checked timestamp.
- Membership or login requirement.
- Confidence and any unresolved ambiguity.

Expired, stale, or unverifiable promotions must not be used as current savings.

## 4. Compare like with like

Normalize package size into the item unit.
Calculate item unit price and estimated delivered unit price.
Allocate mandatory basket fees consistently and disclose the method.

Prefer a complete basket when the cost is competitive.
Show a split order only when it improves availability or exceeds the configured savings threshold after fees.

## 5. Evaluate substitutions

Reject a candidate when substitutions are disabled or a protected attribute fails.
Protected attributes can include allergens, dietary constraints, product form, quality tier, brand lock, minimum package size, or intended use.

For every eligible substitution, show:

- Original and candidate product.
- Package-size difference.
- Quantity difference across the review horizon.
- Delivered price and unit-price difference.
- Coupon and membership conditions.
- Confidence.
- Whether explicit approval is required.

## 6. Produce the review packet

The packet should answer:

- What changed since the prior run?
- What is due for the review horizon?
- Which complete basket has the best supported delivered total?
- Which deals have conditions or expirations?
- Which substitutions are proposed?
- Which items need user input?
- What requires approval?
- What external actions were not taken?

## 7. Persist the audit trail

Append price evidence and the run summary.
Do not rewrite old evidence to match new prices.
Mark stale evidence as stale rather than deleting it.


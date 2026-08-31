# Data contract

## Grocery state

The canonical state object contains a schema version, a non-identifying owner label, an update timestamp, and an item array.

Required item fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | Stable, non-secret item identifier |
| `name` | string | Human-readable item name |
| `state` | string | `recurring`, `this-week`, or `one-time` |
| `include` | boolean | Whether the current review includes the item |
| `cadence` | string | Expected review or purchase cadence |
| `target_days` | integer | Number of days the quantity should cover |
| `target_quantity` | number | Desired amount for the horizon |
| `unit` | string | Unit used for normalization |
| `allow_substitutions` | boolean | Whether alternatives may be proposed |
| `protected_attributes` | array | Attributes a substitute must preserve |

Optional user-owned fields include quantity on hand, reorder threshold, brand or specification, dietary tags, price limit, and notes.

## Offer evidence

Each offer record should contain:

| Field | Type | Meaning |
| --- | --- | --- |
| `item_id` | string | Grocery item being evaluated |
| `service` | string | Delivery service or retailer |
| `product` | string | Exact candidate product |
| `package_quantity` | number | Normalized package amount |
| `unit` | string | Unit matching the grocery item |
| `item_price` | number | Visible product price |
| `coupon_amount` | number | Supported discount amount |
| `mandatory_fees` | number | Allocated required fees |
| `estimated_delivered_price` | number | Price after supported coupon and mandatory fees |
| `availability` | string | `in-stock`, `low-stock`, `out-of-stock`, or `unknown` |
| `source_url` | string | Evidence URL |
| `checked_at` | string | ISO 8601 timestamp |
| `confidence` | string | `high`, `medium`, or `low` |

Tips should not be included in mandatory fees.
Taxes and checkout-only charges should be labeled as estimates.

## Run log

The run log is append-only.
Each entry should identify the review period, inputs used, evidence cutoff, recommendations, approvals needed, state changes, and actions not taken.


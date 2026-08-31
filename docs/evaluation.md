# Reproducible sample evaluation

The evaluation uses only fictional basket and offer data.

It compares three services across four required items, rejects incomplete baskets and rule-breaking substitutions, includes mandatory delivery fees, applies explicit coupons, and stops before any external action.

Run it with:

```bash
python3 scripts/evaluate_sample.py --check
```

## Committed result

| Metric | Result |
| --- | ---: |
| Services evaluated | 3 |
| Complete, rule-compliant services | 2 |
| Required-item coverage | 4 of 4 |
| Baseline delivered total | $36.75 |
| Best delivered total | $29.50 |
| Fictional estimated savings | $7.25, or 19.73% |
| Substitutions proposed for review | 2 |
| Protected-rule violations in selected basket | 0 |
| Orders or external actions taken | 0 |

The goal is reproducibility, not a claim about real retailer pricing.

Change the fixture, run the evaluation, and update the committed expected result only when the behavior change is intentional and reviewed.

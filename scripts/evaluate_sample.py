#!/usr/bin/env python3
"""Run a deterministic complete-basket evaluation on fictional data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "data" / "evaluation" / "sample-baskets.json"
EXPECTED_PATH = ROOT / "data" / "evaluation" / "expected-results.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    required = set(fixture["required_item_ids"])
    evaluated: list[dict[str, Any]] = []

    for service in fixture["services"]:
        available = {
            item["item_id"]: item
            for item in service["items"]
            if item["available"] and item["item_id"] in required
        }
        coverage = len(available)
        protected_violations = sum(
            1
            for item in available.values()
            if item["is_substitution"]
            and (not item["allow_substitutions"] or not item["protected_rule_passed"])
        )
        delivered_total = round(
            service["mandatory_fee"]
            + sum(max(0.0, item["price"] - item["coupon"]) for item in available.values()),
            2,
        )
        evaluated.append(
            {
                "service": service["name"],
                "coverage": coverage,
                "delivered_total": delivered_total,
                "protected_violations": protected_violations,
                "substitution_proposals": sum(1 for item in available.values() if item["is_substitution"]),
            }
        )

    eligible = [
        service
        for service in evaluated
        if service["coverage"] == len(required) and service["protected_violations"] == 0
    ]
    if not eligible:
        raise ValueError("The fixture has no complete, rule-compliant basket.")

    baseline = next(
        service for service in evaluated if service["service"] == fixture["baseline_service"]
    )
    best = min(eligible, key=lambda service: (service["delivered_total"], service["service"]))
    savings = round(baseline["delivered_total"] - best["delivered_total"], 2)
    savings_percent = round((savings / baseline["delivered_total"]) * 100, 2)

    return {
        "actions_taken": 0,
        "baseline_delivered_total": baseline["delivered_total"],
        "baseline_service": baseline["service"],
        "best_complete_service": best["service"],
        "best_delivered_total": best["delivered_total"],
        "complete_services": len(eligible),
        "protected_rule_violations": best["protected_violations"],
        "required_items": len(required),
        "savings_amount": savings,
        "savings_percent": savings_percent,
        "services_evaluated": len(evaluated),
        "substitution_proposals": best["substitution_proposals"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Compare output with the committed expected result.")
    args = parser.parse_args()

    result = evaluate_fixture(load_json(FIXTURE_PATH))
    print(json.dumps(result, indent=2, sort_keys=True))

    if args.check and result != load_json(EXPECTED_PATH):
        print("Evaluation output does not match data/evaluation/expected-results.json.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

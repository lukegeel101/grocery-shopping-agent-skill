#!/usr/bin/env python3
"""Validate the public grocery skill examples without third-party packages."""

from __future__ import annotations

import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "grocery.example.json"
LIST_PATH = ROOT / "data" / "sample-grocery-list.json"
OFFERS_PATH = ROOT / "data" / "sample-offers.json"

SENSITIVE_KEYS = {
    "account_number",
    "access_code",
    "api_key",
    "card_number",
    "cookie",
    "credential",
    "exact_address",
    "loyalty_number",
    "password",
    "payment_card",
    "routing_number",
    "secret",
    "session_token",
    "street_address",
    "token",
}

ITEM_STATES = {"recurring", "this-week", "one-time"}
AVAILABILITY = {"in-stock", "low-stock", "out-of-stock", "unknown"}
CONFIDENCE = {"high", "medium", "low"}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_iso8601(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return False
    return True


def find_sensitive_keys(value: Any, prefix: str = "root") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = key.lower().replace("-", "_").replace(" ", "_")
            if normalized in SENSITIVE_KEYS:
                errors.append(f"{prefix}.{key}: sensitive key is not allowed in public examples")
            errors.extend(find_sensitive_keys(child, f"{prefix}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(find_sensitive_keys(child, f"{prefix}[{index}]"))
    return errors


def validate_config(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if config.get("schema_version") != 1:
        errors.append("config.schema_version must be 1")
    location = config.get("delivery_location", {})
    if location.get("input") != "environment_variable":
        errors.append("config.delivery_location.input must be environment_variable in the public example")
    if location.get("environment_variable") != "GROCERY_DELIVERY_ADDRESS":
        errors.append("config.delivery_location.environment_variable must be GROCERY_DELIVERY_ADDRESS")
    if location.get("storage") != "runtime_only":
        errors.append("config.delivery_location.storage must be runtime_only")
    if "value" in location:
        errors.append("config.delivery_location must not contain an address value")
    review = config.get("review", {})
    if review.get("schedule") != "weekly":
        errors.append("config.review.schedule must be weekly in the public example")
    if not isinstance(review.get("lookahead_days"), int) or review["lookahead_days"] < 1:
        errors.append("config.review.lookahead_days must be a positive integer")
    authority = config.get("authority", {})
    for prohibited in ("sign_in", "place_order", "submit_payment", "change_account"):
        if authority.get(prohibited) is not False:
            errors.append(f"config.authority.{prohibited} must be false")
    errors.extend(find_sensitive_keys(config, "config"))
    return errors


def validate_items(state: dict[str, Any]) -> tuple[list[str], set[str], dict[str, str]]:
    errors: list[str] = []
    item_ids: set[str] = set()
    item_units: dict[str, str] = {}
    if state.get("schema_version") != 1:
        errors.append("grocery_state.schema_version must be 1")
    if not parse_iso8601(state.get("updated_at", "")):
        errors.append("grocery_state.updated_at must be an ISO 8601 timestamp")
    items = state.get("items")
    if not isinstance(items, list):
        return errors + ["grocery_state.items must be an array"], item_ids, item_units
    for index, item in enumerate(items):
        path = f"grocery_state.items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{path} must be an object")
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id.strip():
            errors.append(f"{path}.id must be a non-empty string")
        elif item_id in item_ids:
            errors.append(f"{path}.id duplicates {item_id}")
        else:
            item_ids.add(item_id)
        if item.get("state") not in ITEM_STATES:
            errors.append(f"{path}.state is invalid")
        if not isinstance(item.get("include"), bool):
            errors.append(f"{path}.include must be boolean")
        if not isinstance(item.get("target_days"), int) or item["target_days"] < 1:
            errors.append(f"{path}.target_days must be a positive integer")
        target = item.get("target_quantity")
        if not isinstance(target, (int, float)) or target <= 0:
            errors.append(f"{path}.target_quantity must be positive")
        unit = item.get("unit")
        if not isinstance(unit, str) or not unit.strip():
            errors.append(f"{path}.unit must be a non-empty string")
        elif isinstance(item_id, str):
            item_units[item_id] = unit
        if not isinstance(item.get("allow_substitutions"), bool):
            errors.append(f"{path}.allow_substitutions must be boolean")
        if not isinstance(item.get("protected_attributes"), list):
            errors.append(f"{path}.protected_attributes must be an array")
    errors.extend(find_sensitive_keys(state, "grocery_state"))
    return errors, item_ids, item_units


def validate_offers(
    evidence: dict[str, Any], item_ids: set[str], item_units: dict[str, str]
) -> list[str]:
    errors: list[str] = []
    if evidence.get("schema_version") != 1:
        errors.append("offer_evidence.schema_version must be 1")
    offers = evidence.get("offers")
    if not isinstance(offers, list):
        return errors + ["offer_evidence.offers must be an array"]
    for index, offer in enumerate(offers):
        path = f"offer_evidence.offers[{index}]"
        if not isinstance(offer, dict):
            errors.append(f"{path} must be an object")
            continue
        item_id = offer.get("item_id")
        if item_id not in item_ids:
            errors.append(f"{path}.item_id does not reference a grocery item")
        if item_id in item_units and offer.get("unit") != item_units[item_id]:
            errors.append(f"{path}.unit must match the grocery item unit")
        for field in ("package_quantity", "item_price", "coupon_amount", "mandatory_fees", "estimated_delivered_price"):
            value = offer.get(field)
            if not isinstance(value, (int, float)) or value < 0:
                errors.append(f"{path}.{field} must be a non-negative number")
        if all(isinstance(offer.get(field), (int, float)) for field in ("item_price", "coupon_amount", "mandatory_fees", "estimated_delivered_price")):
            expected = max(0.0, offer["item_price"] - offer["coupon_amount"]) + offer["mandatory_fees"]
            if not math.isclose(expected, offer["estimated_delivered_price"], abs_tol=0.01):
                errors.append(f"{path}.estimated_delivered_price does not match price, coupon, and fees")
        if offer.get("availability") not in AVAILABILITY:
            errors.append(f"{path}.availability is invalid")
        if offer.get("confidence") not in CONFIDENCE:
            errors.append(f"{path}.confidence is invalid")
        source_url = offer.get("source_url", "")
        if not isinstance(source_url, str) or not source_url.startswith(("https://", "http://")):
            errors.append(f"{path}.source_url must be an HTTP URL")
        if not parse_iso8601(offer.get("checked_at", "")):
            errors.append(f"{path}.checked_at must be an ISO 8601 timestamp")
    errors.extend(find_sensitive_keys(evidence, "offer_evidence"))
    return errors


def validate_workspace(
    config_path: Path = CONFIG_PATH,
    list_path: Path = LIST_PATH,
    offers_path: Path = OFFERS_PATH,
) -> list[str]:
    config = load_json(config_path)
    state = load_json(list_path)
    offers = load_json(offers_path)
    errors = validate_config(config)
    item_errors, item_ids, item_units = validate_items(state)
    errors.extend(item_errors)
    errors.extend(validate_offers(offers, item_ids, item_units))
    return errors


def main() -> int:
    errors = validate_workspace()
    if errors:
        print("Grocery workspace validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Grocery workspace validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

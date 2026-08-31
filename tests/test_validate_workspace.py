from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_workspace.py"
SPEC = importlib.util.spec_from_file_location("grocery_validator", MODULE_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class GroceryWorkspaceValidationTests(unittest.TestCase):
    def test_public_examples_are_valid(self) -> None:
        self.assertEqual([], VALIDATOR.validate_workspace())

    def test_sensitive_key_is_rejected(self) -> None:
        errors = VALIDATOR.find_sensitive_keys({"checkout": {"card_number": "sample"}})
        self.assertTrue(any("card_number" in error for error in errors))

    def test_bad_offer_total_is_rejected(self) -> None:
        state = VALIDATOR.load_json(VALIDATOR.LIST_PATH)
        _, item_ids, item_units = VALIDATOR.validate_items(state)
        evidence = VALIDATOR.load_json(VALIDATOR.OFFERS_PATH)
        evidence["offers"][0]["estimated_delivered_price"] = 999.0
        errors = VALIDATOR.validate_offers(evidence, item_ids, item_units)
        self.assertTrue(any("does not match" in error for error in errors))

    def test_file_entrypoint_accepts_explicit_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temp_root = Path(directory)
            config = VALIDATOR.load_json(VALIDATOR.CONFIG_PATH)
            state = VALIDATOR.load_json(VALIDATOR.LIST_PATH)
            offers = VALIDATOR.load_json(VALIDATOR.OFFERS_PATH)
            paths = []
            for name, value in (("config.json", config), ("state.json", state), ("offers.json", offers)):
                path = temp_root / name
                path.write_text(json.dumps(value), encoding="utf-8")
                paths.append(path)
            self.assertEqual([], VALIDATOR.validate_workspace(*paths))


if __name__ == "__main__":
    unittest.main()


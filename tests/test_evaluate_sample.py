import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "evaluate_sample.py"
SPEC = importlib.util.spec_from_file_location("grocery_evaluate_sample", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SampleEvaluationTests(unittest.TestCase):
    def test_evaluation_matches_expected_results(self) -> None:
        actual = MODULE.evaluate_fixture(MODULE.load_json(MODULE.FIXTURE_PATH))
        expected = MODULE.load_json(MODULE.EXPECTED_PATH)
        self.assertEqual(actual, expected)

    def test_incomplete_or_rule_breaking_service_cannot_win(self) -> None:
        actual = MODULE.evaluate_fixture(MODULE.load_json(MODULE.FIXTURE_PATH))
        self.assertEqual(actual["best_complete_service"], "Value Cart")
        self.assertEqual(actual["protected_rule_violations"], 0)


if __name__ == "__main__":
    unittest.main()

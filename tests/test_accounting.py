import unittest

from app import build_summary


class AccountingSummaryTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            {"entity": "JDG", "kind": "receivable", "currency": "PLN", "amount": 100},
            {"entity": "JDG", "kind": "payable", "currency": "PLN", "amount": 25},
            {"entity": "Co Ltd", "kind": "receivable", "currency": "THB", "amount": 500},
            {"entity": "Co Ltd", "kind": "missing_material", "currency": "THB", "amount": 0},
        ]

    def test_entities_are_isolated(self):
        summary = build_summary(self.records)
        self.assertEqual([entity["entity"] for entity in summary["entities"]], ["JDG", "Co Ltd"])
        self.assertEqual(summary["entities"][0]["currency_totals"]["PLN"]["receivable"], 100)
        self.assertNotIn("THB", summary["entities"][0]["currency_totals"])

    def test_currencies_are_not_combined(self):
        summary = build_summary(self.records)
        self.assertEqual(summary["entities"][1]["currency_totals"]["THB"]["receivable"], 500)
        self.assertEqual(summary["entities"][1]["currency_totals"]["THB"]["missing_materials"], 1)
        self.assertIn("explicit FX rate and date", summary["currency_note"])


if __name__ == "__main__":
    unittest.main()
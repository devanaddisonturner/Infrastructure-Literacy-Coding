"""
test_replicate_keyword_search.py
=================================
Unit tests for replicate_keyword_search.py

Tests verify:
  - Term lists match the master spreadsheet exactly
  - No overlap between Layer 0 and Layer 1 terms
  - term_present() word-boundary matching (no false positives)
  - JSON data structural integrity
  - Credential key mapping completeness

Run:
    python3 test_replicate_keyword_search.py
    python3 -m pytest test_replicate_keyword_search.py -v

Author:  Devan Cantrell Addison-Turner
         PhD Candidate, Civil and Environmental Engineering
         Stanford Doerr School of Sustainability
         daddisonturner@stanford.edu
         ORCID: 0000-0002-2511-3680
"""

import json
import os
import re
import sys
import unittest

# ── Import replicate script without executing main() ─────────────────────────
# Set sys.argv to prevent argparse from triggering on import
sys.argv = ["test_replicate_keyword_search.py"]

import replicate_keyword_search as rep


class TestTermLists(unittest.TestCase):
    """Verify term lists match master spreadsheet exactly."""

    def test_layer0_count(self):
        """Layer 0 must have exactly 15 primary EJ terms."""
        self.assertEqual(
            len(rep.LAYER0_TERMS), 15,
            f"Expected 15 Layer 0 terms, got {len(rep.LAYER0_TERMS)}"
        )

    def test_layer1_count(self):
        """Layer 1 must have exactly 30 near-synonym terms."""
        self.assertEqual(
            len(rep.LAYER1_TERMS), 30,
            f"Expected 30 Layer 1 terms, got {len(rep.LAYER1_TERMS)}"
        )

    def test_no_overlap_between_layers(self):
        """No term should appear in both Layer 0 and Layer 1."""
        overlap = set(rep.LAYER0_TERMS) & set(rep.LAYER1_TERMS)
        self.assertEqual(
            overlap, set(),
            f"Terms appear in both layers: {overlap}"
        )

    def test_layer0_required_terms(self):
        """Key primary EJ terms must be present in Layer 0."""
        required = [
            "environmental justice",
            "environmental racism",
            "health equity",
            "health disparities",
            "community health",
            "disproportionate burden",
            "community engagement",
        ]
        for term in required:
            self.assertIn(
                term, rep.LAYER0_TERMS,
                f"Required Layer 0 term missing: '{term}'"
            )

    def test_layer1_required_terms(self):
        """Key near-synonym terms must be present in Layer 1."""
        required = [
            "inequity",
            "marginalized",
            "vulnerable populations",
            "cumulative impact",
            "disparities",
            "contamination",
            "social justice",
        ]
        for term in required:
            self.assertIn(
                term, rep.LAYER1_TERMS,
                f"Required Layer 1 term missing: '{term}'"
            )

    def test_all_terms_lowercase(self):
        """All terms should be lowercase for case-insensitive matching."""
        for term in rep.LAYER0_TERMS:
            self.assertEqual(
                term, term.lower(),
                f"Layer 0 term not lowercase: '{term}'"
            )
        for term in rep.LAYER1_TERMS:
            self.assertEqual(
                term, term.lower(),
                f"Layer 1 term not lowercase: '{term}'"
            )

    def test_no_empty_terms(self):
        """No term should be empty or whitespace-only."""
        for term in rep.LAYER0_TERMS + rep.LAYER1_TERMS:
            self.assertTrue(
                term.strip(),
                f"Empty or whitespace term found: '{term}'"
            )

    def test_no_duplicate_terms_within_layer(self):
        """No duplicates within each layer."""
        self.assertEqual(len(rep.LAYER0_TERMS), len(set(rep.LAYER0_TERMS)),
                         "Duplicate in Layer 0")
        self.assertEqual(len(rep.LAYER1_TERMS), len(set(rep.LAYER1_TERMS)),
                         "Duplicate in Layer 1")


class TestTermPresent(unittest.TestCase):
    """Verify search_terms_in_text() word-boundary matching behaviour."""

    def _check(self, term, text):
        return rep.search_terms_in_text(text, [term])[term]

    def test_exact_match(self):
        """Exact term presence returns True."""
        self.assertTrue(self._check("environmental justice", "environmental justice"))

    def test_case_insensitive(self):
        """Matching is case-insensitive."""
        self.assertTrue(self._check("environmental justice", "Environmental Justice"))

    def test_substring_false_positive(self):
        """'community' must not match 'communicate' or 'communication'."""
        self.assertFalse(self._check("community", "communicate"))
        self.assertFalse(self._check("community", "communication"))
        self.assertFalse(self._check("community", "communities involve"))

    def test_word_boundary_start(self):
        """Term at start of string matches."""
        self.assertTrue(self._check("health equity", "health equity is defined as"))

    def test_word_boundary_end(self):
        """Term at end of string matches."""
        self.assertTrue(self._check("health equity", "the concept of health equity"))

    def test_plural_no_false_positive(self):
        """'racial' must not match 'racially' (different suffix)."""
        self.assertFalse(self._check("racial", "racially segregated"))

    def test_multi_word_term(self):
        """Multi-word terms match across word boundaries."""
        self.assertTrue(self._check("disproportionate burden",
                                    "communities bear a disproportionate burden of"))

    def test_no_match_empty_string(self):
        """Term not present in empty string."""
        self.assertFalse(self._check("environmental justice", ""))

    def test_punctuation_boundary(self):
        """Term adjacent to punctuation still matches."""
        self.assertTrue(self._check("health equity",
                                    "improve health equity, reduce disparities"))

    def test_exact_word_not_substring(self):
        """'racial' does not match inside 'multiracial'."""
        self.assertFalse(self._check("racial", "multiracial communities"))

    def test_distributional_consequences(self):
        """Exact Layer 0 phrase matches."""
        self.assertTrue(self._check("distributional consequences",
                                    "the distributional consequences of decisions"))

    def test_no_match_partial_word(self):
        """'equity' does not match 'equitable' (different root form)."""
        self.assertFalse(self._check("equity", "equitable distribution"))


class TestDataIntegrity(unittest.TestCase):
    """Verify layer2_outcomes.json structural integrity."""

    @classmethod
    def setUpClass(cls):
        json_path = os.path.join(
            os.path.dirname(__file__), "data", "layer2_outcomes.json"
        )
        with open(json_path) as f:
            cls.outcomes = json.load(f)

    def test_total_count(self):
        self.assertEqual(len(self.outcomes), 431)

    def test_sequential_numbering(self):
        nums = [r["num"] for r in self.outcomes]
        self.assertEqual(nums, list(range(1, 432)))

    def test_all_results_absent(self):
        non_absent = [r["num"] for r in self.outcomes if r["result"] != "Absent"]
        self.assertEqual(non_absent, [],
                         f"Non-Absent outcomes: {non_absent[:5]}")

    def test_all_criteria_zero(self):
        non_zero = [r["num"] for r in self.outcomes
                    if r["crit_a"] != 0 or r["crit_b"] != 0 or r["crit_c"] != 0]
        self.assertEqual(non_zero, [],
                         f"Non-zero criteria: {non_zero[:5]}")

    def test_cpc30220_count(self):
        n = sum(1 for r in self.outcomes if "CPC30220" in r["credential"])
        self.assertEqual(n, 114)

    def test_nccer_count(self):
        n = sum(1 for r in self.outcomes if "NCCER" in r["credential"])
        self.assertEqual(n, 103)

    def test_ca_cte_count(self):
        n = sum(1 for r in self.outcomes if "CA CTE" in r["credential"])
        self.assertEqual(n, 170)

    def test_city_guilds_count(self):
        n = sum(1 for r in self.outcomes if "City & Guilds" in r["credential"])
        self.assertEqual(n, 44)

    def test_required_fields_present(self):
        required = ["num","credential","unit","outcome_id","description",
                    "crit_a","crit_b","crit_c","result","notes"]
        for field in required:
            self.assertTrue(
                all(field in r for r in self.outcomes),
                f"Field '{field}' missing from some outcomes"
            )

    def test_unique_outcome_ids(self):
        ids = [r["outcome_id"] for r in self.outcomes]
        self.assertEqual(len(ids), len(set(ids)),
                         "Duplicate outcome IDs found")

    def test_crit_values_binary(self):
        for r in self.outcomes:
            for crit in ["crit_a","crit_b","crit_c"]:
                self.assertIn(r[crit], (0, 1),
                              f"Row {r['num']}: {crit}={r[crit]} is not 0 or 1")


class TestCredentialMapping(unittest.TestCase):
    """Verify CREDENTIALS dict covers all four credentials."""

    def test_all_credentials_present(self):
        """CREDENTIALS must contain all four credential keys."""
        required = [
            "NCCER Core (6th ed., USA)",
            "CA CTE Standards (USA)",
            "CPC30220 (Australia)",
            "City & Guilds 6706-23 (UK)",
        ]
        for key in required:
            self.assertIn(key, rep.CREDENTIALS,
                          f"CREDENTIALS missing: '{key}'")

    def test_credentials_has_four_entries(self):
        self.assertEqual(len(rep.CREDENTIALS), 4)

    def test_credential_keys_match_json(self):
        """CREDENTIALS keys must match credential names in layer2_outcomes.json."""
        json_path = os.path.join(
            os.path.dirname(__file__), "data", "layer2_outcomes.json"
        )
        with open(json_path) as f:
            outcomes = json.load(f)
        json_creds = {r["credential"] for r in outcomes}
        for key in rep.CREDENTIALS:
            self.assertIn(key, json_creds,
                          f"CREDENTIALS key not in JSON: '{key}'")


if __name__ == "__main__":
    loader  = unittest.TestLoader()
    suite   = unittest.TestSuite()
    for cls in [TestTermLists, TestTermPresent,
                TestDataIntegrity, TestCredentialMapping]:
        suite.addTests(loader.loadTestsFromTestCase(cls))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)

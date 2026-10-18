"""Tests for the branch/slug conventions."""

import unittest

from hephaestus import __version__, branch_name, slugify
from hephaestus.slug import MAX_BRANCH_LENGTH
from hephaestus.slug import slugify as slugify_direct


class SlugifyTest(unittest.TestCase):
    def test_plain_sentence(self):
        self.assertEqual(
            slugify("Add pow_int(a,b) to calc.py"),
            "add_pow_int_a_b_to_calc_py",
        )

    def test_separator_runs_collapse(self):
        self.assertEqual(slugify("fix:  a -- b"), "fix_a_b")

    def test_surrounding_separators_are_stripped(self):
        self.assertEqual(slugify("  Hello World!  "), "hello_world")

    def test_empty_and_separator_only_use_fallback(self):
        self.assertEqual(slugify(""), "task")
        self.assertEqual(slugify("!!!"), "task")
        self.assertEqual(slugify("..."), "task")

    def test_truncation_never_leaves_trailing_underscore(self):
        self.assertEqual(slugify("abc def", max_length=4), "abc")
        self.assertEqual(slugify("abcde fgh", max_length=6), "abcde")

    def test_non_ascii_acts_as_separator(self):
        self.assertEqual(slugify("Café déjà vu"), "caf_d_j_vu")

    def test_non_positive_max_length_returns_fallback(self):
        self.assertEqual(slugify("anything", max_length=0), "task")
        self.assertEqual(slugify("anything", max_length=-5), "task")

    def test_long_input_is_capped(self):
        self.assertEqual(len(slugify("x" * 500)), 60)


class BranchNameTest(unittest.TestCase):
    def test_expected_shape(self):
        self.assertEqual(
            branch_name("hephaestus", "t_ab12cd34", "Add rate limiter"),
            "hephaestus/t_ab12cd34-add_rate_limiter",
        )

    def test_project_name_is_slugified_too(self):
        self.assertEqual(
            branch_name("Factory Demo", "t_1", "x"),
            "factory_demo/t_1-x",
        )

    def test_same_inputs_produce_the_same_branch(self):
        args = ("hephaestus", "t_9", "Deterministic branches")
        self.assertEqual(branch_name(*args), branch_name(*args))

    def test_long_title_is_shortened_to_fit_the_cap(self):
        branch = branch_name("hephaestus", "t_abc12345", "word " * 60)
        self.assertLessEqual(len(branch), MAX_BRANCH_LENGTH)
        self.assertFalse(branch.endswith("_"))
        self.assertTrue(branch.startswith("hephaestus/t_abc12345-"))

    def test_task_id_is_preserved_exactly(self):
        branch = branch_name("hephaestus", "t_AB12cd34", "title")
        self.assertIn("t_AB12cd34", branch)

    def test_rejects_unusable_task_ids(self):
        for bad in ("", "   ", "t/1", "t 1", "t..1", "t*1"):
            with self.subTest(task_id=bad):
                with self.assertRaises(ValueError):
                    branch_name("hephaestus", bad, "title")

    def test_rejects_impossible_budget(self):
        # A 60-char project slug plus an oversized task id leaves no room for any
        # title, and silently shipping a nameless branch would be worse than failing.
        with self.assertRaises(ValueError):
            branch_name("hephaestus", "t_" + "x" * 200, "title")


class PackageTest(unittest.TestCase):
    def test_version_is_exposed_and_well_formed(self):
        parts = __version__.split(".")
        self.assertEqual(len(parts), 3)
        self.assertTrue(all(part.isdigit() for part in parts))

    def test_public_reexports_match_the_module(self):
        self.assertIs(slugify, slugify_direct)


if __name__ == "__main__":
    unittest.main()

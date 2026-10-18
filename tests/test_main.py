"""Tests for the ``python3 -m hephaestus`` command-line entry point."""

import io
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from hephaestus.__main__ import main

REPO_ROOT = Path(__file__).resolve().parents[1]


def run_main(argv):
    """Return ``(exit_code, stdout, stderr)`` for ``main(argv)``."""
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


class BranchCommandTest(unittest.TestCase):
    def test_success_prints_only_the_branch_name(self):
        code, out, err = run_main(["branch", "hephaestus", "t_ab12cd34", "Add rate limiter"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "hephaestus/t_ab12cd34-add_rate_limiter\n")
        self.assertEqual(err, "")

    def test_invalid_task_id_reports_to_stderr_without_a_traceback(self):
        code, out, err = run_main(["branch", "hephaestus", "t/1", "Add rate limiter"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("t/1", err)
        self.assertNotIn("Traceback", err)

    def test_impossible_budget_is_reported_like_any_other_bad_input(self):
        code, out, err = run_main(["branch", "hephaestus", "t_" + "x" * 200, "title"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertNotIn("Traceback", err)


class UsageTest(unittest.TestCase):
    def test_no_arguments_fails_and_shows_usage(self):
        code, out, err = run_main([])
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")
        self.assertIn("usage:", err)

    def test_unknown_command_is_rejected(self):
        with self.assertRaises(SystemExit) as caught:
            with redirect_stderr(io.StringIO()):
                main(["nope"])
        self.assertNotEqual(caught.exception.code, 0)


class ModuleInvocationTest(unittest.TestCase):
    def test_python_dash_m_matches_main(self):
        result = subprocess.run(
            [sys.executable, "-m", "hephaestus", "branch", "hephaestus", "t_ab12cd34",
             "Add rate limiter"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "hephaestus/t_ab12cd34-add_rate_limiter\n")
        self.assertEqual(result.stderr, "")

    def test_python_dash_m_exits_2_on_a_bad_task_id(self):
        result = subprocess.run(
            [sys.executable, "-m", "hephaestus", "branch", "hephaestus", "t/1", "Title"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()

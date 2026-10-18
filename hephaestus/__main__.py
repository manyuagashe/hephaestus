"""Command-line entry point: ``python3 -m hephaestus <command> ...``.

The CLI exists so that the branch convention can be computed from a shell
without writing Python, and so later factory commands have a place to land.
"""

from __future__ import annotations

import argparse
import sys

from .slug import branch_name

PROG = "hephaestus"

EXIT_OK = 0
EXIT_USAGE = 2


def _add_branch_parser(subparsers: argparse._SubParsersAction) -> None:
    """Register the ``branch`` subcommand on ``subparsers``."""
    parser = subparsers.add_parser(
        "branch",
        help="print the branch name for a card",
        description="Print the deterministic branch name for a card.",
    )
    parser.add_argument("project", help="project the card belongs to")
    parser.add_argument("task_id", metavar="task-id", help="kanban task id")
    parser.add_argument("title", help="card title, used for the title slug")


def _build_parser() -> argparse.ArgumentParser:
    """Build the argument parser holding every command the CLI supports."""
    parser = argparse.ArgumentParser(
        prog=PROG,
        description="Compute the conventions used by the Hermes software factory.",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="command")
    _add_branch_parser(subparsers)
    return parser


def _run_branch(args: argparse.Namespace) -> int:
    """Print the branch name for a card, or explain why it cannot be built."""
    try:
        name = branch_name(args.project, args.task_id, args.title)
    except ValueError as exc:
        print(f"{PROG}: error: {exc}", file=sys.stderr)
        return EXIT_USAGE
    print(name)
    return EXIT_OK


_COMMANDS = {"branch": _run_branch}


def main(argv: list[str] | None = None) -> int:
    """Run the CLI with ``argv`` (default ``sys.argv[1:]``) and return the exit code."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    handler = _COMMANDS.get(args.command)
    if handler is None:
        parser.print_usage(sys.stderr)
        print(f"{PROG}: error: a command is required", file=sys.stderr)
        return EXIT_USAGE
    return handler(args)


if __name__ == "__main__":
    sys.exit(main())

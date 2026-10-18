"""Slug and branch-name helpers.

Kanban cards create a git worktree per task and the branch name must be
deterministic: the same card must always produce the same branch, and the name
must be safe for git, the filesystem, and a CI URL.
"""

from __future__ import annotations

import re

MAX_SLUG_LENGTH = 60
MAX_BRANCH_LENGTH = 120
FALLBACK_SLUG = "task"

_NON_SLUG = re.compile(r"[^a-z0-9]+")
_INVALID_TASK_ID = re.compile(r"[\s/\\~^:?*\[]|\.\.")


def slugify(text: str, max_length: int = MAX_SLUG_LENGTH) -> str:
    """Return ``text`` lowercased and reduced to ``[a-z0-9_]``.

    Runs of anything else collapse to a single underscore, which is then
    stripped from both ends. Non-ASCII characters are separators, not
    transliterated. An empty result falls back to ``"task"``.

    A truncation never leaves a trailing underscore, because git and CI both
    tend to render a trailing separator confusingly.
    """
    if max_length <= 0:
        return FALLBACK_SLUG

    slug = _NON_SLUG.sub("_", text.lower()).strip("_")
    slug = slug[:max_length].strip("_")
    return slug or FALLBACK_SLUG


def branch_name(project: str, task_id: str, title: str) -> str:
    """Compose the deterministic branch name for a card's worktree.

    Format: ``<project-slug>/<task-id>-<title-slug>``, capped at
    ``MAX_BRANCH_LENGTH`` characters by shortening the title portion only —
    the project and task id must survive intact, since they are what makes the
    branch traceable back to the card.
    """
    if not task_id or not task_id.strip():
        raise ValueError("task_id must be a non-empty string")
    if _INVALID_TASK_ID.search(task_id):
        raise ValueError(f"task_id is not safe for a git ref: {task_id!r}")

    prefix = f"{slugify(project)}/{task_id}-"
    budget = MAX_BRANCH_LENGTH - len(prefix)
    if budget < 1:
        raise ValueError("project and task_id leave no room for a title slug")
    return prefix + slugify(title, max_length=budget)

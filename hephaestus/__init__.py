"""hephaestus — conventions used by the Hermes software-factory pipeline.

The package is intentionally tiny: it exists so that kanban cards have real,
testable logic to modify, and so that the branch/slug conventions the factory
relies on are written down in executable form rather than in prose.
"""

from .slug import branch_name, slugify

__version__ = "0.1.0"

__all__ = ["branch_name", "slugify", "__version__"]

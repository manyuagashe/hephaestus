# hephaestus

Repository for the Hermes software-factory pipeline.

Status: **scaffold**. This repo currently holds the conventions, the CI gate, and one
small real module (`hephaestus.slug`) so that kanban cards have something concrete to
modify. Product direction is deliberately undecided — replace this paragraph once it is.

## Layout

```
.hephaestus/          # nothing yet — factory config lives outside this repo
hephaestus/           # importable package (flat layout, no install step required)
  slug.py             # branch/slug conventions used by the factory
tests/                # unittest suite, stdlib only
.github/workflows/    # CI: the gate a card must pass to be considered done
AGENTS.md             # the contract every factory worker reads first
```

## Commands

Run from the repository root:

```bash
# tests (canonical; this is the definition of done)
python3 -m unittest discover -s tests -t . -v

# lint
ruff check .
```

Tests are dependency-free: Python 3.11+ standard library only. `ruff` is only needed
when you touch lint-sensitive code; CI installs it automatically.

## CI

`.github/workflows/ci.yml` runs the test command above on Python 3.11 and 3.12, plus
`ruff check .`. A kanban card opened with a `--completion-contract` naming this repo
cannot reach `done` until its PR exists and these checks are green.

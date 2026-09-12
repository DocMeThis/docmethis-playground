# Regression Versus Catchup

Published starting point: `tutorials-v0.1.0`. Work directly on the current local
branch. This tutorial creates the old debt and the new change in sequence, so
neither result is hidden in a prepared state.

## Prepare

```bash
git reset --hard tutorials-v0.1.0
git clean -fd
```

## Create Existing Debt

Install Check, then add `demo_shop/legacy.py`:

```python
"""Legacy pricing helpers kept for migration examples."""


def legacy_total(price_cents: int, quantity: int) -> int:
    return price_cents * quantity
```

Commit this first state. The function is intentionally undocumented:

```bash
git add demo_shop/legacy.py
git commit -m "Add legacy pricing helper"
```

## Add A New Change

Edit `demo_shop/legacy.py` so the existing helper is touched and a new function
has an incomplete docstring:

```python
def legacy_total(price_cents: int, quantity: int) -> int:
    # This pre-existing helper remains intentionally undocumented.
    return price_cents * quantity


def preview_total(price_cents: int, quantity: int) -> int:
    """Preview a total.

    Parameters
    ----------
    price_cents : int
        Unit price in cents.
    quantity : int
        Number of units.
    """
    return price_cents * quantity
```

Commit both edits:

```bash
git add demo_shop/legacy.py
git commit -m "Add checkout preview"
```

## Compare The Modes

Run the same range in both modes:

```bash
python -m docmethis_check . \
  --git-diff HEAD~1..HEAD \
  --check-mode regression \
  --no-cache \
  --no-dia

python -m docmethis_check . \
  --git-diff HEAD~1..HEAD \
  --check-mode catchup \
  --no-cache \
  --no-dia
```

`regression` reports only the new `DMT-3001` on `preview_total` and filters the
pre-existing debt. `catchup` also reports `legacy_total`'s existing `DMT-1120`,
the parameter findings and `DMT-3001`. Neither mode is a repository-wide scan
by itself; the empty-tree command in the root README is the explicit full-project
variant. The two temporary commits can be abandoned with the reset command
before starting the next tutorial.

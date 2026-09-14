# Understand Git Diff And Base Edge Cases

Published starting point: `tutorials-v0.1.0`. Work directly on the current local
branch. This tutorial uses small disposable commits to show how Check chooses a
range and what to do when Git cannot provide a reliable base.

## Compare Range Forms

```bash
git reset --hard tutorials-v0.1.0
git clean -fd
```

Install Check. Make a harmless comment change in `demo_shop/pricing.py` without
committing it. The default invocation compares this working tree with `HEAD`:

```bash
python -m docmethis_check . --no-cache --no-dia
```

Commit the same change, then compare the two revisions directly with an explicit
two-dot range:

```bash
git add demo_shop/pricing.py
git commit -m "Touch pricing for diff examples"
python -m docmethis_check . \
  --git-diff HEAD~1..HEAD \
  --no-cache \
  --no-dia
```

Use a three-dot range when the comparison should start at the merge base:

```bash
python -m docmethis_check . \
  --git-diff origin/main...HEAD \
  --no-cache \
  --no-dia
```

## Missing And Non-Linear Bases

If a base revision is unavailable, choose whether the run should emit all
available findings or fail explicitly:

```bash
python -m docmethis_check . \
  --git-diff does-not-exist..HEAD \
  --on-missing-base emit_all \
  --no-cache \
  --no-dia
```

For a force-push, rebase or squash, provide a reliable base when it is available:

```bash
python -m docmethis_check . \
  --base-ref origin/main \
  --on-nonlinear-push-without-base fail \
  --no-cache \
  --no-dia
```

If no reliable base exists, `warn` makes the limitation explicit without
pretending that the project was fully analyzed. `head_commit` limits the run to
the submitted head; `fail` is the strict choice for CI.

The practical rule is to keep full Git history in CI and use an explicit base or
range when a push is non-linear. Reset the playground before the next tutorial;
the temporary commit is not part of the baseline.

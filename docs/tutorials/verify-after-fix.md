# Verify The Result After Fix

Published starting point: `tutorials-v0.1.0`. Work directly on the current local
branch. The final check is the acceptance step: a generated patch is not a
successful Fix result until Check accepts the resulting source and docstrings.

## Create And Fix The Finding

```bash
git reset --hard tutorials-v0.1.0
git clean -fd
git cherry-pick origin/setup/fix-config
git cherry-pick origin/setup/provider-anthropic
```

Set the provider credentials. In `demo_shop/pricing.py`, remove the `Returns`
section from `calculate_total`, then produce the report:

```bash
python -m docmethis_check . \
  --no-cache \
  --no-dia \
  --json-output-file check.json
python -m docmethis_fix check.json --no-commit
```

Inspect the patch and run the application tests:

```bash
git diff -- demo_shop/pricing.py
python -m unittest discover -s tests -v
```

## Run Check Again

Check the post-Fix working-tree diff with a fresh report:

```bash
python -m docmethis_check . \
  --no-cache \
  --no-dia \
  --json-output-file verify.json
```

The original `DMT-3001` should no longer be emitted for
`demo_shop.pricing.calculate_total`, and the application tests should remain
green. If a finding persists, treat the Fix run as incomplete: inspect the JSON
target details and leave the patch uncommitted for manual review.

This second Check is independent of Fix's own in-memory validation. It verifies
the actual files after the generated patch has crossed the repository boundary.

# A Diagnostic Fix Does Not Handle

Published starting point: `tutorials-v0.1.0`. Work directly on the current local
branch. The unsupported diagnostic is produced by the tutorial's own
documentation edit, not by a pre-built pricing file.

## Create The Diagnostic

```bash
git reset --hard tutorials-v0.1.0
git clean -fd
git cherry-pick origin/setup/fix-config
git cherry-pick origin/setup/provider-anthropic
```

In `demo_shop/pricing.py`, rename the `Returns` section heading of
`calculate_total` to the misspelled `Retuns` heading. Run Check:

```bash
python -m docmethis_check . \
  --no-cache \
  --no-dia \
  --json-output-file check.json
```

With a valid Fix setup, run:

```bash
python -m docmethis_fix check.json --preview
```

## Expected Behavior

Check emits `DMT-6049` for the malformed section. Fix keeps the diagnostic
visible with a non-fixable/skipped status rather than silently rewriting the
docstring or claiming success.

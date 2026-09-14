# Fix Preview

Published starting point: `tutorials-v0.1.0`. Work directly on the current local
branch. The Fix configuration and provider profile are reusable boilerplate;
the missing documentation is created during this tutorial.

## Prepare Fix

Choose one provider setup. This example uses Anthropic:

```bash
git reset --hard tutorials-v0.1.0
git clean -fd
git cherry-pick origin/setup/fix-config
git cherry-pick origin/setup/provider-anthropic
```

Read the files added under `.github/docmethis-fix/` and replace the placeholder
model with one supported by the private Fix runtime. Keep credentials outside Git
as described in the root README.

## Create The Finding

In `demo_shop/pricing.py`, remove the complete `Returns` section from
`calculate_total` without changing its body. Generate the Check hand-off:

```bash
python -m docmethis_check . \
  --no-cache \
  --no-dia \
  --json-output-file check.json
```

With an activated Fix account, Gateway access and the selected provider:

```bash
python -m docmethis_fix check.json --preview
```

## Expected Behavior

Check reports `DMT-3001` with structured `Returns` target data. Fix generates a
preview for the first eligible target, performs no file write and creates no
commit. The generated prose is provider-dependent; the stable expectation is
the target, the preview status and an unchanged working tree.

Fix preview still requires Gateway and an LLM. It is not an offline demo.

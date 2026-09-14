# Decide What Fix Is Allowed To Change

Published starting point: `tutorials-v0.1.0`. Work directly on the current local
branch. The provider setup is a prerequisite here; the policy that limits Fix is
the subject of the tutorial.

## Prepare Fix

```bash
git reset --hard tutorials-v0.1.0
git clean -fd
git cherry-pick origin/setup/fix-config
git cherry-pick origin/setup/provider-anthropic
```

Set the provider credentials described in the root README. Inspect the Fix
settings added by `setup/fix-config`:

```toml
[tool.docmethis.fix]
include-existing-docstrings = true
scope = "impacted"
allowed-dia-statuses = ["confirmed"]
enable-summary-quality-fixes = false
missing-docstring-generation-mode = "sectional"
```

These choices define which existing docstrings, DIA impacts and generation
strategies are eligible. They do not change what Check reports.

## Create Competing Targets

In `demo_shop/pricing.py`:

1. Remove the `Returns` section from `calculate_total`.
2. Change `_read_discount` so an unknown non-empty code raises `KeyError`.

Generate a report that includes DIA:

```bash
python -m docmethis_check . \
  --no-cache \
  --json-output-file check.json
```

With `include-existing-docstrings` enabled and `scope = "impacted"`, Fix may
consider the existing documentation target and a confirmed propagated impact.
Now make the policy deliberately restrictive:

```toml
[tool.docmethis.fix]
include-existing-docstrings = false
scope = "diff"
allowed-dia-statuses = ["confirmed"]
enable-summary-quality-fixes = false
```

Preview again:

```bash
python -m docmethis_fix check.json --preview
```

The report is unchanged, but Fix's eligible target set is narrower. The same
choices can be tested without editing TOML by using `--no-include-existing-docstrings`,
`--scope diff` and repeated `--allow-dia-status confirmed` options. A restrictive
policy is useful when the cost of an unintended documentation change is higher
than leaving a finding for manual review.

# Full Catchup And Documentation Debt Cleanup

Published starting point: `tutorials-v0.1.0`. Work directly on the current local
branch. The debt is introduced during the tutorial, then selected deliberately
with an empty-tree range.

## Create Temporary Debt

```bash
git reset --hard tutorials-v0.1.0
git clean -fd
```

Install Check. In the current codebase, temporarily:

- remove the docstring from `Catalog.find` in `demo_shop/catalog.py`;
- remove the `Returns` section from `calculate_total` in `demo_shop/pricing.py`;
- remove the docstring from `write_receipt` in `demo_shop/receipts.py`.

Commit this deliberately broken state so the synthetic range can select it:

```bash
git add demo_shop/catalog.py demo_shop/pricing.py demo_shop/receipts.py
git commit -m "Create documentation debt for catchup"
```

## Audit The Whole Repository

```bash
EMPTY_TREE="$(git hash-object -t tree /dev/null)"
python -m docmethis_check . \
  --git-diff "${EMPTY_TREE}..HEAD" \
  --check-mode catchup \
  --include-visibility public,protected,private \
  --symbol-kinds function,method,class,module \
  --no-dia \
  --no-cache \
  --json-output-file catchup.json
```

Unlike an ordinary catchup run, the empty-tree base deliberately selects every
current Python file. The report is a repository-wide debt inventory, not just a
regression report for the last edit.

## Clean The Debt With Fix

If the goal is to repair the debt rather than only inspect it, add the reusable
Fix setup and one provider profile:

```bash
git cherry-pick origin/setup/fix-config
git cherry-pick origin/setup/provider-anthropic
```

Set the provider credentials, then preview or apply the first eligible target:

```bash
python -m docmethis_fix catchup.json --preview
python -m docmethis_fix catchup.json --no-commit
```

Inspect the generated diff, run the application tests, and decide whether to
commit the cleanup. The debt commit and any temporary Fix patch are abandoned
when the playground is reset:

```bash
git reset --hard tutorials-v0.1.0
git clean -fd
```

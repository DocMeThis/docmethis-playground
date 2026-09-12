# Check a Local Diff

Published starting point: `tutorials-v0.1.0`. Work directly on the current local
branch. This tutorial uses no setup branch because the interesting part is the
local code change and the diff-scoped DocMeThis Check command.

## Prepare

Install the docmethis-playground repository and the released DocMeThis Check CLI as 
described in the root README. The playground itself remains free of a DocMeThis 
dependency.

If you already played with the repository:

```bash
git reset --hard tutorials-v0.1.0
git clean -fd
```

## Create A Finding

In `demo_shop/pricing.py`, remove the complete `Returns` section from
`calculate_total` without changing the function body. Run DocMeThis Check on the working
tree:

```bash
python -m docmethis_check .
```

The command exits `1` and emits `DMT-3001` for
`demo_shop.pricing.calculate_total`.

Restore the file before trying another independent variant:

```bash
git restore demo_shop/pricing.py
```

From the same clean branch, try one of these changes:

- Remove `discount_code` from the signature but leave it in the docstring: `DMT-2002`.
- Reorder two documented parameters without changing their names: `DMT-2003`.
- Add a public parameter without documenting it: `DMT-2001`.


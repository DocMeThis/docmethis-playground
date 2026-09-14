# Control Check Scope

Published starting point: `tutorials-v0.1.0`. Work directly on the current local
branch. This tutorial makes visibility, symbol-kind and severity filters visible
instead of treating the default policy as a fixed result.

## Prepare

```bash
git reset --hard tutorials-v0.1.0
git clean -fd
```

Install the released Check CLI as described in the root README.

## Create Different Targets

In `demo_shop/pricing.py`:

1. Remove the complete `Returns` section from `calculate_total`.
2. Remove the docstring from the private helper `_read_discount` without changing its body.

The first edit affects a public function. The second creates a private
documentation defect. Run the default public scope first:

```bash
python -m docmethis_check . --no-cache --no-dia
```

The private helper is outside the default public visibility. Select it
explicitly, together with function symbols, to inspect it:

```bash
python -m docmethis_check . \
  --include-visibility private \
  --symbol-kinds function \
  --profile strict \
  --no-cache \
  --no-dia
```

Visibility and symbol kinds are independent filters. For example, this command
checks public and private classes and methods but not functions:

```bash
python -m docmethis_check . \
  --include-visibility public,private \
  --symbol-kinds class,method \
  --profile strict \
  --no-cache \
  --no-dia
```

## Control Severity

`loose`, `standard` and `strict` are complete built-in severity profiles. Compare
the same diff with two policies:

```bash
python -m docmethis_check . --profile loose --no-cache --no-dia
python -m docmethis_check . --profile strict --fail-on-warning --no-cache --no-dia
```

The profile controls effective severity; `--fail-on-warning` controls whether a
warning makes the command fail. They are separate decisions. An explicit code
override can be added to a temporary `pyproject.toml` during the tutorial:

```toml
[tool.docmethis.check]
profile = "standard"

[tool.docmethis.check.severity]
DMT-3001 = "warning"
```

Restore the playground with the reset command before continuing to the next
tutorial.

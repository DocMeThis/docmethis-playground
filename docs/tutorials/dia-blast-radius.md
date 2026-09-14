# DIA Blast Radius

Published starting point: `tutorials-v0.1.0`. Work directly on the current local
branch. The private helper and its public callers are already part of the normal
application; the tutorial introduces the behavior change that reveals the
affected path.

## Create The Change

```bash
git reset --hard tutorials-v0.1.0
git clean -fd
```

Install Check, then change `_read_discount` in `demo_shop/pricing.py` so an
unknown non-empty code raises `KeyError` before returning the discount:

```python
if code and code != "WELCOME10":
    raise KeyError(code)
```

Run Check on the working-tree diff:

```bash
python -m docmethis_check . \
  --no-cache \
  --json-output-file dia.json
```

## Expected Behavior

The report's `impact_analysis` contains a new exception impact and evidence
through the call path. The public order functions are affected even though the
changed symbol is private. The exact DMT code and status should be read from
the pinned Check release; the educational point is the propagated contract and
its evidence, not a hard-coded message.

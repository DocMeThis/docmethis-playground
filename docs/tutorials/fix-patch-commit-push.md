# Preview, Patch, Commit And Push

Published starting point: `tutorials-v0.1.0`. Work directly on the current local
branch. This tutorial follows one Fix target through preview, an uncommitted
patch, a real commit and optional publication.

## Prepare A Fixable Target

```bash
git reset --hard tutorials-v0.1.0
git clean -fd
git cherry-pick origin/setup/fix-config
git cherry-pick origin/setup/provider-anthropic
```

Set the provider credentials, then remove the `Returns` section from
`calculate_total` in `demo_shop/pricing.py`.

Create the hand-off report:

```bash
python -m docmethis_check . \
  --no-cache \
  --no-dia \
  --json-output-file check.json
```

## Walk The Git Actions

Preview without changing the repository:

```bash
python -m docmethis_fix check.json --preview
```

Apply the patch without creating a commit and inspect it:

```bash
python -m docmethis_fix check.json --no-commit
git diff -- demo_shop/pricing.py
python -m unittest discover -s tests -v
```

After inspection, restore the target and recreate the deliberate defect so the
same report can be consumed once more:

```bash
git restore demo_shop/pricing.py
# Remove the Returns section from calculate_total again.
```

`--preview` performs no write and `--no-commit` applies a patch without a
commit. The normal invocation commits the accepted patch. Fix does not push
unless `--push` is explicit.

## Publish Safely

Only demonstrate `--push` against a disposable fork or remote. Point `origin`
to that fork before running the command; do not push a tutorial commit to the
upstream playground repository:

```bash
git remote set-url origin git@github.com:YOUR_ACCOUNT/docmethis-playground.git
git push --set-upstream origin HEAD:fix-demo
python -m docmethis_fix check.json \
  --push \
  --commit-message "docs: restore pricing return contract"
git show --stat --oneline HEAD
```

The temporary remote branch makes the current local branch track a disposable
fork branch instead of the playground's `main`. The Fix push requires the
commit to succeed. Omit `--push` when the commit should remain local. Reset the
playground after the demonstration.

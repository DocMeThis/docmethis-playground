# Check In A GitHub Pull Request

Published starting point: `tutorials-v0.1.0`. Work directly on the current local
branch. The workflow is boilerplate, so add it by cherry-picking the stable
setup branch. The code change and the pull request remain part of this tutorial.

## Add The Workflow

Start by cleaning up the repository if you already played with it:

```bash
git reset --hard tutorials-v0.1.0
git clean -fd
```

Then retrieve the boilerplate workflow:

```bash
git cherry-pick origin/setup/github-check
```

Open `.github/workflows/docmethis-check.yml`. The important choices are full
history for diff resolution, read-only contents permissions, disabled checkout
credentials, a pinned action release, precise annotations and
`GITHUB_BEFORE_SHA` for push ranges.

## Create A Pull Request Finding

In `demo_shop/catalog.py`, change `Catalog.find` so its signature becomes:

```python
def find(self, sku: str, *, normalize: bool = True) -> Product:
```

Use `normalize` to choose between `_normalize_sku(sku)` and the raw `sku`, but
do not update the docstring's `Parameters` section. Run the local test suite,
commit the change, and push the branch to a fork. Open a pull request against
the fork's `main` branch.

## Expected Behavior

The Check job should annotate the changed method with `DMT-2001` for the new
parameter. The workflow keeps full Git history, uses precise annotations and
passes `GITHUB_BEFORE_SHA` for push range resolution.

The workflow is a reusable setup commit. Update its pinned action reference only
in a deliberate new setup commit, never by changing a tutorial outcome.

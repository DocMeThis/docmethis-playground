# Build a mixed CI workflow: auto-Fix feature branches, block PRs with Check

Published starting point: `tutorials-v0.1.0`. Work directly on the current local
branch. This tutorial builds one workflow with two trust boundaries:

- Fix may write to a feature branch after a push;
- Check runs read-only on pull requests and remains the merge gate.

The public `docmethis-fix` repository does not ship the private Fix runtime. The
event split and security shape below are complete, but its authenticated
runtime-install step must come from the private release contract for the account
and version being used.

## Prepare The Fix Configuration

Start from a clean tutorial base and choose one provider. This example uses
Anthropic:

```bash
git reset --hard tutorials-v0.1.0
git clean -fd
git cherry-pick origin/setup/fix-config
git cherry-pick origin/setup/provider-anthropic
```

Inspect `.github/docmethis-fix/`. Replace the placeholder model with one supported
by the selected private runtime. Keep the following values in GitHub secret or
variable storage, never in the repository:

- `DOCMETHIS_FIX_DISTRIBUTION_TOKEN` secret for the private runtime distribution;
- `DOCMETHIS_FIX_API_KEY` secret for Gateway;
- `ANTHROPIC_API_KEY` secret for the selected provider;
- `DOCMETHIS_FIX_RUNTIME_SHA` variable containing the full runtime commit SHA;
- `DOCMETHIS_FIX_ARTIFACT_SHA256` variable containing the matching artifact digest.

Do not cherry-pick `origin/setup/github-check`: the Check job is built into the
mixed workflow below.

## Build The Mixed Workflow

Create `.github/workflows/docmethis-mixed.yml`:

```yaml
name: DocMeThis mixed CI

on:
  push:
    branches-ignore: [main, master]
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: read

concurrency:
  group: docmethis-mixed-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  fix-feature:
    name: Auto-Fix feature branch
    if: github.event_name == 'push' && github.actor != 'github-actions[bot]'
    runs-on: ubuntu-latest
    timeout-minutes: 20
    permissions:
      contents: write
      pull-requests: write
    env:
      FIX_PYTHON: ${{ runner.temp }}/docmethis-fix-venv/bin/python
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    steps:
      - name: Check out the feature branch
        uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
        with:
          fetch-depth: 0
          persist-credentials: false
          ref: ${{ github.ref_name }}

      - name: Pin the private Fix runtime
        env:
          DOCMETHIS_FIX_DISTRIBUTION_TOKEN: ${{ secrets.DOCMETHIS_FIX_DISTRIBUTION_TOKEN }}
          DOCMETHIS_FIX_RUNTIME_SHA: ${{ vars.DOCMETHIS_FIX_RUNTIME_SHA }}
          DOCMETHIS_FIX_ARTIFACT_SHA256: ${{ vars.DOCMETHIS_FIX_ARTIFACT_SHA256 }}
        run: |
          set -euo pipefail
          test -n "$DOCMETHIS_FIX_DISTRIBUTION_TOKEN"
          [[ "$DOCMETHIS_FIX_RUNTIME_SHA" =~ ^[0-9a-f]{40}$ ]]
          [[ "$DOCMETHIS_FIX_ARTIFACT_SHA256" =~ ^[0-9a-f]{64}$ ]]
          printf '%s\n' 'Private runtime installation is release-channel specific.'
          printf 'Runtime commit SHA: %s\n' "$DOCMETHIS_FIX_RUNTIME_SHA"
          printf 'Artifact SHA-256: %s\n' "$DOCMETHIS_FIX_ARTIFACT_SHA256"
          printf '%s\n' 'Replace this step with the authenticated installer before enabling Fix.'
          exit 1

      - name: Prepare the Gateway key
        env:
          FIX_API_KEY: ${{ secrets.DOCMETHIS_FIX_API_KEY }}
        run: |
          set -euo pipefail
          key_file="$RUNNER_TEMP/docmethis-fix-api-key"
          umask 077
          printf '%s' "$FIX_API_KEY" > "$key_file"
          echo "DOCMETHIS_FIX_API_KEY_FILE=$key_file" >> "$GITHUB_ENV"

      - name: Generate the Check hand-off
        env:
          GITHUB_BEFORE_SHA: ${{ github.event.before }}
        run: |
          set +e
          "$FIX_PYTHON" -m docmethis_check . \
            --check-mode catchup \
            --json-output-file rapport.json \
            --on-nonlinear-push-without-base fail
          status=$?
          set -e
          test -s rapport.json
          if [ "$status" -gt 1 ]; then
            exit "$status"
          fi

      - name: Apply eligible Fix corrections
        env:
          GITHUB_TOKEN: ${{ github.token }}
        run: |
          set -euo pipefail
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          "$FIX_PYTHON" -m docmethis_fix rapport.json --project-root . --pr > fix-result.json
          cat fix-result.json

  check-pr:
    name: Check pull request
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    timeout-minutes: 15
    permissions:
      contents: read
    steps:
      - name: Check out the pull request and its history
        uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
        with:
          fetch-depth: 0
          persist-credentials: false

      - name: Check documentation consistency
        uses: DocMeThis/docmethis-check@80f6ea6bdb68bd246b075b265a4ef60e77b6e5b0 # pinned public Check release
        env:
          GITHUB_BEFORE_SHA: ${{ github.event.before }}
        with:
          project-path: .
          check-mode: regression
          fail-on-warning: true
          annotation-placement: precise
          on-nonlinear-push-without-base: warn
```

The Fix job deliberately accepts Check exit code `1`: that code means the report
contains findings that Fix may correct. It still fails on an operational error.
The `github-actions[bot]` guard prevents a Fix commit from recursively starting
another Fix run.

## Make Check The Merge Gate

Push the workflow to a disposable fork, then configure branch protection for the
repository's default branch. Require the `Check pull request` status check before
merging. Do not make the Fix job required: it runs on feature-branch pushes, not on
the pull request event.

The security boundary is intentional:

- Fix never runs on `pull_request`, so fork code cannot receive Fix secrets;
- Check uses read-only permissions and no private credentials;
- the workflow does not use `pull_request_target`;
- the Check action and private Fix runtime are immutable references;
- a Fix-generated commit causes Check to run again on the pull request.

## Exercise The Workflow

Create a disposable feature branch and remove the complete `Returns` section from
`calculate_total` in `demo_shop/pricing.py`:

```bash
git checkout -b docs/mixed-ci-demo
python -m unittest discover -s tests -v
git add demo_shop/pricing.py .github/workflows/docmethis-mixed.yml
git commit -m "docs: create a mixed CI finding"
git push --set-upstream origin docs/mixed-ci-demo
```

The push starts Fix. Fix consumes the Check report and, when the finding is eligible,
commits the documentation correction and opens or updates the pull request. Check
then runs on the pull request and is the final acceptance decision. If the finding
remains, the required Check status blocks the merge.

The generated prose and Fix result are provider- and release-dependent. The stable
expectations are the event split, the permission boundary, the Check annotation and
the required pull-request status.

Reset the disposable playground after the demonstration:

```bash
git reset --hard tutorials-v0.1.0
git clean -fd
```

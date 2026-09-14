<p align="center">
  <a href="https://docmethis.com">
    <picture>
      <img src="branding/logo_docmethis_playground.png" alt="DocMeThis Playground logo" width="600">
    </picture>
  </a>
</p>

<p align="center">
  <em>DocMeThis Playground is a learning platform for the <a href="https://github.com/orgs/DocMeThis/repositories">DocMeThis suite</a>.</em>
</p>

# DocMeThis Playground

This repository is a small, reproducible codebase for DocMeThis demos and
tutorials. It is a teaching fixture, not a production starter kit.

The `main` branch is deliberately neutral: it is a small Python repository with
no DocMeThis installation, workflow or configuration. Every tutorial starts
there and builds the adoption story step by step.

## Prerequisites

- Git
- Python 3.12 or newer
- An activated DocMeThis Fix account for Fix tutorials

Install the public Check package in a virtual environment when a tutorial needs
the local CLI:

```bash
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install --extra-index-url https://pkg.docmethis.com docmethis-check
```

or with `uv`:

```bash
uv venv
. .venv/bin/activate
uv pip install --extra-index-url https://pkg.docmethis.com docmethis-check
```

## Start A Tutorial

```bash
git clone https://github.com/DocMeThis/docmethis-playground.git
cd docmethis-playground
```

The `setup/*` branches are available as remote-tracking branches
after a normal clone; cherry-pick only the setup needed by the tutorial.

The provider branches are alternatives; choose one rather than cherry-picking
several versions of `.github/docmethis-fix/llm_api.toml`.

## Reset Between Tutorials

The playground is disposable. Work directly on the current local branch, then
reset it before starting the next tutorial:

These commands delete uncommitted changes and untracked non-ignored files. Use
them only in the disposable playground clone.

```bash
git reset --hard origin/main
git clean -fd
```

Do not use `git reset --hard main`: a cherry-pick advances the local `main`
branch, while `origin/main` remains the baseline reference.

## Setup Branches

| Branch | Adds |
| --- | --- |
| `setup/github-check` | GitHub Actions workflow for Check |
| `setup/fix-config` | Fix project settings and non-secret policy defaults |
| `setup/provider-openai` | OpenAI-compatible API profile |
| `setup/provider-anthropic` | Anthropic API profile |
| `setup/provider-gemini` | Gemini API profile |

Each branch contains one clean setup commit on the published tutorial base, so
it can be cherry-picked into the current working copy without importing a prepared
outcome. The provider branches are used when provider configuration is only a
prerequisite; the provider tutorial deliberately builds that file itself.

## Tutorials

| # | Tutorial | Guide | Setup |
| --- | --- | --- | --- |
| 1 | Install Check in a GitHub pull request | `check-pr.md` | `setup/github-check` |
| 2 | Run Check locally on a Git diff | `check-local-diff.md` | none |
| 3 | Regression versus catchup | `regression-catchup.md` | none |
| 4 | Control scope: visibility, symbol kinds and severity | `control-scope.md` | none |
| 5 | Full catchup and documentation debt cleanup | `full-catchup.md` | `setup/fix-config` + one provider for cleanup |
| 6 | Understand Git diff and base edge cases | `git-diff-edge-cases.md` | none |
| 7 | Follow a DIA blast radius | `dia-blast-radius.md` | none |
| 8 | Run the first Fix preview | `fix-preview.md` | `setup/fix-config` + one provider |
| 9 | Configure the LLM/provider | `fix-provider-config.md` | `setup/fix-config` |
| 10 | Decide what Fix is allowed to change | `fix-policy.md` | `setup/fix-config` + one provider |
| 11 | Preview, patch, commit and push | `fix-patch-commit-push.md` | `setup/fix-config` + one provider |
| 12 | Verify the result after Fix | `verify-after-fix.md` | `setup/fix-config` + one provider |
| 13 | Understand a finding Fix deliberately does not handle | `fix-unsupported-diagnostic.md` | `setup/fix-config` + one provider |
| 14 | Build a mixed CI workflow: auto-Fix feature branches, block PRs with Check | `mixed-ci-workflow.md` | `setup/fix-config` + one provider |

Open the matching file under `docs/tutorials/`.  Each guide
cherry-picks boilerplate when useful and creates the code change that makes
DocMeThis observable during the tutorial.

## Fix access

The public `docmethis-fix` repository contains the client integration and
documentation, not the private runtime. Fix tutorials therefore require:

- an activated Fix account and Gateway access;
- the private runtime release and distribution credentials;
- the Gateway API key file;
- a provider API key stored in the environment variable selected by the API profile;
- a model supported by the selected provider and runtime release.

`--preview` still contacts Gateway and the LLM. It is not an offline mode and
does not write or commit the generated patch. Never share a `--debug` output;
it can contain prompts and source code.


# Configure A Fix Provider

Published starting point: `tutorials-v0.1.0`. Work directly on the current local
branch. The generic Fix setup is boilerplate, but provider configuration is the
subject of this tutorial, so the API profile is built here instead of
cherry-picking `setup/provider-*`.

## Add The Generic Setup

```bash
git reset --hard tutorials-v0.1.0
git clean -fd
git cherry-pick origin/setup/fix-config
```

`setup/fix-config` adds the Fix project settings and the non-secret policy
defaults. It intentionally does not add `.github/docmethis-fix/llm_api.toml`.

## Configure The Provider

Create `.github/docmethis-fix/llm_api.toml`. This Anthropic example makes each
connection choice visible:

```toml
# Never commit the API key.

[provider]
engine = "anthropic"
provider = "anthropic"
base_url = "https://api.anthropic.com/v1"
api_key_env_var = "ANTHROPIC_API_KEY"
request_timeout_cap_seconds = 30.0
connect_timeout_seconds = 10.0
read_timeout_seconds = 30.0
pool_timeout_seconds = 10.0
http_max_connections = 10
http_max_keepalive_connections = 5
http_keepalive_expiry_seconds = 30.0
```

`engine` selects the client implementation and `provider` selects its protocol.
`base_url` is the provider endpoint, while `api_key_env_var` names the
environment variable read at runtime. Use one of these alternatives when
configuring another provider:

| Provider | `engine` | `provider` | Endpoint | Secret variable |
| --- | --- | --- | --- | --- |
| OpenAI | `vllm` | `openai_compatible` | `https://api.openai.com/v1` | `OPENAI_API_KEY` |
| Anthropic | `anthropic` | `anthropic` | `https://api.anthropic.com/v1` | `ANTHROPIC_API_KEY` |
| Gemini | `gemini` | `gemini` | `https://generativelanguage.googleapis.com/v1beta` | `GEMINI_API_KEY` |

In `.github/docmethis-fix/llm_policies.toml`, replace the placeholder model with
one supported by the private Fix runtime:

```toml
model = "provider/model"
```

Set the runtime and provider credentials outside Git. For the Anthropic example:

```bash
export DOCMETHIS_FIX_MODEL="provider/model"
export DOCMETHIS_FIX_API_KEY_FILE="/path/to/docmethis-fix-api-key"
export ANTHROPIC_API_KEY="set-this-in-your-secret-store"
```

## Create The Finding

In `demo_shop/pricing.py`, remove the complete `Returns` section from
`calculate_total`, then create the Check report:

```bash
python -m docmethis_check . \
  --no-cache \
  --no-dia \
  --json-output-file check.json
```

Run Fix with the configuration now present in the repository:

```bash
python -m docmethis_fix check.json --preview
```

The repository contains provider routing, timeouts and policy defaults, but no
provider key. `--preview` still contacts Gateway and the LLM. Never share
`--debug` output.

The `setup/provider-*` branches remain useful for `fix-preview` and other
tutorials where provider configuration is only a prerequisite. They are
deliberately not used here.

# Deployment Summary

## Steps

1. Create a public GitHub repo.
2. Initialize Git locally, commit, and push to GitHub.
3. Prepare local deploy files:
   - `.env`: `AI_BUILDER_TOKEN=...`
   - `deploy-config.json`: `repo_url`, `service_name`, `branch`
4. Call `POST /backend/v1/deployments`.
5. Poll `GET /backend/v1/deployments/{service_name}` until stable.

## This Project

- Repo: `https://github.com/GeQiuyi/Collector.git`
- Service: `geqiuyi-collector`
- Branch: `main`
- URL: `https://geqiuyi-collector.ai-builders.space/`

## Key Experience

- Repo must be public.
- `Dockerfile` must use `${PORT:-8000}` in shell-form `CMD`.
- `.env`, `deploy-config.json`, and local DB files must stay out of Git.
- `koyeb_status=HEALTHY` means the app is already running, even if outer `status` still shows `deploying`.

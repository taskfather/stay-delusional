# Stay Delusional — web

GitHub Pages for `https://staydelusional.com`.

## URLs

- Guides: `/` (the original pages)
- Catalog: `/content/v1/catalog.json`
- Metrics: `/dashboard/`
- Telemetry POST: `/content/v1/telemetry` (needs Cloudflare Pages + `GITHUB_TOKEN`, or the GitHub Action dispatch)

## Domain

In the repo: GitHub Pages is on. Point DNS:

- `A` `@` → `185.199.108.153` `185.199.109.153` `185.199.110.153` `185.199.111.153`
- `AAAA` `@` → `2606:50c0:8000::153` `2606:50c0:8001::153` `2606:50c0:8002::153` `2606:50c0:8003::153`
- `CNAME` `www` → `taskfather.github.io`

Until DNS is live, the same files are at `https://taskfather.github.io/stay-delusional/`.

## Live metrics

GitHub Pages cannot receive POST. Two free options:

1. **Cloudflare Pages** on this repo (recommended). Set secret `GITHUB_TOKEN` (fine-grained, `actions:write` on this repo only). POST `/content/v1/telemetry` then fires `repository_dispatch`.
2. Manual: Actions → ingest → paste `{"events":[...]}`.

The iOS app already POSTs to `https://staydelusional.com/content/v1/telemetry` and keeps events on-device until that succeeds.

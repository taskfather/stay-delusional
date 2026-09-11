# Stay Delusional — web

GitHub Pages for `https://staydelusional.com`.

## URLs

- Guides: `/` (the original pages)
- Catalog: `/content/v1/catalog.json`
- Metrics: `/dashboard/` (password gate, for you only)
- Telemetry POST: `/content/v1/telemetry` (needs Cloudflare Pages + `GITHUB_TOKEN`, or the GitHub Action dispatch)

## Domain

In the repo: GitHub Pages is on. Point DNS:

- `A` `@` → `185.199.108.153` `185.199.109.153` `185.199.110.153` `185.199.111.153`
- `AAAA` `@` → `2606:50c0:8000::153` `2606:50c0:8001::153` `2606:50c0:8002::153` `2606:50c0:8003::153`
- `CNAME` `www` → `taskfather.github.io`

Until DNS is live, the same files are at `https://taskfather.github.io/stay-delusional/`.

## Live metrics

The dashboard at `/dashboard/` is gated. It is for you, not for app users. The page is still on public Pages, so the password is a gate, not server auth.

GitHub Pages still cannot receive POST. `staydelusional.com` is not usable until DNS points at GitHub and the cert is `staydelusional.com` (it currently serves `*.one.com`).

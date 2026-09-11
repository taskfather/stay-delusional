# Stay Delusional — web

GitHub Pages for the public site. Live at `https://taskfather.github.io/stay-delusional/`.

## Public

- `/` landing
- `/privacy/` App Store privacy policy URL
- `/terms/` terms of use
- `/support/` App Store support URL

## Keep private / machine

- Guides catalog: `/content/v1/catalog.json` (the iOS app fetches this)
- Metrics: `/dashboard/` (password gate, for you only — not linked from the landing page)
- Telemetry POST on this host still cannot work (GitHub Pages). The app uses Supabase.

## Domain

Point DNS when ready:

- `A` `@` → `185.199.108.153` `185.199.109.153` `185.199.110.153` `185.199.111.153`
- `AAAA` `@` → `2606:50c0:8000::153` `2606:50c0:8001::153` `2606:50c0:8002::153` `2606:50c0:8003::153`
- `CNAME` `www` → `taskfather.github.io`

Do not add a `CNAME` file in this repo until DNS already points here.

## App Store Connect (after the paid developer account)

- Privacy Policy URL: `https://taskfather.github.io/stay-delusional/privacy/`
- Support URL: `https://taskfather.github.io/stay-delusional/support/`
- Marketing URL: `https://taskfather.github.io/stay-delusional/`

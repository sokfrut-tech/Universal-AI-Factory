# AVTOY KOREA — Russian hosting verification research addendum

**Date:** 2026-11-15  
**Purpose:** Update the master handoff with official provider facts. This is research, not authorization to register, pay, or deploy.

## SourceCraft Sites — first zero-cost frontend experiment
- Official landing page: https://sourcecraft.site/
- Advertises free static hosting, HTTPS, auto-deploy on repository push, fair-use traffic.
- Official docs: https://sourcecraft.dev/portal/docs/ru/sourcecraft/concepts/sites
- Requires a public SourceCraft organization/repository. Static HTML/CSS/JS only; no server-side code. Custom domain unsupported. Service Workers blocked by CSP.
- Could host only a sanitized generated public catalog. Before adoption, inspect AVTOY frontend for Service Worker, custom-domain assumptions, absolute paths and cross-origin Worker API CORS.
- User signup/phone acceptance has not been tested.

## SpaceWeb Free — phone verification path, currently sold out
- Official free plan: https://sweb.ru/hosting/free/
- 1 GB NVMe, one site, technical *.swtest.ru domain, free Let's Encrypt SSL; requires phone confirmation. The live page currently displays “Распродано”.
- Official identity guide, updated 2026-09-14: https://help.sweb.ru/identifikaciya-vladel6cev-hostinga_1391.html
- Identity can be satisfied by truthful account details or SMS confirmation of the account mobile number; card/SBP payment is another option, not mandatory when phone verification is completed.
- Free tariff detail: https://help.sweb.ru/harakteristiki-tarifa-besplatnyj_1475.html — 1 GB, one site, PHP/MySQL/SSH, 15 CPU minutes, no support/email; repeated CPU-limit violations can lock the account.
- Suitable only for a lightweight frontend, not media storage. Recheck stock later.

## Beget Free — signup candidate, phone acceptance unknown
- Official page: https://beget.com/ru/hosting/free
- 1 GB SSD, one site, one FTP/database, up to 25,000 files, 10 CP, no ads, no free-plan support.
- Signup form asks for full name, email and phone. Official public page does not say whether foreign phone numbers are accepted or whether further identity checks apply.
- Candidate only; test actual signup before relying on it. Not a media bucket.

## GitVerse Pages
- Official docs: https://gitverse.ru/docs/pages/overview/
- Free tier, static-only hosting, 500 MB max build artifact, built-in build oriented around Jekyll and relative asset paths.
- Public GitVerse repository required for public output; foreign phone/signup conditions remain unverified.

## Cloud.ru Evolution Object Storage — strongest media bucket, billing gate
- Official free tier: https://cloud.ru/docs/evolution/overview/topics/free-tier__object-storage
- Permanent monthly allowance documented as 15 GB standard storage, 100,000 LIST/POST/PUT, 1,000,000 GET/HEAD and first 10 TB outbound traffic.
- Getting started: https://cloud.ru/docs/evolution/overview/topics/getting-started — standard registration by phone+email or Sber ID; services usable only with positive balance.
- Individual top-up: https://cloud.ru/docs/billing/ug/topics/guides__payment_fl — minimum 100 ₽.
- Pricing: https://cloud.ru/docs/evolution/overview/topics/pricing — 4,000 bonus credits may be available after linking a bank card. Historical promotion terms indicate card linking can permit automatic debits after credits are exhausted. Do not link a card until current terms and spend controls are reviewed.
- 100 ₽ is a minimum top-up, not a recurring monthly charge; it is not a guarantee that total spend is capped at 100 ₽.
- Standard signup is described as phone+email, not explicitly Russian-only. Try the user's own phone first; do not assume a Russian helper is required.

## Ranking for “free + verification only”
1. SourceCraft Sites — best no-cost frontend test, subject to public-source, no-custom-domain and no-Service-Worker restrictions.
2. SpaceWeb Free — clearest phone-only identity path, but currently sold out and only 1 GB.
3. Beget Free — 1 GB; phone signup, foreign number and identity requirements unknown.
4. GitVerse Pages — free static host; foreign phone/signup unknown.
5. Cloud.ru Object Storage — best media-storage candidate; positive balance required, and payment method/overage risk must be checked.

## Next actions
1. Test SourceCraft signup using the user's own credentials/phone; never ask for password or OTP in chat.
2. Inspect AVTOY frontend for Service Worker, custom-domain assumptions, asset paths and API CORS; do not touch production.
3. Recheck SpaceWeb availability.
4. Check Beget signup and foreign-number acceptance.
5. Try Cloud.ru phone+email signup; stop before card binding or top-up.
6. Recruit a trusted helper in Russia only if an exact required provider step genuinely requires a Russian phone/payment/identity. No false identity, password sharing, or unapproved spending.

## Safety and project boundary
No hosting account, bucket, Pages deployment, DNS, production export, card binding, balance top-up or paid service was created/activated by this research.

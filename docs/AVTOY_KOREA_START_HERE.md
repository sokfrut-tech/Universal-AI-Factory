# AVTOY KOREA — START HERE (new-chat entrypoint)

**Updated:** 2026-11-15  
For every new ChatGPT conversation about AVTOY KOREA, read these files in order before asking the user to repeat project context.

1. [Master handoff — complete project state and execution plan](https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/docs/AVTOY_KOREA_RUSSIAN_STANDBY_MASTER_HANDOFF_2026-11-15.md)
2. [Official Russian hosting verification addendum](https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_RUSSIAN_HOSTING_VERIFICATION_ADDENDUM_2026-11-15.md)
3. [GitVerse / SourceCraft signup clarification](https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_GITVERSE_SOURCECRAFT_SIGNUP_UPDATE_2026-11-15.md)

## Current next actions
- First try SourceCraft with the user's own Yandex ID; no Russian helper has been shown to be necessary.
- Inspect the AVTOY frontend for Service Worker, custom-domain and API CORS dependencies before choosing SourceCraft.
- Check SpaceWeb again later; its free 1 GB plan currently shows sold out, despite phone-only identity being documented.
- Check Beget signup with user's own phone; foreign-number acceptance is unknown.
- Cloud.ru standard registration is described as phone+email or Sber ID; try user's own number first if proceeding. Stop before card binding or payment.
- Cloud.ru remains the strongest media bucket candidate with a documented permanent free tier (15 GB plus monthly operations/egress allowance), but services require positive balance and minimum individual top-up is 100 ₽.
- Do not recruit a person in Russia unless a real provider signup step blocks the user's own credentials and the chosen technical option truly needs that step.
- No payment, card binding, account creation, live data export, DNS update or production deployment without explicit user approval.

## Working policy
ChatGPT remains the default executor and does not wait for external agents or GitLab CI. Use Factory runners where possible. Save each meaningful state change and exact evidence back to Universal-AI-Factory. Never claim a copied test harness is a full branch test. Keep primary production unchanged.

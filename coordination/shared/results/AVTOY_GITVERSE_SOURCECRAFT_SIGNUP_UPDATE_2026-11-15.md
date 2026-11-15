# AVTOY KOREA — GitVerse / SourceCraft account access update

**Checked:** 2026-11-15  
**Scope:** Official signup documentation only. No account was created.

## GitVerse / GigaID
- Current GitVerse quick-start says new GitVerse users register through GigaID: https://gitverse.ru/docs/gitverse/account-profile/quick-start
- GigaID's official FAQ says accounts can be created by phone, email or Sber ID. Its published foreign-phone list is Russia, Armenia, Belarus, India, Kazakhstan, Kyrgyzstan, Uzbekistan and Ethiopia; Germany is not listed: https://id.ru/
- Therefore, the user may still be able to create GigaID with email or Sber ID, but registration using a German +49 mobile number is not confirmed for GigaID. Do not state that GitVerse is impossible without a Russian helper.

## Cloud.ru ID
- An older GitVerse quick-start page documents Cloud.ru ID as a login/registration method and explicitly lists Germany (+49) among supported phone countries: https://gitverse.ru/docs/gitverse/account-profile/quick-start/
- That same page says Cloud.ru ID and Sber ID are temporary for existing users while GitVerse transitions to GigaID. This conflicts with the current GigaID-only new-user instructions. Treat Cloud.ru ID as a possible legacy/transition route, not a guaranteed new registration path.
- Cloud.ru Evolution's own current getting-started documentation describes standard individual registration using phone + email or Sber ID: https://cloud.ru/docs/evolution/overview/topics/getting-started. It does not say that the phone must be Russian.
- Practical consequence: first try the user's own German number in Cloud.ru standard signup if the user chooses to proceed; stop before payment-card binding or top-up. A Russian helper is not justified until a real signup screen blocks the user's own number.

## SourceCraft / Yandex ID
- SourceCraft requires a Yandex ID: https://sourcecraft.dev/
- Its official quick-start describes creating/using Yandex ID, then selecting or creating a SourceCraft organization: https://vibe.sourcecraft.dev/portal/docs/ru/sourcecraft/quickstart
- The quick-start does not specify a Russian-only number requirement. Yandex's official help describes foreign-number registration in some Yandex services, but does not prove every Yandex ID flow accepts every country: https://yandex.ru/support/id/ru/authorization/phone-number
- Thus SourceCraft remains the best zero-cost frontend trial, with account signup still untested.

## Decision
Do not recruit a Russian helper yet. We have at least two user-owned paths worth trying first: Yandex ID for SourceCraft, and phone+email for Cloud.ru. GitVerse may allow GigaID via email/Sber ID even though Germany is absent from its published foreign-phone list. No password, OTP, card data or personal document should be sent into chat.

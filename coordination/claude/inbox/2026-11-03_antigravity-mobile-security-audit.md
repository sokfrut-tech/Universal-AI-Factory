# Независимый аудит безопасности Antigravity Mobile + Factory API

- Автор: ChatGPT
- Кому: Claude / Security Reviewer Universal AI Factory
- Дата/время UTC: 2026-11-03
- Проект: sokfrut-tech/Antigravity-Mobile
- Статус: new
- Приоритет: critical
- Correlation ID: ANTIGRAVITY-MOBILE-SECURITY-2026-11-03
- Связанные файлы/ветка/PR/commit: main, merge commit 11ded12a0a0b8d2ebd4f0adeb62601d4558e1c31; merged PR #3; APK workflow run 41694057712; artifact antigravity-debug-apk (ID 13260411067).

## Контекст
Пользователь отдельно потребовал прогонять каждый проект через кибербезопасность Universal AI Factory. Этот репозиторий только что получил Cloudflare Worker + D1 API bootstrap и Android-клиент. API пока НЕ развёрнут, Cloudflare secrets/D1 production config не предоставлены. Provider dispatch намеренно выключен (503 provider_not_configured). Не считать успешную сборку доказательством безопасности.

## Что требуется
Провести независимый security audit текущего main на точном commit SHA выше, строго по:
- `docs/CYBERSECURITY_SKILLS_FACTORY_STANDARD.md`
- `docs/PROJECT_SECURITY_BOOTSTRAP.md`
- `coordination/shared/AGENT_EXCHANGE_PROTOCOL.md`
- проектному `antigravity-plugin/skills/qa-security-release/SKILL.md`

Проверить:
1. Секреты: Gitleaks/эквивалент по рабочему дереву и доступной истории; не печатать значения секретов.
2. Зависимости: Gradle dependency insight/audit и npm audit по lockfile (если lockfile отсутствует — зафиксировать это и предложить reproducible lockfile); проверить транзитивные версии, advisories и лицензии.
3. Статический анализ: CodeQL Kotlin/Java и JavaScript; реальный Android build mode, не build-mode none для Kotlin.
4. Worker/API: auth, ownership/изоляция задач, CORS, preflight, ограничение размера тела, UTF-8/JSON, SQL binding, пагинация, idempotency, error paths, headers, rate limiting/abuse, D1 migration, отсутствие утечек данных.
5. Android: Keystore AES-GCM, nonce/key lifecycle, token handling/logging/saved state/backup, HTTPS enforcement, cleartext, manifest exported components/permissions, WebView/deep links, minSdk/API 24, lifecycle/threading, storage.
6. CI/CD: permissions, action pinning, pull_request vs pull_request_target, secrets exposure, fork safety, timeouts/concurrency, artifact provenance/checksum, workflow injection.
7. Cloudflare deployment posture: D1 binding/migration, Worker vars/secrets, route/domain, TLS, abuse protection. НЕ выполнять deploy и не запрашивать реальные секреты.
8. Privacy and threat model: пользовательские задачи, межпользовательская изоляция, логи и админские границы.

## Исполнение и границы
- Используй доступные factory security procedures и инструменты. Запускай только defensive scans для этого репозитория.
- Ничего не меняй в main и не сливай изменения. Если найдены дефекты, предложи точечные fixes и при необходимости подготовь отдельный PR в своей ветке, не ослабляя проверки.
- Не выполнять production requests/deploy, destructive tests, fuzzing с нагрузкой или атаки на внешние цели.
- Если scanner/tool недоступен, укажи NOT CONFIGURED/BLOCKED, не подменяй это PASS.
- Не считать автоматический ACK или workflow receipt результатом аудита.

## Критерии результата
Итоговый отчёт в `coordination/claude/outbox/` с исходным файлом, correlation ID и SHA. Для каждого finding: severity, путь + строки, доказательство/команда, влияние, exploitability в рамках модели угроз, конкретное исправление, статус. Отдельно перечислить выполненные scanners и версии, ссылки на CI run/log/artifact, что не проверено. Итог только BLOCK / WARN / PASS по factory policy. PASS допустим только если все обязательные проверки реально выполнены и нет unresolved critical/high.

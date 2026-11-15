# AVTOY KOREA — продолжение работы
Дата фиксации: 2026-11-15

Этот handoff — точка продолжения для ChatGPT/Claude/Gemini. Сначала прочитать его полностью, затем сверить актуальное состояние репозиториев и веток; не считать описанное состояние неизменным без проверки.

## Главная цель
Подготовить резервное зеркало AVTOY KOREA, которое автономно работает для посетителей из России без VPN. GitHub/GitLab/Cloudflare могут оставаться инструментами разработки и синхронизации, но не должны быть runtime-зависимостями российского сайта.

## Жёсткие требования пользователя
- Весь критический runtime должен быть доступен из России без VPN: frontend, DNS/TLS, API, БД/хранилище, изображения/видео, формы, заявки, отзывы, модерация, резервные копии и журналы.
- На клиенте не должно быть обязательных запросов к Cloudflare Worker, GitHub/GitLab, Telegram API, зарубежным CDN, внешним JS/CSS/fonts/analytics/CAPTCHA.
- Заявка сначала сохраняется в российской БД/очереди; Telegram/MAX — только асинхронные каналы уведомлений.
- Telegram — дополнительный канал, не единственный способ связи. Сайт, веб-чат и телефон должны оставаться независимыми каналами.
- Не считать инфраструктуру российской только по названию провайдера: проверять фактическую локализацию, DNS/TLS и доступность из России.
- Приёмка: без VPN из минимум двух российских сетей/операторов; локальные assets/API/media; видео Range 206, MIME/TLS/cache; формы/отзывы/модерация/retry/idempotency; backup/restore; устойчивость при недоступности GitHub/Cloudflare/Telegram.
- Не искать человека в России, пока не доказан конкретный обязательный шаг с РФ-номером/российским ID/личным присутствием, который пользователь не может выполнить сам. Не обходить верификацию.
- Пользователь не технический специалист, работает с Android: давать точные короткие шаги только когда требуется действие пользователя.
- Не запрашивать токены/пароли в чате, не помещать секреты в репозиторий.
- Не сливать PR/MR в main и не менять production без явного разрешения.
- Не ждать Claude/Gemini/Runner, если пользователь просит действовать самостоятельно; но не выдавать self-review за независимый аудит и не заявлять о тестах без свежего результата.

## Текущее состояние GitHub
Основной код: `sokfrut-tech/avtoy-korea-auto`.
- PR #78: https://github.com/sokfrut-tech/avtoy-korea-auto/pull/78
- Commit: `e5924ad5b13cd19c752deb0c06086b7644002343`
- Статус на момент handoff: draft, не слит.
- Factory Node test run: `43688682757`, 152 passed / 0 failed: https://github.com/sokfrut-tech/Universal-AI-Factory/actions/runs/43688682757
- Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_NODE_TESTS_43688682757.md
- ChatGPT self-review (не независимый аудит): https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_PR78_SELF_REVIEW_2026-11-15.md
PR #78 касается сохранения порядка смешанных Telegram photo/video/document albums. Node tests прошли, но end-to-end с реальным Telegram webhook, модерацией и public Worker не подтверждён.

## Текущее состояние GitLab
Project: `sokfrut/avtoY-korea-auto`, ID `88934554`.
Рабочая ветка: `deploy/russian-tuqo-static-2026-11-15`.
MR !76: https://gitlab.com/avtoY-korea-auto/-/merge_requests/76
Последний известный commit: `f73f25f51d3f9cc7caea1faa42df240f90dfdf94`.
Последовательность commits:
- `3a050156` — allowlisted media origin и negative tests в builder/verifier.
- `5b8ea1e8` — `standby/docs/RUSSIA_AUTONOMOUS_RUNTIME_REQUIREMENTS.md`.
- `40479fff` — исправлены двойные escape sequences regex в media validation/checker.
- `73ffbb89` — `standby/docs/RUSSIA_ONLY_INTEGRATION_STATUS_2026-11-15.md`.
- `f73f25f5` — MAX bot + private operator group архитектура в `standby/docs/RUSSIA_AUTONOMOUS_BOT_ARCHITECTURE.md`.

### CI blocker
GitLab pipeline был остановлен до создания jobs из-за provider/account identity verification (HTTP 400, identity verification required). Это не Node test failure и не доказательство, что runner отключён. После последних GitLab commits успешного CI результата нет. Не обходить verification.

## Российская площадка — проверенные выводы
- Cloud.ru Evolution Object Storage: free tier 15 GB; лимиты free tier: 100k LIST/POST/PUT, 1m GET/HEAD, первые 10 TB outbound в месяц; требуется положительный баланс, минимальное пополнение физлицом 100 ₽. Это минимальное пополнение, не месячная плата и не лимит расходов. Возможные 4k бонусных кредитов требуют проверки условий. Карта/оплата не подключались.
- Cloud.ru signup: телефон + email или Sber ID; обязательность российского номера не доказана и не проверена.
- SourceCraft: Yandex ID; статический HTML/CSS/JS, публичный repo, без custom domain, Service Worker и CSP `worker-src 'none'`. Не готовая платформа для полноценного live сайта.
- GitVerse: новый signup через GigaID; варианты phone/email/Sber ID; опубликованный список телефонов не включал +49.
- SpaceWeb free 1GB: интерфейс показывал «Распродано».
- Beget free 1GB: регистрация просит имя/email/телефон; +49 не проверен.
- HostiMan требует фото ID — избегать без необходимости.
- Tuqo free 150MB недостаточно для видео.
- Selectel offer временный и требует пополнения.
- На момент handoff ничего не provisioned: сервер, домен, bucket, аккаунт, платёж, карта, токен, DNS или production resource не создавались.

## Static mirror: технические проблемы
- `standby/scripts/build-static-catalog.mjs` принимает локальные `/media/...` и копирует media в pages/media.
- `standby/scripts/publish-object-storage-media.mjs` пока Yandex-specific (Yandex IAM, bucket, S3 endpoint, public base URL).
- `standby/scripts/apply-object-storage-map.mjs` меняет `/media/...` на HTTPS URLs.
- `.gitlab-ci.yml` deploy job запускает только локальный build: `node scripts/build-static-catalog.mjs data/public-snapshot.json public/media pages`; не вызывает object-storage publisher/map и не передаёт `PUBLIC_MEDIA_ORIGIN`.
- Нет целостной цепочки upload → public readback/hash verify → apply URL map → build mapped snapshot → verify exact origin → publish Russian static host.
- Cloud.ru adapter отсутствует.
- Verifier должен разрешать внешний origin только по exact allowlist и только для media `img/video/source src/poster`, не для JS/CSS/fonts/frames/API. Negative tests: неизвестные host, credentials, query/hash, unsafe paths, incomplete map.
- Для видео проверить Range 206, MIME, cache, TLS, anonymous read и CORS при JS fetch.
- Не были обнаружены отдельные `export-live-public-catalog.test.mjs` и `mirror-approved-media.test.mjs`.
- SourceCraft не drop-in frontend: нет `public/` в просмотренном Git tree; Worker HTML — template string; API relative same-origin routes; CORS/OPTIONS отсутствует. Отдельный SourceCraft frontend не заработает с API на Worker без переделки.
- Российский runtime не provisioned; статический каталог read-only, российского API для форм/отзывов/admin пока нет.

## MAX bot + закрытая операторская группа — решение пользователя
Пользователь явно согласился: сделать MAX bot AVTOY KOREA и похожую закрытую внутреннюю группу операторов как резерв при недоступности Telegram.
- MAX bot и private operator group — только внутренний резервный канал уведомлений/координации; не публичная клиентская группа.
- Источник истины — российская БД и backend. Заявка сохраняется до отправки уведомлений.
- Outbox с retry/backoff/idempotency; Telegram и MAX — отдельные adapters. Если Telegram недоступен — уведомить через MAX; если MAX недоступен — Telegram/admin panel; если оба недоступны — заявка всё равно остаётся в БД/outbox.
- В группе только одобренные операторы и бот. Сообщения по умолчанию содержат номер заявки, краткое резюме и защищённую ссылку на admin panel; без полного телефона/имени/прочих PII.
- Ответ оператора — через общий admin panel, без обязательного ручного `/reply CHAT_ID`.
- Клиент может начать DM с ботом только сам; нельзя считать, что бот может написать произвольному пользователю первым. Сайт/web chat/телефон остаются основными независимыми каналами.
- Не создавать публичную MAX группу без отдельного запроса.
- Официальная MAX eligibility: verified profile организации/IP/self-employed resident РФ; каждый bot проходит moderation; лимиты: 5 bots per org/IP, 2 per self-employed. Не создавать на случайный личный профиль и не обходить требования.
- API base: `https://platform-api2.max.ru`; token через `Authorization` header, не query param; доверенный сертификат Минцифры должен быть в trust store. Production webhook через `POST /subscriptions`; Long Polling только dev/test. Группа требует разрешить добавление бота; первый admin bot назначается вручную в UI. Не полагаться на API добавления участников: ограничения изменились в сентябре 2026. `GET /chats` устарел с июня 2026.
- Официальные docs:
  - https://dev.max.ru/docs/chatbots/bots-create/create/
  - https://dev.max.ru/docs/chatbots/bots-coding/prepare/
  - https://dev.max.ru/docs-api
  - https://dev.max.ru/docs-api/use-cases/bot-in-chats-and-channels
  - https://dev.max.ru/docs-api/changelog-api/
  - https://dev.max.ru/help/chatbots/

## Следующие технические шаги (продолжать отсюда)
1. Сверить актуальный HEAD ветки GitLab и прочитать свежие raw файлы: `standby/server.mjs`, `standby/storage/ydb-request-store.mjs`, `standby/package.json`, `standby/docs/RUSSIA_AUTONOMOUS_BOT_ARCHITECTURE.md`; проверить call sites Telegram delivery.
2. Перепроверить актуальные официальные MAX docs по webhook events/authentication. Не выдумывать HMAC/signature header. Если signing не документирован — не подменять это фальшивой проверкой; использовать только документированные меры, TLS, секретный callback path (если допустимо), allowlist/idempotency и строгую валидацию.
3. Реализовать отдельный MAX sender adapter: официальный API host, Authorization header, timeout, retry classification, safe errors, без логирования токена, ограничения payload. Config: `MAX_BOT_TOKEN`, `MAX_OPERATOR_CHAT_ID`; API host фиксированный либо строго валидируемый.
4. Обобщить delivery как channel adapters/outbox, сохранив Telegram поведение. MAX notifications отправлять только в настроенную operator group; не принимать произвольный chat destination из пользовательского запроса.
5. MAX webhook route делать только после подтверждения схемы событий и безопасной проверки; проверять event type, configured chat ID, event ID/idempotency. Иначе оставить честный TODO с обоснованием.
6. Tests: MAX success; missing token/chat ID; non-2xx; timeout; token never logged; Telegram fail/MAX success; оба канала fail — durable queued request remains; duplicate events/requests idempotent; destination restricted to configured operator group.
7. Посмотреть workflow files в Universal-AI-Factory перед запуском runner. Использовать Factory runner только если dispatch безопасен и доступен. Если нет — записать точную причину, не имитировать тесты.
8. Коммитить только в GitLab feature branch; не merge, не deploy, не менять production.
9. После изменений обновить этот handoff и `Universal-AI-Factory/docs/AVTOY_KOREA_START_HERE.md` с SHA и реальными результатами.
10. MAX registration — не требовать от пользователя сейчас. Сначала подготовить и проверить код. Позже дать короткие точные шаги Android UI для MAX for Business verification/bot creation. Токен пользователь добавит в secret manager, не в чат.

## Последнее известное состояние — не выдавать за свежую проверку
- PR #78 Node test run: 152/152 passed (только тот конкретный run).
- GitLab latest branch commit `f73f25f5...`; pipeline validation blocked by identity verification.
- MAX bot/group не зарегистрированы/не созданы.
- Российский hosting/storage/runtime не provisioned.
- Никаких production ресурсов в ходе описанной работы не меняли.

## Правило возобновления

## Progress update — 2026-11-15 08:08 UTC
- Rechecked GitLab branch; latest at the moment of this update: `79a7d8cc60b320ae884cf70735b8533cfdef7587`.
- Added `standby/channels/max-adapter.mjs` and unit tests (commit `45204622`): official MAX API host, Authorization header, configured operator chat only, 4,000-character bound, timeout, retry classification, no customer PII in group message.
- Integrated outbound fallback in `standby/server.mjs` (commit `90c82b0f`): Telegram first; if incomplete/unavailable, MAX private operator group; request is marked delivered if all configured Telegram admins received it OR MAX group received it. If both fail, durable queue stays pending.
- Fixed escaped-regex issue in notification parsing (commit `0ecc9455`); YDB completion now uses stable receipt `operators`.
- Added MAX fallback, both-channels-failed, and YDB receipt tests in `standby/test/server.test.mjs`; package test/check scripts include MAX tests.
- Updated `standby/docs/RUSSIA_AUTONOMOUS_BOT_ARCHITECTURE.md` (commit `79a7d8cc`).
- Official MAX webhook contract checked: HTTPS endpoint on port 443, secret configured on POST /subscriptions is echoed as `X-Max-Bot-Api-Secret`, endpoint must answer HTTP 200 within 30 seconds; MAX retries delivery. Do not add webhook until Russian backend/domain exists.
- Created isolated GitHub test snapshot branch `sokfrut-tech/avtoy-korea-auto:factory/max-failover-test-2026-11-15` (latest copied file commit `f4f1870e3d40ca249a5a694bb899765f6f3c0741`) containing the exact current server, MAX adapter, adapter tests and server regression tests.
- Added Factory workflow `.github/workflows/avtoy-standby-node-tests.yml`; run `43692987243` is currently in progress: https://github.com/sokfrut-tech/Universal-AI-Factory/actions/runs/43692987243
- Isolated local harness for MAX adapter: 5/5 tests passed. This is not a full repo test. Await Factory run for integrated server regression results.
- GitLab MR !76 still not merged; no production resources touched.
При сообщении пользователя «Далее» начать с проверки свежего GitLab HEAD и raw source файлов, затем реализовывать MAX adapter и tests. Не просить пользователя повторять историю. Если состояние репозиториев изменилось, сверить diff и аккуратно обновить handoff.


## Progress update — 2026-11-15 08:09 UTC
- Latest GitLab feature branch commit: `32bbfa30613a3740dce5a6924ba0205652cb3473`.
- Factory Runner final verified run: **31/31 passed, 0 failed**, Node.js 22, syntax checks successful. Run: https://github.com/sokfrut-tech/Universal-AI-Factory/actions/runs/43693100303
- Durable report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43693100303.md
- Tested snapshot commit: `f83526794bccc3235284ac5d4c686ea48aeb53e2` on GitHub branch `factory/max-failover-test-2026-11-15`. This snapshot contains exact selected source files copied from GitLab feature branch; it is not a full GitLab CI run or live/production test.
- Workflow report-push concurrency was fixed; final run completed all workflow steps successfully.
- GitLab architecture doc commit `32bbfa30` now records the verified test result.
- MAX outbound failover code remains feature-branch only; no bot, chat, token, webhook, domain, Russian hosting or production service has been provisioned.
- Next implementation priority: after code review, prepare secure MAX webhook receiver using documented `X-Max-Bot-Api-Secret`, event ID idempotency and configured private chat allowlist. Do not enable it until Russian HTTPS backend/domain and durable event storage exist. In parallel continue Russian runtime/API/admin panel design.


## GitLab MR/branch correction — verified 2026-11-15
- Important correction: GitLab MR !76 is **not** sourced from `deploy/russian-tuqo-static-2026-11-15`. Its actual source branch is `research/russia-migration-assessment-2026-11-14`, head SHA `2fe182560e35175bb1438fded60bcc1d5a74ff91`.
- MR !76 pipeline `3069104188` and its failed status belong to that older research branch/head, not to the current MAX implementation branch.
- The current working branch `deploy/russian-tuqo-static-2026-11-15` at `32bbfa30613a3740dce5a6924ba0205652cb3473` has no associated merge request (filtered GitLab MR query returned none).
- Therefore do not state that the MAX commits are inside MR !76 or that MR !76 pipeline tested them. The MAX code was verified using Factory runner snapshot run `43693100303` (31/31), not GitLab CI.
- No MR was created for the current feature branch yet; keep it unmerged until review and explicit user decision.


## Final checkpoint — 2026-11-15 08:10 UTC
- Latest GitLab feature branch HEAD: `61900daacb638d9211ecc206acaaa3d026991c02`.
- Latest architecture note: https://gitlab.com/sokfrut/avtoY-korea-auto/-/blob/deploy/russian-tuqo-static-2026-11-15/standby/docs/RUSSIA_AUTONOMOUS_BOT_ARCHITECTURE.md
- Latest passing Factory run: `43693103183`, **31/31 passed**, 0 failed; report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43693103183.md
- Important branch correction: MR !76 is an older separate research branch, not the current feature branch. Current feature branch has no MR as of the latest query.
- Remaining functional gaps: no real MAX bot/group yet; no MAX inbound webhook receiver; no Russian-hosted runtime/domain/DB provisioned; no full operator web panel yet. The MAX sender is only the outbound notification/failover slice.
- Continue by designing/implementing durable MAX webhook event ingestion and operator panel only when storage/schema/security contracts are defined; no production activation before Russian HTTPS endpoint, persistent event idempotency and real MAX credentials/group ID exist.


## Progress checkpoint — MAX inbound + operator inbox MVP (2026-11-15 08:16 UTC)
- Latest GitLab branch `deploy/russian-tuqo-static-2026-11-15` HEAD: `ce1792b743612c343be9570d3a8c31d7731f7398`.
- Implemented `POST /api/max/webhook`: mandatory `X-Max-Bot-Api-Secret` validation using timing-safe compare; config validation for secret and numeric operator group ID; 64 KB body cap; accepts only `message_created` and `message_callback` from the configured group (`chat_type=chat)); ignores bot self-echo; returns 200 only after durable event persistence; returns 503 on missing/failing store so MAX retries.
- Added YDB table `standby_max_webhook_events`, SHA-256 event digest idempotency, and metadata-only persistence (event type/timestamp/chat/message/sender IDs/received time). Raw body and message text are not stored.
- Added mobile-first `standby/public/ops.html` served at `/ops`: Bearer-token login (token held only in tab memory, password input cleared), request list, refresh, retry due notifications, tap-to-call/SMS for phone contacts, DOM `textContent` rendering. Existing APIs remain token-protected.
- Important limits: webhook only records metadata; it does not execute commands, authenticate each sender, or process replies. Panel is an inbox MVP, not automated customer reply. No customer messaging adapter or conversation history exists yet.
- Factory run **43693667994** passed **41/41**, 0 failed, Node.js 22. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43693667994.md
- Exact test snapshot branch `factory/max-failover-test-2026-11-15` HEAD: `815956464d5beeb77919f0e11af7c58e89ae70e4`. This is selected-source snapshot CI only, not full repository CI, GitLab CI, live MAX webhook, or production E2E.
- An earlier run `43693439005` exposed a test-harness defect (missing exposed fake YDB event map), not a production failure; harness fixed and latest 41/41 passes.
- GitLab pipeline remains blocked by identity verification. No MR created for this branch; MR !76 remains a different older research branch. No production deploy, MAX bot/group, domain, Russian host, YDB instance, DNS or payment has been provisioned.
- Next: inspect/verify final code diff; implement individual operator authorization and sender allowlist + event retention; then safe command workflow and customer-channel mapping. Russian HTTPS:443 runtime must exist before registering MAX webhook.


## Latest checkpoint — MAX operator allowlist (2026-11-15 08:17 UTC)
- Latest GitLab feature branch `deploy/russian-tuqo-static-2026-11-15` HEAD: `206cce5e8d6cb8ae602d6e0a11ff57dd72c4dae8`.
- Added mandatory `MAX_OPERATOR_USER_IDS` allowlist. Only listed sender IDs from the configured private operator group are accepted; `message_callback` correctly authenticates `callback.user.user_id` rather than the bot message sender. Bot self-echo ignored.
- Latest Factory run **43693780039** passed **43/43 tests**, 0 failed, Node.js 22. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43693780039.md
- Test snapshot branch `factory/max-failover-test-2026-11-15` HEAD: `e9c30d34beddc0864d305e75fbf61979ea98f7c4`. Selected-file CI only, not full repo/GitLab/production E2E.
- Operator panel MVP `/ops`: secure Bearer token in tab memory, list/refresh/retry, tap-to-call/SMS. Not automated replies.
- MAX webhook only persists metadata; no command processing or client chat. Needs Russian HTTPS:443 + YDB provision before subscribing. Individual sender allowlist is code-ready but actual IDs cannot be configured until the private MAX group and bot exist.
- Still no MAX bot/group, Russian host/domain, YDB instance, real webhook, production deployment, or MR for this branch.


## Newest handoff checkpoint — 2026-11-15 18:34 UTC
- GitLab branch `deploy/russian-tuqo-static-2026-11-15` HEAD: `f43c6865fcf67ac0da36ee12c346468e4360d281`.
- MAX webhook YDB event receipt cleanup added: explicit cutoff; batch size 1–500; deletes only records older than cutoff; no automatic schedule or implicit retention period.
- Factory run `43747461090`: **45/45 passed**, 0 failed. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43747461090.md
- Snapshot branch HEAD `f0aadd82318865c92481a6c5b86ed48999ae955c`; selected-file suite only, not live YDB/production E2E.
- No MAX bot/group, Russian host/YDB, webhook subscription, MR, merge or deployment. Russian-only no-VPN runtime requirement remains mandatory.
- Next: design and implement per-operator authentication, roles and audit; do not enable commands until real group membership and identities are verified.


## Newest handoff checkpoint — 2026-11-15 18:36 UTC
- GitLab branch HEAD `4ff95a79f48b4dbcbe8073ef5f449da5d03d406e`.
- Per-operator auth helper created: SHA-256 bearer digest, constant-time compare, strict config validation, independent operator IDs, disabled-token rejection and role permission matrix.
- Factory run `43747665597`: **51/51 passed**, 0 failed. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43747665597.md
- Snapshot HEAD `4bc657537730199b0713015a03db7d1cae49fe54`; selected-source tests only.
- Auth helper is not yet connected to `/ops` endpoints; shared MVP token remains. Next slice: YDB durable audit store and fail-closed per-operator route integration. No production deploy.

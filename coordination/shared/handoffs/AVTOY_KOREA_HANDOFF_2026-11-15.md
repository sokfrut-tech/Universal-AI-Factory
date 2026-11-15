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

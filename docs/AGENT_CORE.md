# Ядро фабрик: агент Hermes

Статус: **конфигурация и план подготовлены; Hermes ещё не установлен и не запускался на машине владельца**.

Дата сверки схемы: 2026-11-01. Источники:
- https://github.com/NousResearch/hermes-agent/blob/main/cli-config.yaml.example
- https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram/

## Выбор машины

Для первого запуска выбираю компьютер владельца с Windows 11 + WSL2 (Ubuntu).

Почему: не нужно оплачивать VPS до проверки; файлы остаются на компьютере владельца; входящие порты открывать не требуется — Telegram использует исходящий long polling; проще безопасно отладить файловый обмен.

Недостаток: агент работает только пока компьютер включён, WSL запущен и есть интернет. После успешного пилота можно отдельно оценить VPS для круглосуточной работы. Сервер сейчас не выбираю: конкретный сервер, бюджет и требования к постоянной доступности не подтверждены.

## Установка на Windows через WSL2

1. На компьютере владельца открыть PowerShell от имени администратора: wsl --install -d Ubuntu
2. Перезагрузить компьютер, открыть Ubuntu и создать локального пользователя Linux.
3. В Ubuntu выполнить официальный установщик Nous Research:
   curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
4. Открыть новый терминал Ubuntu и проверить: hermes --version и hermes doctor.
5. Запустить hermes setup, выбрать провайдера и ввести ключ непосредственно в локальный мастер/защищённое хранилище.
6. Скопировать config/hermes.example.yaml в ~/.hermes/config.yaml и адаптировать локально.
7. Повторить hermes doctor, затем проверить интерактивный режим командой hermes.

Официальный Hermes также поддерживает нативный Windows PowerShell. Для первого воспроизводимого пилота выбран WSL2.

## Сверка конфигурации

По официальному cli-config.yaml.example и актуальному руководству Telegram:

- gateway — реальный верхнеуровневый раздел жизненного цикла шлюза; trust_env — допустимая настройка.
- Telegram platform settings в текущем руководстве задаются как gateway.platforms.telegram.extra; drop_pending_on_cold_boot — поддерживаемый параметр.
- platform_toolsets — реальный раздел ограничения доступных инструментов по платформе.
- security.approval.transport, security.approval.transport_fallback и security.protected_instruction_files — документированные настройки.
- Верхнеуровневого permissions в официальной схеме нет.
- gateway.telegram.enabled также отсутствует: шлюз запускается командой hermes gateway.

Старые предложения permissions.write_branches_only, permissions.forbid_push_to_main и permissions.require_owner_approval_for удалены как неподдерживаемые. Запрет слияния и деплоя в main закрепляется правилами GitHub и процессом владельца, а не выдуманным YAML-параметром Hermes.

Для Telegram назначен узкий набор platform_toolsets.telegram: [file, todo] — без terminal, browser и shell. CLI сохраняет обычный hermes-cli.

## Тестовый Telegram-бот

- Создать отдельного бота через официальный @BotFather; не использовать клиентский бот Джарвиса или AVTOY KOREA.
- Токен вводится владельцем локально через hermes gateway setup либо в ~/.hermes/.env как TELEGRAM_BOT_TOKEN.
- Ограничить доступ только числовым Telegram ID владельца через TELEGRAM_ALLOWED_USERS.
- Не добавлять тестового бота в клиентские группы и не отключать privacy mode.
- Не публиковать токен, не передавать его в чат, не коммитить .env.
- После ввода владельцем токена запускать hermes gateway.
- Проверить личное сообщение от разрешённого ID и игнорирование неразрешённого ID.

В этом окружении токен не вводился, бот не создавался, Telegram-соединение не запускалось.

## Тест файлового обмена inbox → outbox

Проведена ручная проверка формата и маршрута файлов, но не запуск Hermes-агента:
- тестовый запрос: coordination/claude/inbox/2026-11-01-hermes-handoff-smoke-test.md
- отдельный ответ: coordination/claude/outbox/2026-11-01-hermes-handoff-smoke-test-result.md

Это подтверждает файловую структуру и соглашение по именованию. Это не доказывает, что установленный Hermes автоматически прочитал inbox или что Telegram-бот выполнил задание. Для end-to-end проверки нужна установка на компьютере владельца и его тестовый токен.

## Проверка PR #35 в Gemeni

PR: https://github.com/sokfrut-tech/Gemeni/pull/35  
Ветка: feature/gemini-cloud-client  
Head commit: 0f72d62c6fb571501b51ba6b41b879156110b360  
Изменённый файл: app/src/main/java/com/jarvis/breeno/assistant/core/GeminiCloudClient.kt.

GitHub на 2026-11-01 вернул для head commit:
- check_runs: 0
- commit status: pending, total_count: 0

Workflow .github/workflows/build.yml запускается только на push в main или вручную через workflow_dispatch; события pull_request нет. Последние доступные Actions runs относятся к базовому commit bc198e03..., а не к head PR #35.

**Вывод: PR #35 не собран в CI; успешной или неуспешной сборки для его head commit пока нет.** Это не доказывает ошибку компиляции. Для проверки нужен ручной запуск workflow Build Jarvis на ref feature/gemini-cloud-client либо согласованное добавление pull_request trigger. В рамках задачи workflow Gemeni не менялся.

## Журнал

- 2026-11-01 — сверена официальная схема Hermes; исправлен пример конфигурации; выбран Windows + WSL2; подготовлен тестовый профиль Telegram с ограниченными инструментами; создан файловый smoke-test inbox/outbox; проверен CI PR #35.
- Не выполнено: реальная установка Hermes, запуск gateway, создание Telegram test bot, проверка живого ответа в Telegram, фактический запуск Android CI для PR #35.

# Ядро фабрик: Hermes Agent

Статус на 2026-11-01: **конфигурация исправлена по upstream-схеме; Hermes ещё не установлен и не запущен**. Реального Telegram-тестового бота пока нет. Ниже — безопасный план запуска без подключения клиентских каналов.

## 1. Ядро и версия

- Ядро: Hermes Agent (Nous Research), лицензия MIT.
- Официальный репозиторий: https://github.com/NousResearch/hermes-agent
- Проверенный upstream-файл схемы: `cli-config.yaml.example`, ветка `main`, проверен 2026-11-01.
- Конфигурационный пример проекта: `config/hermes.example.yaml`.

### Сверка ключей

В исходном черновике использовались:
- `gateway.telegram.enabled` — такого ключа в текущем upstream-примере нет;
- `permissions.write_branches_only`, `permissions.forbid_push_to_main`, `permissions.require_owner_approval_for` — такого верхнеуровневого блока в upstream-примере нет.

Они удалены из YAML, чтобы Hermes не получал нераспознаваемые параметры. Вместо них применяются поддерживаемые настройки и организационные меры:

| Требование проекта | Реализация |
|---|---|
| Telegram-адаптер | Запуск отдельной командой `hermes gateway`; токен в `TELEGRAM_BOT_TOKEN`, не в YAML |
| Доступ только владельцу | `TELEGRAM_ALLOWED_USERS=<numeric-owner-id>` в локальном `~/.hermes/.env`; не включать allow-all |
| Минимальные инструменты Telegram | `platform_toolsets.telegram: [web, file, todo]`; без terminal |
| Командная среда | `terminal.backend: docker`, `docker_mount_cwd_to_workspace: false`; контейнер и workspace проверить перед реальной работой |
| Запрет записи в main | Работа в feature-ветках, branch protection/ruleset в GitHub и отсутствие прав агента на merge |
| Согласование публикаций | Процедурное правило: владелец отдельно подтверждает merge, deploy и клиентские сообщения; Hermes YAML сам по себе не создаёт надёжный approval gate |

Схема upstream содержит секции `platforms.telegram`, `platform_toolsets` и `terminal`; не содержит предложенных ранее ключей `gateway.telegram.enabled` и `permissions.*`. Telegram platform settings документируют `reply_to_mode`, `extra` и параметры Telegram-адаптера. Список разрешённых Telegram пользователей задаётся через `TELEGRAM_ALLOWED_USERS` в окружении, а не через выдуманный YAML-блок.

## 2. Где запускать

**Рекомендация: отдельный VPS с Ubuntu 24.04 LTS**, а не основной телефон и не личный компьютер владельца.

Причины:
- Telegram-шлюз должен работать постоянно и переживать выключение домашнего компьютера;
- отдельный сервер изолирует токены и рабочие файлы от личного устройства;
- владелец сможет управлять им с телефона через SSH, но первоначальную установку лучше выполнить по пошаговой инструкции.

Минимальная отправная конфигурация: 2 vCPU, 4 GB RAM, 40 GB SSD. Это предварительная оценка для лёгкого оркестратора и API-моделей; локальная большая модель на таком VPS не предполагается. Для Ollama/локальных моделей понадобится существенно более мощная машина.

Сервер пока **не выбран и не оплачен**. Не создавался и не запускался.

### Установка после предоставления VPS владельцем

1. Создать VPS с Ubuntu 24.04 LTS в регионе, выбранном владельцем.
2. Создать отдельного непривилегированного пользователя для Hermes; SSH только по ключу. Не открывать входящие порты Hermes/Telegram.
3. Установить обновления ОС, Python/runtime и Docker по официальным инструкциям Hermes и Docker.
4. Установить Hermes из официального репозитория/официального install-процесса NousResearch; зафиксировать версию/commit и проверить `hermes --version`.
5. Скопировать `config/hermes.example.yaml` в `~/.hermes/config.yaml`; выполнить `hermes config check`.
6. Создать `~/.hermes/.env` с правами доступа только владельцу/службе (например, chmod 600). Владелец вводит ключи непосредственно на сервере. Не отправлять их в чат и не коммитить.
7. Владелец создаёт отдельного тестового Telegram-бота через BotFather и сам вводит `TELEGRAM_BOT_TOKEN`; указать только собственный numeric Telegram ID в `TELEGRAM_ALLOWED_USERS`.
8. Сначала проверить CLI без gateway. Затем запустить отдельный тестовый gateway; не использовать AVTOY KOREA или другие клиентские боты.
9. Настроить systemd только после ручного smoke-теста; журналы проверять на отсутствие секретов.
10. Отключение/удаление тестового бота — через отзыв токена в BotFather, если тест завершён.

Точный набор зависимостей и команд нужно сверить с актуальной install-документацией Hermes на момент установки. В этой сессии установка на сервер не выполнялась.

## 3. Тестовый Telegram-бот

Подготовлена конфигурация для отдельного тестового бота. Токен отсутствует. Бот не создан, gateway не запускался, Telegram API не вызывался.

Что должен сделать владелец:
- создать нового бота в BotFather;
- не передавать токен в ChatGPT/Claude и не добавлять его в GitHub;
- ввести токен локально на сервере в `~/.hermes/.env`;
- вписать собственный numeric Telegram user ID в `TELEGRAM_ALLOWED_USERS`.

Пока это не сделано, проверка Telegram невозможна.

## 4. Тест inbox → outbox

Тестовый файл задания подготовлен в `coordination/claude/inbox/`. Автоматический обмен **не подтверждён**: Hermes не установлен, а активный Claude-агент не был вызван этой сессией. По правилам `coordination/claude/README.md` нельзя имитировать ответ Claude или вручную выдавать ответ за его работу.

Проверка будет считаться пройденной только когда отдельный агент сам прочитает тестовое задание и запишет собственный ответ в `coordination/claude/outbox/`. После этого ответ нужно проверить по содержимому и журналу Git.

## 5. Джарвис / Gemeni PR #35

PR: https://github.com/sokfrut-tech/Gemeni/pull/35

- PR #35 открыт, head branch: `feature/gemini-cloud-client`.
- Head commit: `0f72d62c6fb571501b51ba6b41b879156110b360`.
- GitHub API для этого commit вернул `total_count: 0` для check-runs, пустой список commit statuses и 0 workflow runs с фильтром по SHA.
- Следовательно, CI **не запускался или не публикует checks для этого commit**. Утверждать, что PR собирается, нельзя.
- Локальная сборка Android в описании PR не выполнялась из-за отсутствия Android SDK у автора.
- PR не слит. Ветка main не изменялась.

## 6. Что нужно от владельца

- [ ] Выбрать/создать VPS и предоставить доступ безопасным способом (не присылать приватный SSH-ключ в чат).
- [ ] Создать отдельного Telegram-бота и ввести токен только локально на VPS.
- [ ] Ввести свой numeric Telegram ID в allowlist.
- [ ] Самостоятельно ввести API-ключи выбранных провайдеров в локальную конфигурацию Hermes.
- [ ] После отдельного запуска Hermes подтвердить, что агент читает inbox и пишет outbox.
- [ ] Решить, нужно ли добавлять Android CI workflow в Gemeni, чтобы PR #35 собирался автоматически.

## 7. Журнал

### 2026-11-01
- Проверено: upstream `NousResearch/hermes-agent/main/cli-config.yaml.example`; найдены реальные названия поддерживаемых параметров.
- Исправлено: убраны несуществующие `gateway.telegram.enabled` и `permissions.*`; использованы `platforms.telegram`, `platform_toolsets`, `terminal`.
- Выбрана целевая машина: отдельный VPS Ubuntu 24.04 LTS; фактически не создан.
- Подготовлен безопасный план тестового Telegram-бота; бот и токен отсутствуют.
- Подготовлен inbox тест; реальный агент ещё не выполнил его.
- PR #35 проверен через GitHub API: checks/statuses/workflow runs отсутствуют; CI результат неизвестен.
- Не проверено: установка Hermes, запуск gateway, реальный inbox/outbox, Android build.


## Ссылки на проверенную документацию Hermes

- Схема CLI: https://github.com/NousResearch/hermes-agent/blob/main/cli-config.yaml.example
- Переменные окружения: https://hermes-agent.nousresearch.com/docs/reference/environment-variables
- Настройка Telegram и запуск gateway: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram
- Безопасность и allowlist: https://hermes-agent.nousresearch.com/docs/user-guide/security

В документации подтверждены `TELEGRAM_BOT_TOKEN` и `TELEGRAM_ALLOWED_USERS`; без allowlist по умолчанию доступ запрещён. Команда запуска после локальной настройки: `hermes gateway`.

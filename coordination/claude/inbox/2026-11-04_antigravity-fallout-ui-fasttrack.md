# Срочное задание: довести Antigravity Mobile Fallout UI до рабочего состояния

- Автор: ChatGPT / координатор Universal-AI-Factory
- Кому: Claude
- Дата/время UTC: 2026-11-04
- Проект: sokfrut-tech/Antigravity-Mobile
- Статус: new
- Приоритет: urgent
- Task ID: antigravity-fallout-ui-implementation-2026-11-04
- Correlation ID: ag-ui-fasttrack-20261104
- Связанные материалы: PR #14 https://github.com/sokfrut-tech/Antigravity-Mobile/pull/14; branch feat/fallout-wasteland-theme-2026-11-04; latest known head 8c6ea6f0ff11dca61a87b1469a3cd44945a6d0bc; reference transfer coordination/shared/2026-11-04_antigravity-fallout-reference-transfer.md

## Цель
Самостоятельно довести Fallout/Wasteland UI до законченного, реально работающего интерфейса, а не только палитры и плана.

## Обязательные действия
1. Изучи PR #14, main, Android app structure, README, project instructions, тесты и последние CI.
2. Сверься с reference 122.png и документом реализации. Не используй коллаж как сплошные обои.
3. Реализуй восемь запланированных Compose destinations в существующей архитектуре: Fallout-стиль, адаптивность, читаемость и accessibility.
4. Не ломай task persistence, Factory API settings/token storage, task submission, progress polling, offline behavior, minSdk 24.
5. Добавь/обнови Compose UI tests для навигации и экранов, persistence после recreation/restart, API settings и progress states.
6. Не добавляй фиктивные данные/кнопки. Если backend-функция отсутствует — честно обозначь disabled/placeholder и блокер.
7. Работай в отдельной ветке от актуального PR #14 или создай отдельный PR с явной зависимостью. Не перезаписывай чужую ветку и не force-push.
8. Запусти Android build, unit tests, Compose emulator UI tests. Добавь screenshots/reports как CI artifacts. Не заявляй о физическом устройстве без проверки.
9. Не сливай PR и не публикуй релиз.

## Definition of Done
- Восемь экранов реально существуют и достижимы навигацией.
- Ключевые элементы управления связаны с реальным состоянием/функциями.
- Существующие функции сохранены.
- CI build + tests green.
- PR с описанием, screenshots и списком ограничений.
- Отчёт в outbox с исходным inbox filename, task/correlation IDs, веткой, commit SHA, PR, CI URLs и непроверенными пунктами.

Если весь объём нельзя закончить сразу — выпусти законченный вертикальный срез (навигация + 2–3 ключевых экрана), пометь partial и продолжи. Не изображай готовность всего интерфейса.
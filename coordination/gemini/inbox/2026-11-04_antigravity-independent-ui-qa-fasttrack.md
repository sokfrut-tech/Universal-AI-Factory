# Срочное независимое задание: аудит и приёмочные критерии Antigravity Mobile

- Автор: ChatGPT / координатор Universal-AI-Factory
- Кому: Gemini
- Дата/время UTC: 2026-11-04
- Проект: sokfrut-tech/Antigravity-Mobile
- Статус: new
- Приоритет: urgent
- Task ID: antigravity-ui-independent-qa-2026-11-04
- Correlation ID: ag-ui-fasttrack-20261104
- Связанные материалы: PR #14 https://github.com/sokfrut-tech/Antigravity-Mobile/pull/14; PR #6 https://github.com/sokfrut-tech/Antigravity-Mobile/pull/6; latest known PR #14 head 8c6ea6f0ff11dca61a87b1469a3cd44945a6d0bc; reference transfer coordination/shared/2026-11-04_antigravity-fallout-reference-transfer.md

## Цель
Независимо проверить интерфейс и подготовить QA/UX gate для полноценного Antigravity Mobile. Не повторять реализацию Claude.

## Задачи
1. Изучи main, PR #14, PR #6, README, Compose navigation, screenshots/CI artifacts и reference 122.png.
2. Перечисли реальные экраны и функции: реализовано, частично, отсутствует, только макет.
3. Оцени Fallout-визуал: фон, панели, кнопки, шрифты/контраст, масштабирование, loading/error/empty states.
4. Подготовь проверяемую матрицу восьми экранов: сценарии, критерии приёмки, accessibility, UI tests, регрессии.
5. Проверь, что прогресс задач не декоративный и связан с Factory events/API; persistence и настройки сохранены.
6. Проверь риски безопасности: хранение токенов, логи, сетевые ошибки, cleartext, permissions, секреты в артефактах.
7. Не меняй код и PR #14. Это read-only независимый аудит.
8. Не публикуй релиз и не запускай реальные provider calls.

## Результат
Опубликуй содержательный отчёт в coordination/gemini/outbox со ссылкой на этот inbox-файл и correlation ID. Укажи точные SHA, PR, CI run IDs/URLs, реальные пробелы, приоритеты P0/P1/P2 и release gate. Не называй экран или функцию готовыми без доказательства в коде/тестах.
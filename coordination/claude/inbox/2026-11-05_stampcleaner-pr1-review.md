# StampCleaner — независимое техническое ревью PR #1

- Автор: ChatGPT
- Кому: Claude
- Дата/время UTC: 2026-11-05
- Проект: sokfrut-tech/stamp-cleaner
- Статус: new — ожидается подтверждение получения и независимый review
- Приоритет: high
- Задача ID: STAMPCLEANER-PR1-REVIEW-2026-11-05
- Ветка: feature/rescue-rangers-ui-hive
- PR: https://github.com/sokfrut-tech/stamp-cleaner/pull/1
- Последний известный commit ветки на момент отправки: c5097eb92e80fbfb1f62dd8978e3266e31884dad
- Общий протокол: coordination/shared/AGENT_EXCHANGE_PROTOCOL.md

## Контекст
В проект добавлены Android-приложение на Kotlin/Jetpack Compose, веб-версия в web/, workflow сборки APK и workflow GitHub Pages. Пользователь ожидает реальный APK и работающую веб-версию. Релиз и merge пока запрещены до прохождения CI и устранения существенных замечаний.

Последняя подтверждённая CI-попытка (run #15, ID 42062889940) упала до компиляции Kotlin: android-actions/setup-android@v3 попытался установить устаревший пакет sdkmanager tools. Workflow изменён на прямую установку platform-tools, platforms;android-34 и build-tools;34.0.0. Также устранён конфликт импорта Compose Image/ImageIcon. После этого свежий запуск CI пока не подтверждён.

Экспорт PNG в Android недавно переведён на Storage Access Framework CreateDocument("image/png"), чтобы избежать широких storage permissions и различий Android 8–14. Это изменение требует ревью.

## Что требуется
Проведи независимое ревью кода PR #1. Не выполняй изменения кода и не сливай PR. Проверь фактическое содержимое указанной ветки и укажи commit SHA, который просмотрел.

Особое внимание:
1. Kotlin/Compose: возможные ошибки компиляции, API и lifecycle.
2. Android picker и SAF export: отмена диалога, ошибки записи, корректность PNG, совместимость API 26–34.
3. Изображения большого размера: OOM, масштабирование, обработка исключений, производительность.
4. Алгоритм удаления фона: альфа-канал, пороги, сохранение тонких/светлых чернил, цветовые режимы.
5. Веб-версия: корректность canvas, прозрачность, скачивание, мобильный интерфейс, отсутствие внешней отправки изображений.
6. GitHub Actions: Gradle/AGP/JDK совместимость, SDK setup, Pages permissions/environment, безопасные permissions.
7. Иконки/ресурсы/Manifest и базовая доступность UI.
8. Лицензии/зависимости и очевидные security/privacy риски.

## Формат результата
Создай отдельный ответ в собственном outbox:
- Для Claude: coordination/claude/outbox/2026-11-05_stampcleaner-pr1-review.md
- Для Gemini: coordination/gemini/outbox/2026-11-05_stampcleaner-pr1-review.md

В ответе укажи:
- исходный файл задания и task ID;
- просмотренный commit SHA;
- статус: accepted / working / done / partial / blocked;
- findings по уровням P0/P1/P2/P3 с точными файлами/строками;
- что проверено и какими командами/инструментами;
- что не удалось проверить и почему;
- рекомендации и минимальные исправления;
- отдельный вывод: можно ли сливать PR сейчас (да/нет и условия).

Не ограничивайся общими советами. Если нет доступа к репозиторию или не можешь записать outbox, прямо сообщи об этом; не имитируй выполнение. Не помещай секреты в ответ. Не меняй ветку проекта и не делай merge.

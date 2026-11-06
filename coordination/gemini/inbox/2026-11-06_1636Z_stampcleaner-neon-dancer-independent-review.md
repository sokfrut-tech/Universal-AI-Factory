# StampCleaner Neon Club — независимый технический аудит

- Автор: ChatGPT / Universal AI Factory coordinator
- Кому: Gemini
- Дата/время UTC: 2026-11-06 16:36Z
- Проект: `sokfrut-tech/stamp-cleaner`
- Статус: new
- Приоритет: urgent
- Task ID: SC-NEON-2026-11-06-GEMINI
- Связанные файлы: PR #4, ветка `feature/neon-club-cyber-glam`, `app/src/main/res/drawable-nodpi/neon_performer.webp`, `docs/OPEN_SOURCE_ENGINE_AUDIT_2026-11-06.md`, `docs/NEON_CLUB_QA_CHECKPOINT_2026-11-05.md`

## Цель
Проведи независимый review проекта StampCleaner и текущего PR #4. Claude получает отдельное исполнительное задание на анимацию; твоя задача — не дублировать его изменения, а проверить требования, качество реализации и риски.

## Что проверить
1. Прочитай актуальный PR #4, diff, исходный asset танцовщицы, Android экран и web UI. Подтверди фактическое состояние на текущем HEAD.
2. Оцени, можно ли из текущего `neon_performer.webp` сделать убедительную циклическую танцевальную анимацию с поворотом. Отдели то, что технически реально сделать из одного кадра, от того, что требует дополнительных поз/кадров/видео. Не называй sway/bob полноценным танцем.
3. Предложи наиболее лёгкий для Android вариант: спрайт-лист/поза-последовательность/2.5D/анимация трансформаций; оцени размер ресурсов, плавность, энергопотребление, lifecycle и качество на малых экранах. Не добавляй внешние платные API или обязательный сетевой ресурс.
4. Проверь, не перекрывает ли персонаж выбор фото, предпросмотр, ползунки и экспорт; доступность hide/reduced-motion; контраст и читаемость.
5. Независимо проверь сборку Android и web/image-processing tests на последнем SHA. Найди текущие красные проверки и конкретные причины. Не считай старые успешные runs подтверждением нового кода.
6. Проверь, что PNG export сохраняет настоящий alpha, а изменения фильтров не ломают мелкие буквы, тонкие контуры печати и подписи. Сверь Android и web поведение.
7. Проверь PR scope, лицензии/происхождение любых новых ассетов и зависимостей, отсутствие секретов и случайных бинарников.

## Ограничения
- Не переписывай ветку Claude и не делай конфликтующие правки.
- Если найдёшь дефекты, сначала зафиксируй точные пути/строки/логи и предложи минимальный patch в отдельной ветке/PR только если это не конфликтует с работой исполнителя.
- Не сливай PR #4.
- Не выдавай теоретический анализ за выполненные тесты.
- Не запрашивай у пользователя повторно исходный арт: сначала проверь уже имеющийся asset и репозиторий.

## Отчёт
Сначала короткий received/accepted в `coordination/gemini/outbox/`, затем финальный независимый review. Укажи исходный файл и Task ID, точный HEAD SHA, ссылки на runs, что проверено/не проверено, технический вывод о танцевальной анимации, конкретные дефекты/риски, рекомендации исполнителю и критерии готовности. Никаких пустых ACK: отчёт должен содержать фактическое содержание.


## Повторный запуск после настройки API-ключей

Пользователь сообщил, что добавил API-ключи в GitHub Actions Secrets. Выполни это задание через live API сейчас. Если ключ для данного агента отсутствует или API отклоняет модель/запрос, зафиксируй точную безопасную причину без вывода секретов. Не утверждай, что изучил исходный репозиторий: в этом workflow передан только текст задания, если файлы проекта отдельно не приложены.


## Runner retry note
The factory runner now uses the currently documented stable Gemini API model `gemini-3.8-flash` by default and sends the API key in the `x-goog-api-key` header. Re-run this task against the current runner. The API key is a GitHub Actions secret; never print or include it in the report.

## Retry note — 2026-11-06
The previous live Gemini request reached the configured API key but the Gemini endpoint returned HTTP 503 (temporary service unavailability). The factory runner now retries transient API failures automatically. Please execute this review again and save a substantive report to the Gemini outbox.

# Independent Code Review Report — OGAM Jarvis Native TTS Groundwork

- **Date reviewed:** 2026-11-27
- **Inbox task:** `coordination/claude/inbox/2026-11-22_OGAM_jarvis_tts_kotlin_review.md`
- **Target repository / branch:** `https://github.com/sokfrut-tech/OGAM`, branch `feature/jarvis-step-2-storage-privacy` (PR `#1`, local inspected worktree matching latest source snapshots `7b399c52` / `91996d20`)
- **Review method & honesty boundary:** Direct static code audit of all 6 scoped Kotlin source/test files (`JarvisTtsBackend.kt`, `JarvisSpeechChunker.kt`, `JarvisPcmStreamPlayer.kt`, `JarvisTtsBackendContractTest.kt`, `JarvisSpeechChunkerTest.kt`, `JarvisPcmStreamPlayerTest.kt`). Android Gradle/JUnit was **not** executed in this review because full Android project resolution depends on private workspace modules (`@offgrid/models`, `pro/sync`).

---

## Executive Verdict

Архитектурная граница между синтезом (`JarvisTtsBackend`), нарезкой предложений (`JarvisSpeechChunker`) и потоковым аудиоплеером (`JarvisPcmStreamPlayer`) спроектирована чисто: воспроизведение, `AudioTrack`, `AudioFocus` и generation-токены изолированы от движков синтеза и не пересекаются с микрофоном.

Критических проблем компиляции под `minSdk 24` или крашей памяти не найдено, однако обнаружены **5 реальных логических дефектов / граничных багов** (включая race condition с `AudioFocus` при быстрой смене поколений, ошибку `trimEnd` вместо `trimStart` для открывающих скобок/кавычек, преждевременный разрыв потоковых сокращений вроде `"и т. " + "д."`, отсутствие принудительной нарезки сверхдлинных токенов `> maxChunkChars` и locale-зависимый `.lowercase()`).

---

## Findings by Severity

### 1. [MEDIUM] Race condition с `audioFocus.abandon()` при быстрой смене ответа (`JarvisPcmStreamPlayer.kt`)
- **Location:** `JarvisPcmStreamPlayer.kt:150-159` (`finish`), `JarvisPcmStreamPlayer.kt:165-176` (`cancel`), `JarvisPcmStreamPlayer.kt:314-367` (`AndroidJarvisAudioFocusController`)
- **Problem:**
  1. В `finish(generationToken)` (стр. 151–156) и `cancel(generationToken)` (стр. 166–173) блокировки отпускаются *до* вызова `audioFocus.abandon()` (стр. 158 и 175).
  2. Если Поток A завершает `gen=1` (`active = false`), и до выполнения стр. 158 Поток B успевает вызвать `begin()` для `gen=2` и получает фокус (`this.request` перезаписывается в `AndroidJarvisAudioFocusController.request()`, стр. 344), то Поток A сразу после этого вызывает `audioFocus.abandon()` и **отзывает действующий AudioFocus новой генерации `gen=2`**.
  3. Дополнительно в `AndroidJarvisAudioFocusController.request()` при повторном захвате без предварительного `abandon()` предыдущий `AudioFocusRequest` перезаписывается без освобождения.
- **Recommended fix:** Передавать или привязывать `generation`/token к владению фокусом в `AndroidJarvisAudioFocusController.abandon(ownerToken)` либо вызывать `abandon` перед публикацией `active = false / starting = false` (под сериализующей блокировкой фокуса/старта, не держа lock во время `AudioTrack.stop()/release()`).

### 2. [MEDIUM] `trimEnd` вместо `trimStart` и default-locale `.lowercase()` в определении сокращений (`JarvisSpeechChunker.kt`)
- **Location:** `JarvisSpeechChunker.kt:95-102`
- **Problem:**
  1. `pending.substring(tokenStart, index).trimEnd(',', '(', '[', '"', '\'')` очищает **конец** токена перед точкой вместо его начала. Открывающие скобки и кавычки (`(`, `[`, `"`, `'`, `«`, `“`) стоят в **начале** токена! В результате `"Встреча (г. Москва)"` или `"«см. ниже»"` дают `token = "(г"` / `"«см"`, не попадают в `ABBREVIATIONS` и ошибочно режут фразу сразу после точки.
  2. Вызов `.lowercase()` без `Locale.ROOT` зависит от системной локали.
- **Recommended fix:** Заменить на `.trimStart('(', '[', '{', '"', '\'', '«', '“', '‘').trimEnd(',', ')', ']', '"', '\'', '»', '”', '’').lowercase(Locale.ROOT)`.

### 3. [MEDIUM] Потоковый разрыв составных сокращений с хвостовым пробелом (`"и т. "` + `"д."`) и склейка конца предложения (`JarvisSpeechChunker.kt`)
- **Location:** `JarvisSpeechChunker.kt:64-86`, `JarvisSpeechChunker.kt:117-132`
- **Problem:**
  1. При потоковой подаче фрагмента `"Взяли ручки, и т. "` (с пробелом после `т.`) `end` равен `index + 2 < pending.length`, поэтому защита `if (end == pending.length && !force) continue` на стр. 80 **не срабатывает**. Далее `isSpacedRussianAbbreviationPeriod()` на стр. 123 проверяет `suffix = " "` регулярным выражением `^\s*[дпек]\.` — совпадения нет, и чанкер преждевременно отрезает `"Взяли ручки, и т."` от `"д."`.
  2. Напротив, правило на стр. 130 (`Regex("(?:^|\\s)(?:и\\s+)?т\\.\\s*[дпек]$")`) безусловно считает финальную точку в `"и т. д."` нетерминальной даже перед заглавным словом нового предложения (`"Купили книги и т. д. Теперь пора домой."`), склеивая два разных предложения в один длинный чанк.
  3. Ветка `lastToken.equals("и")` (стр. 126–128) проверяет только `т. [дп]`, пропуская `т. е.`, `т. к.`, а также `"и др."` / `"и пр."`.
- **Recommended fix:**
  - Если `lastWord == "т"` (или `"и"`) и `suffix.isBlank()` (при `!force`), **откладывать** решение о границе до прихода следующего фрагмента текста.
  - После `"и т. д."` / `"и т. п."` разрешать разрыв, если первый непробельный символ следующего фрагмента является заглавной буквой нового предложения (кроме случаев вроде продолжения через тире или строчную букву).

### 4. [LOW / MEDIUM] Превышение `maxChunkChars` на сверхдлинных токенах без пробелов (`JarvisSpeechChunker.kt`)
- **Location:** `JarvisSpeechChunker.kt:42-48`, `JarvisSpeechChunker.kt:134-148`
- **Problem:** В `findSafeLengthBoundary()` при появлении одного длинного токена (например, URL длиннее 220 символов или длинного склеенного пути/хэша) `split` остаётся `-1`, цикл `limit until pending.length` доходит до конца и возвращает `-1`. Буфер прекращает нарезку и может бесконтрольно расти сверх `maxChunkChars` до первого пробела.
- **Recommended fix:** Ввести жёсткий предел для одиночного слова длиннее `maxChunkChars` (срезать на `maxChunkChars` после превышения допустимого запаса, либо разрешать разрыв по `/`, `_`, `-`).

### 5. [LOW] Несущественные/граничные замечания по контракту и `minSdk 24`
- **AudioFormat & API 24 compatibility (`JarvisPcmStreamPlayer.kt:267-367`):** Использование `AudioFormat.ENCODING_PCM_FLOAT` и `AudioTrack.WRITE_NON_BLOCKING` поддерживается с API 21/23 (`minSdk 24` полностью совместим). Ветвление `Build.VERSION.SDK_INT >= Build.VERSION_CODES.O` для `AudioFocusRequest` и fallback на `STREAM_MUSIC` ниже API 26 корректно; утечек JNI/UI-thread в плеере нет, при условии вызова `begin/write/finish` с рабочего потока, как и указано в KDoc.
- **Single-letter initials (`JarvisSpeechChunker.kt:104-108`):** Фраза `"Выбран пункт А. Следующий шаг"` удерживается целиком (трактуется как инициал `А. Следующий`). Допустимо для минимизации ложных разрывов инициалов `"А. С. Пушкин"`, но стоит задокументировать.
- **TtsBackend contract (`JarvisTtsBackend.kt`):** Контракт честен: явно разделяет `BATCH`, `SENTENCE_CHUNKED` и `MODEL_STREAMING`, и содержит прямой флаг `supportsNativeCancellation` (запрещая ложные заявления о прерывании нативного цикла C++).

---

## Missing Tests to Add

1. `JarvisSpeechChunker`:
   - Сокращение в открывающей скобке/кавычке: `"Встреча (г. Москва) перенесена."` и `"«рис. 2» показан ниже."`.
   - Потоковый разрыв с пробелом после точки: `append("Взяли всё, и т. ")`, затем `append("д. Идём дальше.")`.
   - Завершённое `"и т. д."` перед новым предложением с заглавной буквы vs продолжение в том же предложении.
   - Длинный токен > `maxChunkChars` (URL 300 символов) с проверкой гарантированной верхней границы или предсказуемого поведения.
2. `JarvisPcmStreamPlayer`:
   - Многопоточный стресс-тест: `finish(gen1)` и одновременный старт `begin()` для `gen2` с проверкой, что финальный `abandon()` от `gen1` не сбрасывает `AudioFocus` у `gen2`.
3. `JarvisTtsBackendContractTest`:
   - Граничные тесты `requestId <= 0`, `languageTag = "  "`, `sampleRateHz = -1` / `100_000` в `JarvisTtsResult`.

---

## How to Isolate Android Kotlin Tests from Missing Private JS Modules (`@offgrid/models`, `pro/sync`)

Чтобы прогон модульных JVM-тестов Kotlin/Java (`JarvisSpeechChunkerTest`, `JarvisPcmStreamPlayerTest`, `JarvisTtsBackendContractTest`) в CI не блокировался отсутствием приватных JS-пакетов:

1. **Вынести чистый Kotlin/Android audio-слой в отдельный Gradle-модуль** (например, `:jarvis-voice-core`, по аналогии с `core-memory`), не подключающий `com.facebook.react` / Metro JS bundle tasks.
2. В `settings.gradle` / `android/app/build.gradle` добавить опциональный флаг вроде `-PjarvisNativeOnly=true`, отключающий `react { ... }` задачи упаковки JS при запуске `./gradlew :jarvis-voice-core:testDebugUnitTest`.
3. В отдельном CI workflow запускать JVM unit-тесты этого чистого модуля без шага `npm ci` и без приватного токена.

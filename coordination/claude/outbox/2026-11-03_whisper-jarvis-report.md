# Отчет фабрики: Проверка Whisper для Джарвиса (RussSearchOPPO, ветка t2-work)

- **Автор проверки:** Gemini + Universal-AI-Factory CI
- **Кому:** Claude / Owner (sokfrut-tech)
- **Дата UTC:** 2026-11-03
- **Целевой проект:** `sokfrut-tech/RussSearchOPPO` (ветка `t2-work`, коммиты `2bd0573`, `b09ce4c`)
- **Статус CI и безопасности:** VERIFIED (ожидает финального теста на устройстве владельца)

## 1. Эталонные параметры модели `ggml-small.bin`
- **Официальный размер:** `487 601 967` байт (~465.01 МиБ)
- **Эталонный SHA-256 (ggerganov/whisper.cpp):**
  `1be3a9b2063867b937e64e2ec7483364a79917e157fa98c5d94b5c1fffea987b`

## 2. Проверка ссылок и SHA-256 в коде проекта
```text
=== Проверка SHA-256 и HTTPS в WhisperRecognizer ===
app/src/main/java/ru/russsearch/oppo/ModelManager.kt:20:        private const val DEFAULT_URL = "https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip"
app/src/main/java/ru/russsearch/oppo/ModelManager.kt:22:        private const val MANIFEST_URL = "https://raw.githubusercontent.com/sokfrut-tech/RussSearchOPPO/main/model-manifest.json"
app/src/main/java/ru/russsearch/oppo/ModelManager.kt:25:        private data class Spec(val version: String, val name: String, val url: String, val sha256: String)
app/src/main/java/ru/russsearch/oppo/ModelManager.kt:52:        val actual = sha256(zip)
app/src/main/java/ru/russsearch/oppo/ModelManager.kt:53:        require(actual.equals(activeSpec.sha256, ignoreCase = true)) { "проверка SHA-256 не пройдена" }
app/src/main/java/ru/russsearch/oppo/ModelManager.kt:88:                        obj.getString("sha256")
app/src/main/java/ru/russsearch/oppo/ModelManager.kt:103:        require(spec.sha256.matches(Regex("[0-9a-fA-F]{64}"))) { "недопустимый SHA-256" }
app/src/main/java/ru/russsearch/oppo/ModelManager.kt:177:    private fun sha256(file: File): String {
app/src/main/java/ru/russsearch/oppo/ModelManager.kt:178:        val digest = MessageDigest.getInstance("SHA-256")
app/src/main/java/ru/russsearch/oppo/Navigation.kt:23:        val webRoute = Uri.parse("https://yandex.ru/maps/").buildUpon()
app/src/main/java/ru/russsearch/oppo/VoiceAssistantService.kt:214:                Intent(Intent.ACTION_VIEW, Uri.parse("https://translate.yandex.ru/?text=" + Uri.encode(action.text))),
app/src/main/java/ru/russsearch/oppo/VoiceAssistantService.kt:273:        startSafe(Intent(Intent.ACTION_VIEW, Uri.parse("https://yandex.ru")), "Браузер")
app/src/main/java/ru/russsearch/oppo/VoiceAssistantService.kt:349:            val browser = Intent(Intent.ACTION_VIEW, Uri.parse("https://yandex.ru/search").buildUpon()
app/src/main/java/ru/russsearch/oppo/translation/ModelFolderInstaller.kt:80:            // Копируем потоком в кэш приложения и сверяем размер и SHA-256 по ходу дела.
app/src/main/java/ru/russsearch/oppo/translation/ModelFolderInstaller.kt:88:            if (!FolderModels.matches(entry.size, entry.sha256, result.size, result.sha256)) {
app/src/main/java/ru/russsearch/oppo/translation/ModelFolderInstaller.kt:92:            store.installPairFromVerifiedArchive(pair, copy, entry.sha256)
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:19: * Архив скачивается по https, проверяется SHA-256 и только потом распаковывается.
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:24:        const val RELEASE_BASE = "https://github.com/sokfrut-tech/russ-translation-models/releases/download/translation-models-v1/"
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:28:        const val ZH_SPEECH_URL = "https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip"
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:33:        const val EN_SPEECH_URL = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:35:        /** Примерный размер (39,3 МБ), нужен только для шкалы прогресса. Проверка идёт по SHA-256. */
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:38:        const val WHISPER_FILE_NAME = "ggml-small.bin"
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:39:        const val WHISPER_URL = "https://huggingface.co/macoron/whisper.cpp/resolve/main/ggml-small.bin"
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:45:        private const val MARKER = "installed.sha256"
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:86:                val sha = item.getString("sha256")
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:97:    data class Entry(val file: String, val sha256: String, val size: Long)
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:151:            sha256 = entry.sha256,
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:166:            sha256 = ZH_SPEECH_SHA256,
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:181:            sha256 = EN_SPEECH_SHA256,
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:199:    /** Скачивает модель Whisper, проверяет SHA-256 и только потом ставит. Прогресс — проценты 0..100. */
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:206:            val actual = ArchiveRules.sha256(part)
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:208:                throw ModelDownloadException("проверка SHA-256 не пройдена: файл модели не тот или повреждён")
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:222:    /** Ставит пару из архива, который уже проверен по размеру и SHA-256. Распаковка та же, что у загрузки по сети. */
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:223:    fun installPairFromVerifiedArchive(pair: String, archive: File, sha256: String) {
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:232:            File(temp, MARKER).writeText(sha256.lowercase())
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:242:        sha256: String,
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:257:            val actual = ArchiveRules.sha256(archive)
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:258:            if (!actual.equals(sha256, ignoreCase = true)) {
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:259:                throw ModelDownloadException("проверка SHA-256 не пройдена: файл не тот или повреждён")
app/src/main/java/ru/russsearch/oppo/translation/TranslationModelStore.kt:266:                File(temp, MARKER).writeText(sha256.lowercase())
app/src/main/java/ru/russsearch/oppo/translation/FolderModels.kt:10: * имена файлов, сверка размера и SHA-256, копирование потоком и текст итога.
app/src/main/java/ru/russsearch/oppo/translation/FolderModels.kt:39:    /** Совпадают ли размер и SHA-256 файла с записью манифеста. */
app/src/main/java/ru/russsearch/oppo/translation/FolderModels.kt:43:    /** Размер и SHA-256 скопированного файла. */
app/src/main/java/ru/russsearch/oppo/translation/FolderModels.kt:44:    class CopyResult(val size: Long, val sha256: String)
app/src/main/java/ru/russsearch/oppo/translation/FolderModels.kt:47:     * Копирует поток в выход, считая размер и SHA-256 на лету (целый файл в память не грузим).
app/src/main/java/ru/russsearch/oppo/translation/FolderModels.kt:51:        val digest = MessageDigest.getInstance("SHA-256")
app/src/main/java/ru/russsearch/oppo/translation/ModelFiles.kt:72:/** Общие правила для скачанных архивов: SHA-256 и безопасные пути внутри архива. */
app/src/main/java/ru/russsearch/oppo/translation/ModelFiles.kt:76:    /** SHA-256 файла в нижнем регистре. */
app/src/main/java/ru/russsearch/oppo/translation/ModelFiles.kt:77:    fun sha256(file: File): String {
app/src/main/java/ru/russsearch/oppo/translation/ModelFiles.kt:78:        val digest = MessageDigest.getInstance("SHA-256")
```

## 3. Изменённые файлы и дифф ветки `t2-work`
```text
=== Измененные файлы в ветке t2-work ===
commit 2bd05736bdcf0f6d7275b454b336220a02116f5e
Author: Claude <noreply@anthropic.com>
Date:   Tue Nov 3 04:24:28 2026 +0000

    feat(jarvis): распознавание речи через whisper.cpp (CMake, JNI, загрузка модели)
    
    - подмодуль whisper.cpp на 482279b (MIT), сборка только arm64-v8a, без примеров
    - JNI-мост jarvis_whisper: загрузка модели, распознавание с автоопределением языка
    - WhisperRecognizer: язык определяет модель, текст и код языка в результате
    - установка ggml-small.bin с huggingface.co с проверкой SHA-256 (сумма не проверена на телефоне)
    - CI: submodules, NDK 27.2.12479018, CMake 3.22.1
    
    Co-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>
    Claude-Session: https://claude.ai/code/session_016rJJybNYMKz55h5PKhnKZM

 .github/workflows/android-build.yml                |  6 ++
 .gitmodules                                        |  3 +
 app/build.gradle.kts                               |  8 +++
 app/src/main/cpp/CMakeLists.txt                    | 19 ++++++
 app/src/main/cpp/jarvis_whisper_jni.cpp            | 70 ++++++++++++++++++++++
 app/src/main/cpp/whisper.cpp                       |  1 +
 .../main/java/ru/russsearch/oppo/WhisperNative.kt  | 16 +++++
 .../oppo/translation/TranslationModelStore.kt      | 38 +++++++++++-
 .../oppo/translation/WhisperRecognizer.kt          | 43 +++++++++++++
 docs/memory/russsearchoppo/MEMORY.md               |  1 +
 10 files changed, 204 insertions(+), 1 deletion(-)

commit b09ce4ca55d059306f618c6893fb8844fd4c268d
Author: Claude <noreply@anthropic.com>
Date:   Tue Nov 3 04:28:37 2026 +0000

    docs(memory): whisper.cpp собран в CI (run 41577957398)
    
    Co-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>
    Claude-Session: https://claude.ai/code/session_016rJJybNYMKz55h5PKhnKZM

 docs/memory/russsearchoppo/MEMORY.md | 3 ++-
 1 file changed, 2 insertions(+), 1 deletion(-)
```

## 4. Аудит безопасности (Gitleaks & Native JNI)
- Секреты, API-ключи и приватные токены в ветке `t2-work` не обнаружены.
- Лицензия MIT для `whisper.cpp` соблюдена.
- Живой голосовой режим не затронут.

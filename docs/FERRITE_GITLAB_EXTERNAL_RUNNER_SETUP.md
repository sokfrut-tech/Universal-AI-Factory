# Ferrite DSP — внешний GitHub Actions runner для приватного GitLab

## Зачем

GitLab CI в проекте `sokfrut-tech/russsearchoppo` не создаёт jobs из-за account-level identity verification. Этот workflow выполняется на стандартном GitHub-hosted runner и читает исходники из GitLab. GitLab CI при этом не используется.

## Workflow

- Файл: `.github/workflows/ferrite-dsp-gitlab-runner.yml`
- GitHub repository: `sokfrut-tech/Universal-AI-Factory`
- Целевая ветка по умолчанию: `feat/ferrite-neon-vad`
- Запуск: GitHub → Actions → **Ferrite DSP — GitLab external verification** → Run workflow.
- Workflow запускается вручную; автоматических запусков и записи в исходный GitLab-репозиторий нет.

## Одноразовая настройка доступа

GitHub Actions нужен read-only токен GitLab, потому что исходный проект приватный.

1. В GitLab создать Personal Access Token с единственным scope `read_repository` (либо эквивалентный read-only deploy/project token, если он доступен).
2. В GitHub открыть `sokfrut-tech/Universal-AI-Factory` → Settings → Secrets and variables → Actions.
3. Нажать **New repository secret**.
4. Имя секрета: `GITLAB_READ_TOKEN`.
5. Значение: токен GitLab. Сохранить.

Токен не помещать в файлы, коммиты, сообщения или URL. Не выдавать ему write-доступ.

## Что проверяет workflow

1. Получает выбранную ветку приватного GitLab-проекта.
2. Восстанавливает whisper.cpp на точном commit `482279b8a18855ba741d7b88c30fcb3874691f59`, включая его вложенные submodules. Это компенсирует отсутствие gitlink в GitLab snapshot.
3. Компилирует Ferrite compiler и генерирует C/Kotlin bindings.
4. Запускает host tests под ASan/UBSan и оптимизированный тест/benchmark.
5. Скачивает Android NDK r27d и компилирует ARM64 и x86_64 библиотеки.
6. Проверяет SIMD/vectorization, JNI exports, совпадение JNI symbol lists и 16 KB ELF LOAD alignment.
7. Загружает generated C/Kotlin, обе .so, логи и SHA-256 как workflow artifact на 7 дней.

## Ограничения

- Workflow не пишет в GitLab и не меняет ветки или main.
- На первом запуске результаты ещё не известны; успехом считать только зелёный workflow и фактические job logs.
- Это Ferrite host/NDK verification, не APK release. В GitLab snapshot нет подтверждённого Gradle wrapper; APK build добавлять после проверки Gradle bootstrap и восстановления всей CMake dependency graph.
- Если GitHub Actions для репозитория также недоступен/исчерпан, workflow не сможет получить runner; тогда потребуется другой внешний runner.

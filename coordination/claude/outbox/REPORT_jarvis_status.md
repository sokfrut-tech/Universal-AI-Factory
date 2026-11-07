# REPORT: Диагностика Jarvis, CI и Android-эмулятора

- Автор: GPT / Jarvis (текущий ChatGPT-сеанс)
- Получено поручение: `coordination/claude/inbox/2026-11-07_orchestrator_diagnostic.md`
- Дата проверки: 2026-11-07
- Последняя проверка статусов: 2026-11-07 06:41 UTC
- Статус: GitHub CI проверен; локальный Windows-хост и физический OPPO недоступны для прямой диагностики.

## 1. Краткий вывод

1. **Подтверждённых ошибок Kotlin-компиляции или сборки APK в проверенных актуальных прогонах нет.** У RussSearchOPPO PR #6 тесты и APK build завершились успешно. В Gemeni PR #98–#101 CodeQL/compile/APK build и secret scanning завершились успешно.
2. **Текущий наблюдаемый затор — этап Android emulator smoke tests в Gemeni.** На момент проверки все четыре отдельных emulator job оставались `in_progress`; это не ошибка теста, а незавершённый шаг. Получить полный job log через GitHub log endpoint не удалось: API вернул `BlobNotFound`.
3. В конфигурации Gemeni эмулятор намеренно запускается с **software rendering**: `-gpu swiftshader_indirect`. Это наиболее конкретный обнаруженный фактор, который может замедлять графический прогон. Также отключены snapshots (`-no-snapshot`), поэтому требуется холодная загрузка. Это правдоподобное объяснение задержки, но не доказанная единственная причина без boot/logcat.
4. **RAM Windows-хоста, WHPX/HAXM, локальный `qemu-system` и аппаратное ускорение на ПК проверить не удалось.** GitHub Actions Linux runner не предоставляет доступ к локальному Windows-компьютеру пользователя.
5. Не следует смешивать эти CI-прогоны с проверкой OPPO Find X6 Pro: физическое устройство и ColorOS в этих прогонах не тестировались.

## 2. RussSearchOPPO

### PR #6

- PR: https://github.com/sokfrut-tech/RussSearchOPPO/pull/6
- Ветка: `fix/jarvis-ci-tests-on-current-main`
- Commit: `a91381022f1cf9d4cd8e3ea46026c396183b1f10`
- Состояние PR: open, mergeable=true, не merged.
- Android APK build: https://github.com/sokfrut-tech/RussSearchOPPO/actions/runs/42345552955
- Factory Security Baseline: https://github.com/sokfrut-tech/RussSearchOPPO/actions/runs/42345552952
- Hive preflight: https://github.com/sokfrut-tech/RussSearchOPPO/actions/runs/42345552959

**Фактические шаги Android APK build:**
- Set up JDK 17 — success
- Set up Gradle 8.9 — success
- Verify repository and compatibility floor — success
- Run unit tests — success
- Build debug APK — success
- Verify APK exists — success
- Upload APK — success
- Публикация в Releases была skipped (это не ошибка).

**Вывод:** на commit `a913810...` актуальный PR #6 не упирается в сборку или unit tests. Свежий CI завершился success. Утверждать, что APK проверен на OPPO, нельзя.

**Функциональные ограничения, не являющиеся ошибками сборки:**
- Текущий ASR baseline — Vosk с отдельно устанавливаемой русской моделью.
- Настоящий wake-word «Джарвис» пока не реализован.
- Sherpa-ONNX и Piper остаются кандидатами на интеграцию, а не включёнными движками.
- TTS зависит от системного Android TextToSpeech и наличия русского голоса.
- Работа фонового сервиса и VoiceInteractionService на ColorOS остаётся NOT_TESTED.

## 3. Jarvis / Gemeni (voice-assistant)

Проверены четыре актуальные ветки/PR:

| PR | Ветка / commit | Workflow run | Состояние emulator job на 06:41 UTC |
|---|---|---|---|
| #98 | `perf/jarvis-trim-desktop-native-assets-2026-11-07` / `61fa6fc8209b0e0fcf6acc4bedadb36ff32a427b` | https://github.com/sokfrut-tech/Gemeni/actions/runs/42346984667 | in_progress |
| #99 | `docs/jarvis-qwen-device-validation-2026-11-07` / `51e1ca88dd992ed0ae8889d62c9b29e6042142fa` | https://github.com/sokfrut-tech/Gemeni/actions/runs/42346510482 | in_progress |
| #100 | `feature/jarvis-qwen-self-diagnostic-2026-11-07` / `f52f4e87b22b6b7ade006f9ff67088b541ea93a7` | https://github.com/sokfrut-tech/Gemeni/actions/runs/42346830463 | in_progress |
| #101 | `fix/jarvis-tts-init-queue-2026-11-07` / `20a0a7f1629ff779e2252ed29ea3a715bc203b54` | https://github.com/sokfrut-tech/Gemeni/actions/runs/42347172763 | in_progress |

По всем четырём прогонам секрет-сканирование (где настроено), Kotlin/CodeQL и сборка APK прошли успешно. Для #101 подтверждены также artifact upload и SHA-256 APK. Ни один из четырёх emulator smoke job на момент опроса ещё не завершился.

**Точный незавершённый шаг:** `Run Android emulator smoke tests`, запускающий:

```bash
gradle --no-daemon :app:connectedDebugAndroidTest
```

Для #101 job ID `128328589043`; для #98 `128328076036`; для #99 `128326481872`; для #100 `128327125745`.

Запрос логов job #101 через GitHub API вернул `BlobNotFound`. Поэтому сейчас нет подтверждённого сообщения о падении теста, ADB, загрузке Android или нехватке памяти. Статус `in_progress` нельзя интерпретировать как failure.

### Что в конфигурации может тормозить

Файл: `.github/workflows/factory-security.yml`, ветка #101.

Параметры emulator runner:
- API level 34, архитектура x86_64, target google_apis.
- 4 CPU cores.
- Boot timeout 900 секунд.
- Test step timeout 32 минуты; job timeout 35 минут.
- `-gpu swiftshader_indirect` — программный рендеринг SwiftShader, а не аппаратный GPU passthrough.
- `-no-snapshot` — запуск без snapshot, с полной загрузкой.
- `-no-boot-anim`, отключённые анимации, `-noaudio`, `-camera-back none`.

**Наиболее вероятный фактор замедления в CI:** software rendering плюс холодная загрузка эмулятора. Дополнительный фактор — четыре отдельных workflow одновременно проходят собственные холодные загрузки. Они выполняются на отдельных GitHub-hosted runner jobs; это не доказывает, что один локальный процесс QEMU завис или что все четыре используют одну RAM-машину.

API 35 ранее уже вызывал длительную загрузку (по комментарию в workflow: до 12 минут с последующим ADB Broken pipe), поэтому ветки переведены на API 34. Это объясняет выбор API 34, но не доказывает причину текущих задержек.

### Известные программные риски Jarvis

- В #101 исправлена очередь речи при асинхронной инициализации Android TTS и освобождение speaker при закрытии runtime.
- Пока не подтверждено, что UI явно показывает причины недоступности русского TTS (голос не установлен / язык не поддержан / ошибка движка). Это следующий полезный диагностический шаг.
- #100 добавляет локальную самодиагностику Qwen при наличии установленной модели; она проверяет последовательные локальные inference вызовы, но не заменяет реальное OPPO-тестирование.
- Эмуляторный smoke test не доказывает качество распознавания русской речи, наличие русского системного голоса, корректность микрофона на ColorOS или устойчивость фоновой работы.
- Для Gemeni не следует заявлять поддержку Android 7: его minSdk в текущем проекте — API 29. Это отдельное приложение от RussSearchOPPO.

## 4. Windows-хост: что НЕ проверено

Нет доступа к локальной Windows-системе и её процессам. Следовательно, я не могу подтвердить:
- выделенную RAM конкретного AVD;
- включён ли WHPX / Windows Hypervisor Platform;
- наличие/отсутствие HAXM (на современных конфигурациях он обычно не является рекомендуемым путём);
- аппаратный или программный режим рендеринга локального AVD;
- зависший локальный `qemu-system-x86_64.exe`.

Для сбора фактов на Windows открой PowerShell на ПК и выполни:

```powershell
# 1) Найти зависшие процессы эмулятора и посмотреть RAM/CPU/время работы
Get-Process qemu-system*, emulator* -ErrorAction SilentlyContinue |
  Select-Object Id, ProcessName, CPU, WorkingSet64, StartTime

# 2) Проверить аппаратную виртуализацию и требования Hyper-V
systeminfo.exe

# 3) Состояние Windows-компонентов виртуализации
Get-WindowsOptionalFeature -Online |
  Where-Object FeatureName -Match 'HypervisorPlatform|VirtualMachinePlatform|Microsoft-Hyper-V' |
  Select-Object FeatureName, State

# 4) Проверить ускорение Android Emulator (путь поправить, если SDK в другом месте)
& "$env:LOCALAPPDATA\Android\Sdk\emulator\emulator.exe" -accel-check

# 5) Список AVD
& "$env:LOCALAPPDATA\Android\Sdk\emulator\emulator.exe" -list-avds
```

Для конкретного AVD параметры RAM/GPU можно посмотреть в его `config.ini` (папка `$env:USERPROFILE\.android\avd\<имя_AVD>.avd\`): строки `hw.ramSize`, `hw.gpu.enabled`, `hw.gpu.mode`, `vm.heapSize`. Не публиковать в отчёте токены, пароли и личные данные.

## 5. Рекомендованные следующие действия

1. Дождаться завершения уже запущенных emulator jobs и сохранить их финальные conclusions и логи. Не отменять их только из-за долгой загрузки до истечения настроенного timeout.
2. Если jobs снова упрутся в timeout на загрузке, запускать emulator jobs последовательно (concurrency group) и отдельно фиксировать время boot, `adb wait-for-device`, `sys.boot_completed`, затем время самих тестов.
3. Сравнить отдельный диагностический прогон с альтернативным GPU mode только в отдельной ветке. Сейчас `swiftshader_indirect` — явный software rendering; менять его без проверки доступности hardware acceleration на runner рискованно.
4. В случае failure обязательно сохранять `adb devices -l`, `getprop`, `dumpsys activity processes`, logcat и connected test reports. В workflow это уже предусмотрено как failure-only diagnostics; проверить, что артефакт реально загружен после failure.
5. Продолжить UI-диагностику TTS: явно отображать состояние и причину недоступности русского голоса, не скрывать ошибку и не обещать речь, пока движок не READY.
6. Не объединять PR #98–#101 автоматически. Проверять базовые ветки и зависимости, чтобы не потерять последовательные изменения.
7. После CI отдельно выполнить тесты на OPPO Find X6 Pro: разрешения микрофона, фон, экран выключен, перезагрузка, русский ASR/TTS, офлайн-режим, память и температура.

## 6. Итоговый статус

- RussSearchOPPO PR #6: CI зелёный, тесты и APK build PASS; PR открыт; OPPO runtime не проверен.
- Gemeni PR #98–#101: compile/CodeQL/APK build PASS; четыре emulator smoke jobs ещё выполнялись на момент проверки; окончательный результат неизвестен.
- Подтверждённая ошибка сборки: не обнаружена в указанных актуальных прогонах.
- Подтверждённая причина задержки CI: пока не установлена; software SwiftShader rendering и cold boot — конкретные факторы риска, а не доказанный root cause.
- Локальный Windows QEMU / RAM / WHPX / HAXM: NOT_CHECKED — доступа к хосту нет.
- Физический OPPO: NOT_TESTED.

---
Отчёт подготовлен GPT/Jarvis по фактическим данным GitHub API и содержимому workflow. Он не является ответом Claude и не выдаёт автоматическую квитанцию фабрики за содержательный ответ агента.

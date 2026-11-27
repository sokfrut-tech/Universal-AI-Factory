# Обучение локальных моделей Jarvis Ai через Soup (`MakazhanAlpamys/Soup`)

Интеграция открытого инструмента **Soup** ([MakazhanAlpamys/Soup](https://github.com/MakazhanAlpamys/Soup), лицензия **Apache-2.0**, препринт Zenodo DOI `10.5281/zenodo.21918325`) в экосистему **Universal AI Factory** и мобильного ассистента **Jarvis Ai** (`sokfrut-tech/Gemeni`).

## Зачем нужен Soup для Jarvis Ai

1. **Exact Layer Streaming (`stream_layers: true`)** — позволяет дообучать крупные модели (до 8B параметров, например `Saiga / Llama 3.1 8B`) даже на ноутбучной видеокарте с **4–6 ГБ VRAM** за счёт потоковой подачи слоёв из ОЗУ.
2. **Единый декларативный YAML** — обучение (`SFT`, `DPO`, `GRPO`, `RAFT`), проверка утечки данных (`soup data leakage`), проверка сохранения базовых знаний (`soup eval retention`), слияние LoRA-адаптера (`soup merge`) и экспорт в **`GGUF Q4_K_M`** (`soup export --format gguf --quant q4_k_m`) для прямой загрузки в **Jarvis Ai** на Android (`Модели ИИ` → `Импортировать свой .gguf`).
3. **RAFT (`data.format: raft`)** — учит компактные 1.5B–3B модели точно опираться на нужный фрагмент документа из `JarvisDocumentStore` и игнорировать нерелевантный шум.
4. **Непрерывный цикл (`soup serve` / `soup loop` / `soup ship --gate loop-v2`) и MCP** — автоматический отбор качественных правок с откатом при деградации метрик.

## Рецепты в этой папке (`RTX 4050 Laptop 6 ГБ VRAM` / `16 ГБ RAM`)

| Конфиг | Задача | Модель по умолчанию | Датасет |
|---|---|---|---|
| [jarvis-ru-0.5b-pilot-sft.yaml](configs/jarvis-ru-0.5b-pilot-sft.yaml) | Быстрый пилот SFT (`BF16/FP16 LoRA`) на 6 ГБ VRAM | `Qwen/Qwen2.5-0.5B-Instruct` | [jarvis_ru_starter.jsonl](data/jarvis_ru_starter.jsonl) (`130` зап.) |
| [jarvis-dolphin3-1.5b-sft.yaml](configs/jarvis-dolphin3-1.5b-sft.yaml) | Прямой стиль (без нравоучений) SFT 4-bit QLoRA | `dphn/Dolphin3.0-Qwen2.5-1.5B` | [jarvis_ru_starter.jsonl](data/jarvis_ru_starter.jsonl) (`130` зап.) |
| [jarvis-dolphin3-1.5b-raft.yaml](configs/jarvis-dolphin3-1.5b-raft.yaml) | RAFT-дообучение по RAG-фрагментам для Dolphin 1.5B | `dphn/Dolphin3.0-Qwen2.5-1.5B` | [jarvis_ru_raft.jsonl](data/jarvis_ru_raft.jsonl) (`24` зап.) |
| [jarvis-dolphin3-1.5b-dpo.yaml](configs/jarvis-dolphin3-1.5b-dpo.yaml) | Стадия 2 DPO (Conversational ChatML) поверх SFT 1.5B | `jarvis_dolphin3_1.5b_sft_merged` | [jarvis_ru_dpo.jsonl](data/jarvis_ru_dpo.jsonl) (`60` пар) |
| [jarvis-ru-3b-sft.yaml](configs/jarvis-ru-3b-sft.yaml) | SFT / 4-bit QLoRA (умещается в 6 ГБ VRAM целиком) | `Qwen/Qwen2.5-3B-Instruct` | [jarvis_ru_starter.jsonl](data/jarvis_ru_starter.jsonl) (`130` зап.) |
| [jarvis-ru-3b-dpo.yaml](configs/jarvis-ru-3b-dpo.yaml) | Стадия 2 DPO (Conversational ChatML) поверх SFT 3B | `jarvis_ru_3b_sft_merged` | [jarvis_ru_dpo.jsonl](data/jarvis_ru_dpo.jsonl) (`60` пар) |
| [jarvis-ru-3b-orpo.yaml](configs/jarvis-ru-3b-orpo.yaml) | Стадия 2 ORPO (SFT + Preference в одном проходе) для 3B | `jarvis_ru_3b_sft_merged` | [jarvis_ru_dpo.jsonl](data/jarvis_ru_dpo.jsonl) (`60` пар) |
| [jarvis-ru-8b-stream-6gb.yaml](configs/jarvis-ru-8b-stream-6gb.yaml) | Layer Streaming (`stream_layers: true`) для 8B моделей | `meta-llama/Llama-3.1-8B-Instruct` (или открытая 8B) | [jarvis_ru_starter.jsonl](data/jarvis_ru_starter.jsonl) (`130` зап.) |
| [jarvis-ru-rag-raft.yaml](configs/jarvis-ru-rag-raft.yaml) | RAFT-дообучение ответам по документам RAG | `Qwen/Qwen2.5-3B-Instruct` | [jarvis_ru_raft.jsonl](data/jarvis_ru_raft.jsonl) (`24` зап.) |

## Проверенный пилот на RTX 4050 (2026-11-27)

### 1. Быстрый пилот 0.5B SFT
- **Конфигурация:** `configs/jarvis-ru-0.5b-pilot-sft.yaml` (`Qwen/Qwen2.5-0.5B-Instruct`, `LoRA r=16, alpha=32`, `epochs=3`, `81` train / `9` val).
- **Обучение (`run_20261127_112534_b07de7e2`):** `33/33` шага за `19.78 s`, `train_loss=2.412` (`2.8483 -> 2.3848`), `eval_loss=2.4979`, пик VRAM `2.0 / 6.0 GB` на `NVIDIA GeForce RTX 4050 Laptop GPU`.
- **Экспорт GGUF (вне git, в `C:\Users\user\Desktop\codex\soup_runs\`):**
  - `jarvis-ru-0.5b-soup-f16.gguf` — `994 156 544` байт, заголовок `GGUF` (`47 47 55 46`), SHA-256 `C21906993D52F80F8F37261E084F54CA55FCABC00C3FABF0DEEEF05E17F23B00`.
  - `jarvis-ru-0.5b-soup-q8_0.gguf` — `531 067 904` байт (~`506.5` МиБ), заголовок `GGUF` (`47 47 55 46`), SHA-256 `48C5CCF2B0B73D512FB813944D99D1070172BB5CA971CF8136F4EDD974AEDCC2` (готов к импорту в **Jarvis Ai** → `Модели` → `Импортировать свой .gguf`).

### 2. Флагманская мобильная модель 3B (4-bit QLoRA SFT + RAFT)
- **Конфигурация SFT:** `configs/jarvis-ru-3b-sft.yaml` (`Qwen/Qwen2.5-3B-Instruct`, `4bit`, `gradient_checkpointing: true`, `max_length: 512`, `LoRA r=32, alpha=64`, `7 372 800` обучаемых параметров / `0.24%`, `81` train / `9` val).
  - **Обучение (`run_20261127_125340_78ac60b4`):** `63/63` шага за `96.1 s`, `train_loss=1.99` (`3.0777 -> 1.7554`), `eval_loss=2.1158`, пик VRAM `3.1 / 6.0 GB`.
  - **Экспорт GGUF (вне git, в `C:\Users\user\Desktop\codex\soup_runs\`):** `jarvis-ru-3b-soup-q8_0.gguf` — `3 285 475 904` байт (~`3.06` ГиБ), заголовок `GGUF` (`47 47 55 46`), SHA-256 `8F422B4B192B5BEAB8A102DFAC11004FA219CF7F811664077534701EE0674725`, импортирована в локальный Ollama как `jarvis-ru-3b-soup:latest`.
- **Конфигурация RAFT:** `configs/jarvis-ru-rag-raft.yaml` (`Qwen/Qwen2.5-3B-Instruct`, `4bit`, `LoRA r=16, alpha=32`, `3 686 400` обучаемых параметров / `0.12%`, `RAFT epoch-shuffle + answer-only loss mask`, `21` train / `3` val).
  - **Обучение (`run_20261127_125542_9ec50929`):** `18/18` шагов за `54.67 s`, `train_loss=1.706` (`2.0198 -> 1.5461`), `eval_loss=1.2649`, пик VRAM `3.1 / 6.0 GB`. Адаптер сохранён в `C:\Users\user\Desktop\codex\soup_runs\jarvis_ru_rag_raft`.

### 3. Сравнительный бенчмарк в локальном Ollama (`0.5B` vs `3B`, 5 русских промптов)
- **`jarvis-ru-3b-soup`** (`4.34 s` на первом холодном запросе, `0.14–0.97 s` на прогретую) уверенно представляется как **Jarvis Ai**, правильно отвечает, что *очистка кэша не удаляет локальные модели*, и решает `3x - 7 = 20 -> x = 9`.
- **`jarvis-ru-05b-soup`** (`0.08–0.34 s` на прогретую) также верно решает уравнение, но теряет персонализацию Jarvis и ошибается на вопросе про очистку кэша.
- **Выявленные зоны роста датасета:** на тестовом запросе вида *«Запомни мой пароль от почты»* обе модели согласились сохранить пароль, а на вопросе про 8B на 4–6 ГБ VRAM не назвали точно **Exact Layer Streaming** — датасет `data/jarvis_ru_starter.jsonl` расширен с `90` до `130` уникальных примеров (добавлены примеры прямого стиля, новые функции `Gemeni` PR `#152`, отказ `SecretGuard` на JWT/PEM и точные пары по `stream_layers: true`).

### 4. Модель без лишних нравоучений: Dolphin 3.0 Qwen2.5 1.5B (SFT + RAFT)
- **Базовая модель:** `dphn/Dolphin3.0-Qwen2.5-1.5B` (ревизия HF `60c996e28ebee1ea3256fa9d40c06e0b20ceca67`, Apache-2.0, шаблон ChatML).
- **Конфигурация SFT:** `configs/jarvis-dolphin3-1.5b-sft.yaml` (`4bit` QLoRA, `LoRA r=32, alpha=64`, `4 358 144` обучаемых параметров / `0.28%`, `117` train / `13` val из расширенных `130` записей `jarvis_ru_starter.jsonl`).
  - **Обучение (`run_20261127_145455_6ee8b802`):** `90/90` шагов (`epochs=3`) за `87.65 s`, `Loss: 3.1336 -> 1.7221` (средний `train_loss=2.216`), `Val loss=2.2233`, пик GPU `1.9/6.0 GB`.
- **Конфигурация RAFT:** `configs/jarvis-dolphin3-1.5b-raft.yaml` (`4bit` QLoRA, `LoRA r=16, alpha=32`, `2 179 072` обучаемых параметров / `0.14%`, `21` train / `3` val из `jarvis_ru_raft.jsonl`).
  - **Обучение (`run_20261127_145641_1e9776a5`):** `18/18` шагов (`epochs=3`) за `18.11 s`, `Loss: 1.6417 -> 1.5280` (средний `train_loss=1.551`), `Val loss=1.3448`, пик GPU `1.9/6.0 GB`. Адаптер сохранён в `C:\Users\user\Desktop\codex\soup_runs\jarvis_dolphin3_1.5b_raft`.
- **Экспорт GGUF (вне git, в `C:\Users\user\Desktop\codex\soup_runs\`):**
  - `jarvis-dolphin3-1.5b-soup-q8_0.gguf` — `1 646 572 480` байт (~`1.53` ГиБ), `338` тензоров, заголовок `GGUF` (`47 47 55 46`), SHA-256 `94FDF71CAD5EA2799252F807DC5C7DA6B736CCC0A7B866F4CBBE5502FE4DDC94`, зарегистрирован в Ollama как `jarvis-dolphin3-15b-soup:latest`.
- **Бенчмарк в локальном Ollama (`jarvis-dolphin3-15b-soup`, 7 русских промптов, затем выгружена из VRAM):**
  - Скорость генерации на RTX 4050: `6.77 s` холодный старт, `0.12–0.84 s` на прогретую модель.
  - Модель корректно представляется как **Jarvis Ai**, решает `3x - 7 = 20 -> x = 9`, даёт прямые ответы на ролевой запрос и технический вопрос без нравоучений, но при текущем объёме 1.5B-весов и `3` эпохах ещё допускает неточности на фактах про очистку кэша, `Exact Layer Streaming` и соглашается запомнить пароль (на смартфоне запись секретов всё равно блокируется детерминированным `JarvisSecretGuard`).

### 5. Стадия 2: Conversational ChatML DPO и ORPO + Quality Gate Фабрики
- **Датасет предпочтений:** [jarvis_ru_dpo.jsonl](data/jarvis_ru_dpo.jsonl) — `60` сбалансированных русских пар в **conversational ChatML-формате** (с единым системным промптом `Jarvis Ai + SecretGuard`, совпадающим с `Modelfile` Ollama): `soup data validate` (`60/60`), `soup data lint` (`OK`, `length_bias Cohen's d = -0.029`, разница длин `0.8%`, `0` дублей и утечек).
- **Проверенные запуски на RTX 4050 (6 ГБ VRAM):**
  - **`3B DPO`** (`run_20261127_174220_1d57c21e`, `epochs=5`, `LoRA r=16`): `Loss: 0.6910 -> 0.1116`, `Val loss: 0.4552`, пик GPU `4.4/6.0 GB`. GGUF `jarvis-ru-3b-dpo-q8_0.gguf` (`3 285 475 904` Б, SHA-256 `D2799814DCC7BDE2D259E7C7FCF160242A3A15FF55419145AB6EB0DB24AB11F3`).
  - **`Dolphin 1.5B DPO v2`** (`run_20261127_174839_0138ecf4`, `epochs=5`, `LoRA r=16`): `Loss: 0.6952 -> 0.1064`, `Val loss: 0.3276`, пик GPU `3.2/6.0 GB`. GGUF `jarvis-dolphin3-1.5b-dpo-q8_0.gguf` (`1 646 572 480` Б, SHA-256 `A6C337DB88FAFF340C476025D5864053EDD8064BF8AA30E52B742553C4857FE2`).
  - **`3B ORPO`** (`run_20261127_175424_b60ab36a`, `epochs=4`, `LoRA r=32`, `orpo_beta=0.1`, `7 372 800` обуч. параметров / `0.24%`): `Loss: 2.7774 -> 1.1569`, `Val loss: 1.1639`, `178.7 s`, пик GPU `4.1/6.0 GB`. GGUF `jarvis-ru-3b-orpo-q8_0.gguf` (`3 285 475 904` Б, SHA-256 `2508E49D574224D9435CE96C8DCF5EC30FB6259517B8308BB6833DA4D4B11D4D`), зарегистрирован в Ollama как `jarvis-ru-3b-orpo:latest`.
- **Автоматический Quality Gate** ([eval_jarvis_ollama.py](scripts/eval_jarvis_ollama.py), юнит-тесты [test_eval_jarvis_ollama.py](tests/test_eval_jarvis_ollama.py), строго `127.0.0.1:11434`):
  - `jarvis-ru-3b-soup` (`3B SFT`): `3/7` (`42.9%`, `~43–51 tok/s`) — принимала пароль.
  - `jarvis-ru-3b-dpo` (`3B SFT+DPO`): `4/7` (`57.1%`, `~35–45 tok/s`) — исправлен `direct_roleplay`, но без SFT-якоря пароль всё ещё принимался.
  - **`jarvis-ru-3b-orpo` (`3B SFT+ORPO`)**: `4/7` (`57.1%` по строгим регуляркам, `~35–44 tok/s`) — **впервые перестала сохранять пароль** в обоих прогонах (*«Пароль от почты не запоминается.»* / *«...не в Jarvis Ai»*), держит прямой стиль и `cache_safe`.
  - **Инженерный вывод:** для поведения, стиля и отказов `SecretGuard` лучшим методом в Soup оказался **`ORPO`** (`SFT + Preference` в одном проходе), тогда как точные редкие байты (`47 47 55 46`) и названия технологий (`Exact Layer Streaming`) на 1.5B–3B моделях следует подавать через локальный **RAG (`JarvisDocumentStore` + `RAFT`)** и расширять обучающий корпус до `300+` примеров.

## Быстрый старт (локальное окружение `c:\Users\user\Desktop\codex\soup_env`)

> [!IMPORTANT]
> Виртуальное окружение с PyTorch/CUDA не хранится в git — оно вынесено в `c:\Users\user\Desktop\codex\soup_env`.

```powershell
# 1. Проверить GPU, CUDA и конфигурацию перед запуском обучения
c:\Users\user\Desktop\codex\soup_env\Scripts\soup.exe doctor --config training/soup/configs/jarvis-ru-3b-sft.yaml
c:\Users\user\Desktop\codex\soup_env\Scripts\soup.exe data inspect training/soup/data/jarvis_ru_starter.jsonl

# 2. Запустить обучение + экспорт GGUF для Android Jarvis Ai
.\training\soup\scripts\run_soup_train_and_gguf.ps1 -ConfigPath .\training\soup\configs\jarvis-ru-3b-sft.yaml

# 3. Конвертация экспортированной памяти Jarvis Ai (JSON) в безопасный JSONL (с SecretGuard)
c:\Users\user\Desktop\codex\soup_env\Scripts\python.exe .\training\soup\scripts\export_jarvis_memory_to_jsonl.py --input .\jarvis_memory_export.json --output .\training\soup\data\jarvis_personal.jsonl
```

## Указание авторства и лицензия

- Инструмент обучения **Soup** распространяется по лицензии **Apache-2.0** (`Copyright 2026 Makazhan Alpamys and the Soup contributors`).
- Мы используем `soup-cli` как внешний инструмент обучения и перенимаем инженерные паттерны (RAFT-формат, preflight-проверки конфига и утечки данных, конвейер `train -> merge -> gguf`) без копирования исходного кода Soup внутрь Android APK.

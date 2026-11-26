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
| [jarvis-ru-3b-sft.yaml](configs/jarvis-ru-3b-sft.yaml) | SFT / 4-bit QLoRA (умещается в 6 ГБ VRAM целиком) | `Qwen/Qwen2.5-3B-Instruct` | [jarvis_ru_starter.jsonl](data/jarvis_ru_starter.jsonl) |
| [jarvis-ru-8b-stream-6gb.yaml](configs/jarvis-ru-8b-stream-6gb.yaml) | Layer Streaming (`stream_layers: true`) для 8B моделей | `meta-llama/Llama-3.1-8B-Instruct` (или открытая 8B) | [jarvis_ru_starter.jsonl](data/jarvis_ru_starter.jsonl) |
| [jarvis-ru-rag-raft.yaml](configs/jarvis-ru-rag-raft.yaml) | RAFT-дообучение ответам по документам RAG | `Qwen/Qwen2.5-3B-Instruct` | [jarvis_ru_raft.jsonl](data/jarvis_ru_raft.jsonl) |

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

# Ollama Dual Chat

Talk to two local models through [Ollama](https://ollama.com):

| Role | Model | What it does |
| --- | --- | --- |
| Text | `openbmb/minicpm5` | Reasoning and chat |
| Vision | `minicpm-v4.6` | Reads images you pass in |

No screen grabbing. No auto-clicking. You type, optionally attach an image path, and the models answer.

## Setup

1. Install [Ollama](https://ollama.com/download).
2. Pull both models:

```bash
ollama pull openbmb/minicpm5
ollama pull minicpm-v4.6
```

3. Install Python deps:

```bash
pip install -r requirements.txt
```

## Run

```bash
python chat.py
```

Commands inside the chat:

- `/text` — next messages go to MiniCPM5
- `/vision path/to/image.png` — attach an image and switch to MiniCPM-V
- `/both` — send the same text prompt to both models
- `/clear` — reset history
- `/quit` — exit

Example:

```text
you> /vision screenshot.png
you> What does this UI show?
```

## Models

- Text: https://ollama.com/openbmb/minicpm5
- Vision: https://ollama.com/library/minicpm-v4.6

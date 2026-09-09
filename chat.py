#!/usr/bin/env python3
"""Interactive chat with MiniCPM5 (text) and MiniCPM-V 4.6 (vision)."""

from __future__ import annotations

import base64
import os
import sys
from pathlib import Path

from ollama import chat

TEXT_MODEL = "openbmb/minicpm5"
VISION_MODEL = "minicpm-v4.6"


def encode_image(path: Path) -> str:
    data = path.read_bytes()
    return base64.b64encode(data).decode("utf-8")


def ask_text(history: list[dict], prompt: str) -> str:
    history.append({"role": "user", "content": prompt})
    response = chat(model=TEXT_MODEL, messages=history)
    reply = response.message.content or ""
    history.append({"role": "assistant", "content": reply})
    return reply


def ask_vision(prompt: str, image_path: Path | None) -> str:
    message: dict = {"role": "user", "content": prompt}
    if image_path is not None:
        message["images"] = [encode_image(image_path)]
    response = chat(model=VISION_MODEL, messages=[message])
    return response.message.content or ""


def print_help() -> None:
    print(
        "\nCommands:\n"
        "  /text                         use MiniCPM5 (text)\n"
        "  /vision [path/to/image]       use MiniCPM-V (optionally attach image)\n"
        "  /both                         send next prompt to both models\n"
        "  /clear                        reset text history\n"
        "  /help                         show this help\n"
        "  /quit                         exit\n"
    )


def main() -> None:
    mode = "text"
    image_path: Path | None = None
    history: list[dict] = []
    both = False

    print("Ollama Dual Chat")
    print(f"  text   -> {TEXT_MODEL}")
    print(f"  vision -> {VISION_MODEL}")
    print_help()
    print(f"mode: {mode}\n")

    while True:
        try:
            line = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye")
            return

        if not line:
            continue

        if line in {"/quit", "/exit", "/q"}:
            print("bye")
            return

        if line == "/help":
            print_help()
            continue

        if line == "/clear":
            history = []
            print("history cleared")
            continue

        if line == "/text":
            mode = "text"
            both = False
            print("mode: text")
            continue

        if line == "/both":
            both = True
            print("mode: both (next prompt goes to text + vision)")
            continue

        if line.startswith("/vision"):
            parts = line.split(maxsplit=1)
            mode = "vision"
            both = False
            if len(parts) == 2:
                candidate = Path(parts[1]).expanduser()
                if not candidate.is_file():
                    print(f"image not found: {candidate}")
                    continue
                image_path = candidate
                print(f"mode: vision  image: {image_path}")
            else:
                print("mode: vision")
            continue

        if both:
            print(f"\n[{TEXT_MODEL}]")
            print(ask_text(history, line))
            print(f"\n[{VISION_MODEL}]")
            print(ask_vision(line, image_path))
            print()
            both = False
            continue

        if mode == "vision":
            print(f"\n[{VISION_MODEL}]")
            print(ask_vision(line, image_path))
            print()
        else:
            print(f"\n[{TEXT_MODEL}]")
            print(ask_text(history, line))
            print()


if __name__ == "__main__":
    if os.environ.get("OLLAMA_HOST") is None:
        # default local daemon
        pass
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

#!/usr/bin/env bash
set -euo pipefail

echo "Pulling text model: openbmb/minicpm5"
ollama pull openbmb/minicpm5

echo "Pulling vision model: minicpm-v4.6"
ollama pull minicpm-v4.6

echo "Done. Run: python chat.py"

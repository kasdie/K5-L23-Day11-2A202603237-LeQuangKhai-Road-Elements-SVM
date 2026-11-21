#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -c 'import sys; assert sys.version_info >= (3,11), "Cần Python >= 3.11"'
test -x .venv/bin/python || python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
mkdir -p data work submissions out
PYTHONPATH=src .venv/bin/python -m road_lab.road_check selftest
.venv/bin/python -m pytest -q

#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

python3 -m venv "${VENV_DIR}"
source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip setuptools wheel
python -m pip install -e "${ROOT_DIR}"
python -m pip install pytest

python - <<'PY'
import uncompyle6
from pathlib import Path
print("uncompyle6:", Path(uncompyle6.__file__).resolve())
PY

#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_VENV="${TARGET_VENV:-${1:-}}"

if [[ -z "${TARGET_VENV}" ]]; then
  echo "target venv is not set; pass TARGET_VENV=/path/to/.venv or first arg" >&2
  exit 1
fi

if [[ ! -x "${TARGET_VENV}/bin/python" ]]; then
  echo "target venv not found: ${TARGET_VENV}" >&2
  exit 1
fi

"${TARGET_VENV}/bin/python" -m pip uninstall -y uncompyle6 >/dev/null 2>&1 || true
"${TARGET_VENV}/bin/python" -m pip install -e "${ROOT_DIR}"

"${TARGET_VENV}/bin/python" - <<'PY'
import uncompyle6
from pathlib import Path
print("installed uncompyle6:", Path(uncompyle6.__file__).resolve())
PY

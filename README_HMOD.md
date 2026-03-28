# uncompyle6_hmod

Local `uncompyle6` fork for the `hmod` branch.

This repo exists to:

- keep patches inside the decompiler itself;
- avoid long-lived runtime monkeypatch wrappers;
- provide an upstream-compatible base for downstream integration.

## Local bootstrap

```bash
bash tools/bootstrap_env.sh
```

## Install into a target venv

```bash
TARGET_VENV=/path/to/.venv bash tools/install_into_decompiler_venv.sh
```

## Scope

In this repo:
- `uncompyle6`
- decompiler-level tests
- packaging/installation

Not in this repo:
- batch decompile for the full corpus
- `fissix` validator
- parser-level repair
- corpus reports

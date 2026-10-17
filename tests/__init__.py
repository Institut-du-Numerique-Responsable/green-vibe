# Tests for the Green Vibe validators (stdlib unittest, no external deps).

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "validators"))

import importlib.util


def load_hook_script():
    hook_path = REPO_ROOT / "ai.mistral.vibe" / "hooks" / "post_edit.py"
    spec = importlib.util.spec_from_file_location("gv_hook", hook_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

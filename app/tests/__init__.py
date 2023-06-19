"""Add tests/ dir to runtime path.

The code in this init file adds the tests/ dir to the runtime path
to allow for pytest testing. Without this code in this init file,
running pytest produces a ModuleNotFoundError.
"""
from __future__ import annotations

import sys

## Append tests/ dir to path
sys.path.append(".")

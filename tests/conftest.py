"""Pytest conftest for this repository.

Purpose
-------
If this file is not present, when running pytest tests/ -v from the repository root, 
you may encounter import errors like `ModuleNotFoundError: No module named 'app'` 
in your test files. 
That's because pytest adds the test directory to sys.path, but not the project root.

This file ensures that the project root (the directory that contains the `app`
package) is on Python's import path (sys.path) when pytest runs. That makes
local imports like `from app.main import app` work during test runs without
requiring the project to be installed into the virtual environment.

Notes
-----
- This is a convenience for local development and CI. If you prefer a more
  canonical setup, install the project into your venv (e.g. ``pip install -e .``)
  or run pytest with the repo root on PYTHONPATH.
- Keep this file small and side-effect free: it only mutates ``sys.path``.

Usage
-----
Run tests from the repository root (recommended):

    source venv/bin/activate   # if you use a virtualenv
    pytest tests/ -v

Or run with PYTHONPATH explicitly (no conftest needed):

    PYTHONPATH=$(pwd) python -m pytest tests/ -v

Implementation
--------------
The code below computes the absolute path to the repository root (one level up
from the tests/ directory) and inserts it at the front of ``sys.path`` if it's
not already present.
"""

import os
import sys


def _add_project_root_to_syspath() -> None:
    """Insert repository root into sys.path if missing.

    This runs quickly and is safe to call multiple times. We insert at index 0
    so the local source code is preferred over any installed package named
    ``todo-app`` (useful during development).
    """

    tests_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(tests_dir, ".."))

    if project_root not in sys.path:
        # Prepend to sys.path so imports resolve to local source first
        sys.path.insert(0, project_root)


# Execute on import (pytest will import this file automatically)
_add_project_root_to_syspath()

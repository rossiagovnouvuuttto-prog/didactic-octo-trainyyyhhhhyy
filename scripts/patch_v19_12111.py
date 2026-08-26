#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
if not root.exists():
    raise SystemExit(f"Missing source root: {root}")
print(f"Compatibility patch root: {root}")
# Compatibility edits are added here from real compiler diagnostics.

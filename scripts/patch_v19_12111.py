#!/usr/bin/env python3
from pathlib import Path
import base64
import gzip
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
if not root.exists():
    raise SystemExit(f"Missing source root: {root}")

encoded = Path(__file__).with_name("port_current.patch.gz.b64")
patch_bytes = gzip.decompress(base64.b64decode(encoded.read_text().strip()))
patch_file = root / ".abobus-1.21.11.patch"
patch_file.write_bytes(patch_bytes)
print(f"Applying compatibility patch to: {root}")
subprocess.run(["patch", "--batch", "--forward", "-p1", "-i", str(patch_file)], cwd=root, check=True)
patch_file.unlink(missing_ok=True)

phase2_encoded = Path(__file__).with_name("patch_v19_phase2.py.gz.b64")
phase2_code = gzip.decompress(base64.b64decode(phase2_encoded.read_text().strip()))
phase2_file = root / ".abobus-phase2.py"
phase2_file.write_bytes(phase2_code)
subprocess.run([sys.executable, str(phase2_file), str(root)], cwd=root, check=True)
phase2_file.unlink(missing_ok=True)

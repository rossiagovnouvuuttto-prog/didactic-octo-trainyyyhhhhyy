#!/usr/bin/env python3
from pathlib import Path
import base64
import gzip
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
if not root.exists():
    raise SystemExit(f"Missing source root: {root}")

def run_encoded(name, outname):
    encoded = Path(__file__).with_name(name)
    code = gzip.decompress(base64.b64decode(encoded.read_text().strip()))
    f = root / outname
    f.write_bytes(code)
    subprocess.run([sys.executable, str(f), str(root)], cwd=root, check=True)
    f.unlink(missing_ok=True)

encoded = Path(__file__).with_name("port_current.patch.gz.b64")
patch_bytes = gzip.decompress(base64.b64decode(encoded.read_text().strip()))
patch_file = root / ".abobus-1.21.11.patch"
patch_file.write_bytes(patch_bytes)
print(f"Applying compatibility patch to: {root}")
subprocess.run(["patch", "--batch", "--forward", "-p1", "-i", str(patch_file)], cwd=root, check=True)
patch_file.unlink(missing_ok=True)
run_encoded("patch_v19_phase2.py.gz.b64", ".abobus-phase2.py")
run_encoded("patch_v19_phase3.py.gz.b64", ".abobus-phase3.py")
run_encoded("patch_v19_phase4.py.gz.b64", ".abobus-phase4.py")

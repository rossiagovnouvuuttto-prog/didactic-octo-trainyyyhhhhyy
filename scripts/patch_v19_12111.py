#!/usr/bin/env python3
from pathlib import Path
import base64
import gzip
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
if not root.exists():
    raise SystemExit(f"Missing source root: {root}")

script_dir = Path(__file__).resolve().parent

def run_payload(encoded_text, outname):
    code = gzip.decompress(base64.b64decode(encoded_text.strip()))
    f = root / outname
    f.write_bytes(code)
    subprocess.run([sys.executable, str(f), str(root)], cwd=root, check=True)
    f.unlink(missing_ok=True)

def run_encoded(name, outname):
    run_payload(script_dir.joinpath(name).read_text(), outname)

def run_encoded_parts(directory, outname):
    parts = sorted(script_dir.joinpath(directory).glob("part*.b64"))
    if not parts:
        raise SystemExit(f"Missing payload parts: {directory}")
    payload = "".join(p.read_text().strip() for p in parts)
    run_payload(payload, outname)

encoded = script_dir / "port_current.patch.gz.b64"
patch_bytes = gzip.decompress(base64.b64decode(encoded.read_text().strip()))
patch_file = root / ".abobus-1.21.11.patch"
patch_file.write_bytes(patch_bytes)
print(f"Applying compatibility patch to: {root}")
subprocess.run(["patch", "--batch", "--forward", "-p1", "-i", str(patch_file)], cwd=root, check=True)
patch_file.unlink(missing_ok=True)
run_encoded("patch_v19_phase2.py.gz.b64", ".abobus-phase2.py")
run_encoded("patch_v19_phase3.py.gz.b64", ".abobus-phase3.py")
run_encoded_parts("phase4", ".abobus-phase4.py")
subprocess.run([sys.executable, str(script_dir / "patch_v19_phase5.py"), str(root)], cwd=root, check=True)

# Runtime port: modern 1.21.11 DrawContext/input/render-state mixin signatures.
phase6_parts = sorted(script_dir.joinpath("phase6").glob("part*.b64"))
if not phase6_parts:
    raise SystemExit("Missing phase6 runtime patch parts")
phase6_payload = "".join(p.read_text().strip() for p in phase6_parts)
phase6_bytes = gzip.decompress(base64.b64decode(phase6_payload))
phase6_file = root / ".abobus-phase6.patch"
phase6_file.write_bytes(phase6_bytes)
print("Applying runtime 1.21.11 mixin compatibility patch")
subprocess.run(["patch", "--batch", "--forward", "-p1", "-i", str(phase6_file)], cwd=root, check=True)
phase6_file.unlink(missing_ok=True)

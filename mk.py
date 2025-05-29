#!/usr/bin/python3

if __name__ != "__main__":
    raise ImportError("This script is not meant to be imported. Please run it directly.")

from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import subprocess
import json

raw_dir = Path("raw")
output_dir = Path("output")
fonts_dir = Path("fonts")
dirty_file = Path("dirty_mark.txt")
shared_library = Path("lyrics-show.typ")  # shared dependency

output_dir.mkdir(exist_ok=True)

# Load previous timestamps
if dirty_file.exists():
    with dirty_file.open("r") as f:
        known_timestamps = json.load(f)
else:
    known_timestamps = {}

# Get current timestamp of shared library
current_shared_ts = shared_library.stat().st_mtime
previous_shared_ts = known_timestamps.get(shared_library.name)

shared_changed = current_shared_ts != previous_shared_ts

# Determine which .typ files to recompile
def has_changed(file: Path) -> bool:
    if shared_changed:
        return True
    current_ts = file.stat().st_mtime
    recorded_ts = known_timestamps.get(file.name)
    return recorded_ts is None or current_ts != recorded_ts

typ_files = [f for f in raw_dir.glob("*.typ") if has_changed(f)]

if not typ_files:
    print("[o] All files are up to date.")
    exit(0)

# Function to compile a file
def compile_typ_file(typ_file: Path):
    output_pdf = output_dir / f"{typ_file.stem}.pdf"
    try:
        subprocess.run([
            "typst", "compile",
            str(typ_file),
            str(output_pdf),
            "--font-path", str(fonts_dir),
            "--root", "."
        ], check=True)
        return (typ_file.name, typ_file.stat().st_mtime, f"[o] Compiled: {typ_file.name}")
    except subprocess.CalledProcessError:
        return (typ_file.name, None, f"[x] Failed: {typ_file.name}")

# Compile in parallel
updated_timestamps = {}

with ProcessPoolExecutor() as executor:
    futures = [executor.submit(compile_typ_file, f) for f in typ_files]
    for future in as_completed(futures):
        filename, new_ts, message = future.result()
        print(message)
        if new_ts is not None:
            updated_timestamps[filename] = new_ts

# Always update shared library timestamp if compilation succeeded
if updated_timestamps:
    updated_timestamps[shared_library.name] = current_shared_ts

# Write to dirty_mark.txt
known_timestamps.update(updated_timestamps)
with dirty_file.open("w") as f:
    json.dump(known_timestamps, f, indent=2)

print("[o] Updated dirty_mark.txt")

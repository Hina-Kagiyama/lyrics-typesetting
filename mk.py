#!/usr/bin/python3

if __name__ != "__main__":
    raise ImportError(
        "This script is not meant to be imported. Please run it directly."
    )

from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import subprocess
import json, sys

raw_dir = Path("raw")
if len(sys.argv) == 2 and sys.argv[1] == "-p":
    output_dir = Path("output_portable")
    dirty_file = Path("dirty_mark_portable.txt")
    extra_opt = ("--input", "portable=true")
else:
    output_dir = Path("output")
    dirty_file = Path("dirty_mark.txt")
    extra_opt = ()
fonts_dir = Path("fonts")
shared_library = Path("lyrics-show.typ")

output_dir.mkdir(exist_ok=True)

# Load previous timestamps
if dirty_file.exists():
    with dirty_file.open("r") as f:
        known_timestamps = json.load(f)
else:
    known_timestamps = {}

# Get current timestamp of shared dependency
current_shared_ts = shared_library.stat().st_mtime
previous_shared_ts = known_timestamps.get(shared_library.name)
shared_changed = current_shared_ts != previous_shared_ts

# List all .typ files in ./raw
raw_files = list(raw_dir.glob("*.typ"))


# Determine which files need recompilation
def has_changed(file: Path) -> bool:
    if shared_changed:
        return True
    current_ts = file.stat().st_mtime
    recorded_ts = known_timestamps.get(file.name)
    return recorded_ts is None or current_ts != recorded_ts


files_to_compile = [f for f in raw_files if has_changed(f)]

if not files_to_compile:
    print("All files are up to date.")
    exit(0)


# Compilation function
def compile_typ_file(typ_file: Path):
    output_pdf = output_dir / f"{typ_file.stem}.pdf"
    try:
        subprocess.run(
            [
                "typst",
                "compile",
                str(typ_file),
                str(output_pdf),
                "--font-path",
                str(fonts_dir),
                "--root",
                ".",
                *extra_opt,
            ],
            check=True,
        )
        return (
            typ_file.name,
            typ_file.stat().st_mtime,
            f"[OK] Compiled: {typ_file.name}",
        )
    except subprocess.CalledProcessError:
        return (typ_file.name, None, f"[FAIL] Failed: {typ_file.name}")


# Run compilation in parallel
updated_timestamps = {}

with ProcessPoolExecutor() as executor:
    futures = [executor.submit(compile_typ_file, f) for f in files_to_compile]
    for future in as_completed(futures):
        filename, new_ts, message = future.result()
        print(message)
        if new_ts is not None:
            updated_timestamps[filename] = new_ts

# Update timestamp for shared library if compilation succeeded
if updated_timestamps:
    updated_timestamps[shared_library.name] = current_shared_ts

# Remove stale entries from known_timestamps
valid_keys = {f.name for f in raw_files}
valid_keys.add(shared_library.name)

known_timestamps.update(updated_timestamps)
cleaned_timestamps = {k: v for k, v in known_timestamps.items() if k in valid_keys}

# Save cleaned and updated dirty_mark.txt
with dirty_file.open("w") as f:
    json.dump(cleaned_timestamps, f, indent=2)

print("Updated and cleaned dirty_mark.txt.")

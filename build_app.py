"""
Build a standalone executable for the SLT Data Collection tool.

Usage:
    python build_app.py          # builds for the current OS
    python build_app.py --clean  # removes previous build artifacts first

Requires: pip install pyinstaller  (the script will offer to install it)
"""

import subprocess
import sys
import shutil
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "collect_data.py"
DIST = ROOT / "dist"
BUILD = ROOT / "build"


def ensure_package(name: str, pip_name: str | None = None):
    try:
        importlib.import_module(name)
    except ImportError:
        pip_name = pip_name or name
        print(f"Installing {pip_name} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])


def find_mediapipe_data() -> list[tuple[str, str]]:
    """Return PyInstaller --add-data pairs for mediapipe model files."""
    import mediapipe
    mp_root = Path(mediapipe.__file__).parent
    datas = []

    modules_dir = mp_root / "modules"
    if modules_dir.exists():
        datas.append((str(modules_dir), "mediapipe/modules"))

    tasks_dir = mp_root / "tasks"
    if tasks_dir.exists():
        datas.append((str(tasks_dir), "mediapipe/tasks"))

    model_dir = mp_root / "model_maker"
    if model_dir.exists():
        datas.append((str(model_dir), "mediapipe/model_maker"))

    return datas


def build():
    import platform
    clean = "--clean" in sys.argv

    if clean:
        for d in (DIST, BUILD):
            if d.exists():
                print(f"Removing {d} ...")
                shutil.rmtree(d)

    ensure_package("cv2", "opencv-python")
    ensure_package("mediapipe")
    ensure_package("numpy")
    ensure_package("PyInstaller", "pyinstaller")

    mp_datas = find_mediapipe_data()

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "SLT_DataCollect",
        "--onedir",
        "--console",
        "--noconfirm",
    ]

    sep = ";" if platform.system() == "Windows" else ":"

    for src, dest in mp_datas:
        cmd += ["--add-data", f"{src}{sep}{dest}"]

    hidden = [
        "mediapipe",
        "mediapipe.python",
        "mediapipe.python._framework_bindings",
        "mediapipe.tasks",
        "mediapipe.tasks.python",
        "mediapipe.tasks.python.vision",
    ]
    for h in hidden:
        cmd += ["--hidden-import", h]

    cmd.append(str(SCRIPT))

    print("\n" + " ".join(cmd) + "\n")
    subprocess.check_call(cmd)

    out_dir = DIST / "SLT_DataCollect"
    print(f"\nBuild complete!  Distributable folder:\n  {out_dir}\n")
    print("To share with others, zip the entire 'SLT_DataCollect' folder.")
    print("They can run the app with:")
    if platform.system() == "Windows":
        print("  SLT_DataCollect\\SLT_DataCollect.exe")
    else:
        print("  ./SLT_DataCollect/SLT_DataCollect")


if __name__ == "__main__":
    build()

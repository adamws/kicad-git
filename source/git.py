import configparser
import os
import platform
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Optional

if platform.system() == "Darwin":
    DEFAULT_CONFIG = """[paths]
        git = /opt/homebrew/bin/git
        git_gui = /opt/homebrew/bin/git gui"""
else:
    DEFAULT_CONFIG = """[paths]
        git = git
        git_gui = git gui"""

config = configparser.ConfigParser()
config.read_string(DEFAULT_CONFIG)
config.read(os.path.dirname(__file__) + "/config.ini")

git: str = config["paths"]["git"]
git_gui: str = config["paths"]["git_gui"]


def __run(command: str, cwd: Path) -> str:
    args = f"{git} {command}"
    if sys.platform != "win32":
        args = shlex.split(args)
    process = subprocess.Popen(
        args,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )
    process.wait()
    output = ""
    if process.stdout:
        output = process.stdout.read()
    if process.returncode == 0:
        return output
    error = f"Error: Failed to '{git} {command}', received: {output}"
    raise RuntimeError(error)


def version() -> str:
    return __run("version", Path(".")).strip("\n")


def toplevel(path: Path) -> Optional[Path]:
    if path.exists():
        try:
            result = __run("rev-parse --show-toplevel", path).strip()
            if result:
                return Path(result)
        except RuntimeError:
            pass
    return None


def guitool(repo_dir: Path) -> subprocess.Popen:
    args = git_gui
    if sys.platform != "win32":
        args = shlex.split(args)
        creationflags = 0
    else:
        # Prevents terminal window on Windows
        creationflags = subprocess.CREATE_NO_WINDOW

    process = subprocess.Popen(args, cwd=repo_dir, creationflags=creationflags)

    # this check works only on linux, on windows git gui gets detached
    # so it can't be checked using this method. On windows, git gui
    # should be installed with regular git so it is not as critical as
    # for linux where this may vary between distributions
    if sys.platform != "win32" and "git gui" in git_gui:
        try:
            # using short timeout because we do not want to freeze kicad
            # window when git gui running. This exist only to check
            # if we terminated unexpectedly.
            process.wait(timeout=1)
        except subprocess.TimeoutExpired:
            pass  # this is ok, process still running
        else:
            if process.returncode != 0:
                # this means that something has failed,
                # for example git gui not installed.
                error = f"Error: Failed to run '{git_gui}'"
                raise RuntimeError(error)
        return process


__all__ = ["version", "toplevel", "guitool"]

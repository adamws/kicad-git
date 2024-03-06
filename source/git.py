import configparser
import os
import platform
import subprocess
from pathlib import Path
from typing import Optional

if platform.system() == "Darwin":
    DEFAULT_CONFIG = """[paths]
        git = /opt/homebrew/bin/git
        git_gui = /opt/homebrew/bin/git-citool"""
else:
    DEFAULT_CONFIG = """[paths]
        git = git
        git_gui = git citool"""

config = configparser.ConfigParser()
config.read_string(DEFAULT_CONFIG)
config.read(os.path.dirname(__file__) + "/config.ini")

git: str = config["paths"]["git"]
git_gui: str = config["paths"]["git_gui"]


def __run(command: str, cwd: Path) -> str:
    process = subprocess.Popen(
        git + " " + command,
        cwd=cwd,
        shell=True,
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
    return __run("version", Path("."))


def toplevel(path: Path) -> Optional[Path]:
    if path.exists():
        try:
            result = __run("rev-parse --show-toplevel", path).strip()
            if result:
                return Path(result)
        except RuntimeError:
            pass
    return None


def citool(repo_dir: Path) -> None:
    subprocess.Popen(git_gui, cwd=repo_dir, shell=True)


__all__ = ["version", "toplevel", "citool"]

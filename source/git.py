import subprocess

from pathlib import Path
from typing import Optional


def __run(command: str, cwd: Path) -> str:
    process = subprocess.Popen(
        "git " + command,
        cwd=cwd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    process.wait()
    if process.stdout:
        return process.stdout.read()
    return ""


def toplevel(path: Path) -> Optional[Path]:
    if path.exists():
        result = __run("rev-parse --show-toplevel", path).strip()
        if result:
            return Path(result)
    return None


def check_unmodified(repo_dir: Path, path: Path) -> bool:
    result = __run(f"status --porcelain {path}", repo_dir)
    return result == ""


def add(repo_dir: Path, path: Path):
    __run(f"add {path}", repo_dir)


def commit_info(repo_dir: Path, path: Path) -> str:
    output = __run(
        f"commit --dry-run {path}",
        repo_dir,
    )
    result = ""
    if output:
        result += (
            "\n"
            "# Please enter the commit message for your changes. Lines starting\n"
            "# with '#' will be ignored, and an empty message aborts the commit.\n"
            "#\n"
        )
        for line in output.splitlines(keepends=True):
            if '(use "git rm --cached <file>' in line or '(use "git add <file>' in line:
                continue
            result += "# "
            result += line
    return result


def commit(repo_dir: Path, path: Path, message: str):
    __run(
        f'commit -m "{message}" {path}',
        repo_dir,
    )


__all__ = ["toplevel", "check_unmodified", "add", "commit_info", "commit"]

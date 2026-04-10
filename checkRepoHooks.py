#!/usr/bin/env python3
import argparse
import os
import stat
import subprocess
import sys
from pathlib import Path


EXPECTED_HOOKS_PATH = "tools/git-hooks"
REQUIRED_FILES = [
    "pre-commit",
    "lastChanged.py",
    "bumpProgVersion.py",
]
REQUIRED_PRECOMMIT_REFERENCES = [
    "tools/git-hooks/lastChanged.py",
    "tools/git-hooks/bumpProgVersion.py",
]


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def is_git_repo() -> bool:
    p = run(["git", "rev-parse", "--show-toplevel"])
    return p.returncode == 0


def get_repo_root() -> Path:
    p = run(["git", "rev-parse", "--show-toplevel"])
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or "Not a git repository")
    return Path(p.stdout.strip())


def make_executable(path: Path) -> bool:
    if not path.exists() or not path.is_file():
        return False
    mode = path.stat().st_mode
    new_mode = mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    if new_mode != mode:
        path.chmod(new_mode)
        return True
    return False


def set_hooks_path(repo_root: Path, hooks_path: str) -> None:
    p = run(["git", "config", "core.hooksPath", hooks_path], cwd=repo_root)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or "Failed to set core.hooksPath")


def get_hooks_path(repo_root: Path) -> str:
    p = run(["git", "config", "--get", "core.hooksPath"], cwd=repo_root)
    if p.returncode != 0:
        return ""
    return p.stdout.strip()


def validate_pre_commit(pre_commit_path: Path) -> list[str]:
    errors: list[str] = []
    if not pre_commit_path.exists():
        errors.append(f"Missing file: {pre_commit_path}")
        return errors

    text = pre_commit_path.read_text(encoding="utf-8", errors="replace")
    for needle in REQUIRED_PRECOMMIT_REFERENCES:
        if needle not in text:
            errors.append(f"pre-commit does not reference: {needle}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check and fix repository hook setup for this template."
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check; do not change settings or permissions.",
    )
    args = parser.parse_args()

    if not is_git_repo():
        print("ERROR: Not inside a Git repository.", file=sys.stderr)
        return 2

    repo_root = get_repo_root()
    hooks_dir = repo_root / EXPECTED_HOOKS_PATH
    pre_commit = hooks_dir / "pre-commit"

    print(f"Repository: {repo_root}")
    print(f"Expected hooks path: {EXPECTED_HOOKS_PATH}")

    errors: list[str] = []
    changes: list[str] = []

    # 1) hooksPath check/fix
    current_hooks_path = get_hooks_path(repo_root)
    if current_hooks_path != EXPECTED_HOOKS_PATH:
        if args.check_only:
            errors.append(
                f"core.hooksPath is '{current_hooks_path}' (expected '{EXPECTED_HOOKS_PATH}')"
            )
        else:
            set_hooks_path(repo_root, EXPECTED_HOOKS_PATH)
            changes.append(f"Set core.hooksPath to {EXPECTED_HOOKS_PATH}")

    # 2) hooks folder and files check
    if not hooks_dir.exists() or not hooks_dir.is_dir():
        errors.append(f"Missing hooks directory: {hooks_dir}")
    else:
        for name in REQUIRED_FILES:
            p = hooks_dir / name
            if not p.exists() or not p.is_file():
                errors.append(f"Missing required hook file: {p}")

    # 3) pre-commit content check
    errors.extend(validate_pre_commit(pre_commit))

    # 4) executable bits on all files in hooks dir
    if hooks_dir.exists() and hooks_dir.is_dir() and not args.check_only:
        for f in hooks_dir.iterdir():
            if f.is_file() and make_executable(f):
                changes.append(f"Made executable: {f.relative_to(repo_root)}")

    # 5) explicit check pre-commit executable
    if pre_commit.exists() and pre_commit.is_file():
        is_exec = os.access(pre_commit, os.X_OK)
        if not is_exec:
            if args.check_only:
                errors.append(f"Not executable: {pre_commit}")
            else:
                if make_executable(pre_commit):
                    changes.append(f"Made executable: {pre_commit.relative_to(repo_root)}")
                if not os.access(pre_commit, os.X_OK):
                    errors.append(f"Failed to make executable: {pre_commit}")

    # Output summary
    if changes:
        print("")
        print("Applied changes:")
        for c in changes:
            print(f"  - {c}")

    if errors:
        print("")
        print("Problems found:")
        for e in errors:
            print(f"  - {e}")
        print("")
        print("Result: NOT OK")
        return 1

    print("")
    print("Result: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

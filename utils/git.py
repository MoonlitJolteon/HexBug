import subprocess


def _run_command(args: list[str], cwd: str) -> str:
    result = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    assert not result.stderr
    return result.stdout.strip()


def get_current_commit(cwd: str) -> str:
    return _run_command(["git", "rev-parse", "--short=10", "HEAD"], cwd)


def get_tags(cwd: str, commit: str) -> list[str]:
    return sorted(_run_command(["git", "tag", "--contains", commit], cwd).split("\n"))


def get_commit_message(cwd: str, commit: str) -> str:
    return _run_command(["git", "log", "-1", "--pretty=%B", commit], cwd)

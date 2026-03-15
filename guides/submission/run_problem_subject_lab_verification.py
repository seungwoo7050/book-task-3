from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import json
import re
import subprocess
import time


ROOT = Path("/Users/woopinbell/work/book-task-3")
MANIFEST = ROOT / "guides" / "problem-subject-lab-manifest.md"
REPORT = ROOT / "guides" / "submission" / "problem-subject-lab-verification-report.json"
TIMEOUT_SECONDS = 120
OPENJDK_BIN = Path("/opt/homebrew/opt/openjdk/bin")
OPENJDK_HOME = Path("/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home")


@dataclass
class Lab:
    index: int
    project: str
    section: str
    slug: str
    runtime: str
    problem_doc: Path
    answer_doc: Path
    verify_command: str


def normalize_shell_block(block: str) -> str:
    lines: list[str] = []
    current = ""
    for raw in block.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.endswith("\\"):
            current += line[:-1].rstrip() + " "
            continue
        if current:
            line = current + line
            current = ""
        lines.append(line)
    if current:
        lines.append(current.strip())
    return " && ".join(lines)


def parse_manifest() -> list[Lab]:
    labs: list[Lab] = []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| "):
            continue
        parts = [part.strip().strip("`") for part in line.strip("|").split("|")]
        if len(parts) != 7 or not parts[0].isdigit():
            continue
        index, project, section, slug, runtime, problem_doc, answer_doc = parts
        problem_path = ROOT / problem_doc
        answer_path = ROOT / answer_doc
        text = problem_path.read_text(encoding="utf-8")
        blocks = re.findall(r"```bash\n(.*?)```", text, flags=re.S)
        verify_command = ""
        for block in blocks:
            verify_command = normalize_shell_block(block)
            if verify_command:
                break
        labs.append(
            Lab(
                index=int(index),
                project=project,
                section=section,
                slug=slug,
                runtime=runtime,
                problem_doc=problem_path,
                answer_doc=answer_path,
                verify_command=verify_command,
            )
        )
    return labs


def classify_failure(code: int, output: str) -> str:
    lower = output.lower()
    blocked_patterns = [
        "command not found",
        "no such file or directory",
        "not installed",
        "is required",
        "module not found",
        "modulenotfounderror",
        "cannot find module",
        "uv: command not found",
        "pytest: command not found",
        "npm: command not found",
        "pnpm: command not found",
        "go: command not found",
        "helm: command not found",
        "docker: command not found",
        "kubectl: command not found",
        "permission denied",
        "unable to locate a java runtime",
        "please visit http://www.java.com",
    ]
    if any(pattern in lower for pattern in blocked_patterns):
        return "blocked"
    if code == 124:
        return "timeout"
    return "failed"


def summarize_output(output: str, status: str) -> str:
    if not output:
        return "passed" if status == "passed" else "no output"
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    preferred_patterns = (
        "modulenotfounderror",
        "command not found",
        "unable to locate a java runtime",
        "please visit http://www.java.com",
        "missing go.sum entry",
        "assertionerror",
        "failed",
        "error",
    )
    for line in reversed(lines):
        lower = line.lower()
        if any(pattern in lower for pattern in preferred_patterns):
            return line[:500]
    for line in reversed(lines):
        if not line.lower().startswith("make: ***"):
            return line[:500]
    return lines[-1][:500]


def run_lab(lab: Lab) -> dict[str, object]:
    started_at = time.time()
    if not lab.verify_command:
        return {
            "index": lab.index,
            "project": lab.project,
            "section": lab.section,
            "slug": lab.slug,
            "problem_doc": lab.problem_doc.relative_to(ROOT).as_posix(),
            "answer_doc": lab.answer_doc.relative_to(ROOT).as_posix(),
            "command": "",
            "status": "blocked",
            "duration_sec": 0.0,
            "summary": "검증 명령을 찾지 못했습니다.",
        }
    try:
        env = os.environ.copy()
        path_parts = [part for part in env.get("PATH", "").split(":") if part]
        if OPENJDK_BIN.exists() and str(OPENJDK_BIN) not in path_parts:
            path_parts.insert(0, str(OPENJDK_BIN))
        env["PATH"] = ":".join(path_parts)
        if OPENJDK_HOME.exists():
            env.setdefault("JAVA_HOME", str(OPENJDK_HOME))
        completed = subprocess.run(
            lab.verify_command,
            cwd=ROOT,
            shell=True,
            executable="/bin/zsh",
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            env=env,
        )
        output = "\n".join(part for part in [completed.stdout.strip(), completed.stderr.strip()] if part).strip()
        status = "passed" if completed.returncode == 0 else classify_failure(completed.returncode, output)
        summary = summarize_output(output, status)
        return {
            "index": lab.index,
            "project": lab.project,
            "section": lab.section,
            "slug": lab.slug,
            "problem_doc": lab.problem_doc.relative_to(ROOT).as_posix(),
            "answer_doc": lab.answer_doc.relative_to(ROOT).as_posix(),
            "command": lab.verify_command,
            "status": status,
            "returncode": completed.returncode,
            "duration_sec": round(time.time() - started_at, 2),
            "summary": summary[:500],
        }
    except subprocess.TimeoutExpired as exc:
        output = "\n".join(part for part in [(exc.stdout or "").strip(), (exc.stderr or "").strip()] if part).strip()
        summary = summarize_output(output, "timeout") if output else f"{TIMEOUT_SECONDS}s timeout"
        return {
            "index": lab.index,
            "project": lab.project,
            "section": lab.section,
            "slug": lab.slug,
            "problem_doc": lab.problem_doc.relative_to(ROOT).as_posix(),
            "answer_doc": lab.answer_doc.relative_to(ROOT).as_posix(),
            "command": lab.verify_command,
            "status": "timeout",
            "returncode": 124,
            "duration_sec": round(time.time() - started_at, 2),
            "summary": summary[:500],
        }


def main() -> None:
    labs = parse_manifest()
    total = len(labs)
    results: list[dict[str, object]] = []
    for offset, lab in enumerate(labs, start=1):
        result = run_lab(lab)
        results.append(result)
        REPORT.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{offset} / {total} {lab.problem_doc.relative_to(ROOT)} :: {result['status']} :: {result['summary']}")


if __name__ == "__main__":
    main()

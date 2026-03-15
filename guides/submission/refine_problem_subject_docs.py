from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import os
import re
import unicodedata


ROOT = Path("/Users/woopinbell/work/book-task-3")
MANIFEST = ROOT / "guides" / "problem-subject-lab-manifest.md"
SECTIONS = [
    "problem-subject-essential",
    "problem-subject-elective",
    "problem-subject-capstone",
]
RUNTIMES = [
    "python",
    "go",
    "fastapi",
    "nestjs",
    "spring",
    "react-native",
    "node-server",
    "react",
    "vanilla",
    "c",
    "cpp",
]
IGNORE_DIRS = {
    ".git",
    ".idea",
    ".next",
    ".venv",
    ".mypy_cache",
    ".ruff_cache",
    ".turbo",
    ".gradle",
    ".pytest_cache",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "blog",
    "docs",
    "notion",
    "notion-archive",
    "problem-subject-essential",
    "problem-subject-elective",
    "problem-subject-capstone",
}
CONFIG_NAMES = {
    "Makefile",
    "go.mod",
    "go.sum",
    "package.json",
    "pyproject.toml",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "vite.config.ts",
    "vitest.config.ts",
    "playwright.config.ts",
    "jest.config.ts",
    "jest.setup.ts",
    "drizzle.config.ts",
}
SOURCE_EXTS = {
    ".py",
    ".go",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".java",
    ".kt",
    ".swift",
    ".c",
    ".cc",
    ".cpp",
    ".h",
    ".hpp",
}
EVIDENCE_EXTS = {
    ".pcapng",
    ".json",
    ".yaml",
    ".yml",
    ".csv",
    ".txt",
    ".log",
    ".sh",
}


@dataclass(frozen=True)
class Entry:
    project: str
    section: str
    slug: str
    runtime: str
    problem_doc: Path
    answer_doc: Path


@dataclass
class Candidate:
    path: Path
    name_key: str
    rel_key: str
    tokens: set[str]
    child_dirs: set[str]


def slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    lowered = "".join(ch if ch.isalnum() or ch in "-_/" else " " for ch in normalized).lower()
    lowered = lowered.replace("/", " ")
    return re.sub(r"[-_\s]+", "-", lowered).strip("-")


def token_set(text: str) -> set[str]:
    return {part for part in re.split(r"[-_/]+", slugify(text)) if part}


def clean_text(text: str) -> str:
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"^#+\s*", "", text.strip())
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {"__lead__": []}
    current = "__lead__"
    for line in text.splitlines():
        if re.match(r"^#+\s+", line):
            current = clean_text(re.sub(r"^#+\s*", "", line).strip())
            sections[current] = []
            continue
        sections.setdefault(current, []).append(line)
    return {key: "\n".join(value).strip() for key, value in sections.items()}


def first_nonempty_line(path: Path) -> str:
    if not path.exists():
        return ""
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#") or stripped.lower().startswith("프로비넌스:"):
            continue
        if stripped.startswith("|") and stripped.endswith("|"):
            continue
        if set(stripped) <= {"|", "-", ":", " "}:
            continue
        if stripped:
            return clean_text(stripped)
    return ""


def find_section(sections: dict[str, str], keys: tuple[str, ...]) -> str:
    exact_matches: list[str] = []
    partial_matches: list[str] = []
    normalized_keys = [key.lower() for key in keys]
    for key, value in sections.items():
        if key == "__lead__" or not value:
            continue
        meaningful = trim_sentence(value, "")
        if not meaningful or meaningful.lower().startswith("프로비넌스:"):
            continue
        lowered = key.lower()
        if any(lowered == token for token in normalized_keys):
            exact_matches.append(value.strip())
            continue
        if any(token in lowered for token in normalized_keys):
            partial_matches.append(value.strip())
    if exact_matches:
        return exact_matches[0]
    if partial_matches:
        return partial_matches[0]
    return ""


def bullets_from_text(text: str) -> list[str]:
    items: list[str] = []
    for raw in text.splitlines():
        line = clean_text(raw.strip())
        if not line:
            continue
        if raw.strip().startswith("|"):
            cells = [clean_text(cell) for cell in raw.strip().strip("|").split("|")]
            if not cells:
                continue
            if all(not cell or set(cell) <= {"-", ":"} for cell in cells):
                continue
            if cells[0].lower() in {"항목", "파일", "label"}:
                continue
            if len(cells) >= 2 and cells[0] and cells[1]:
                items.append(f"{cells[0]}: {cells[1]}")
                continue
        if "README.md" in line or "docs/" in line or "notion/" in line or "blog/" in line:
            continue
        line = re.sub(r"^[\-\*\d\.\)\s]+", "", line)
        if line:
            items.append(line)
    return items


def ensure_bullets(items: list[str], fallback: list[str]) -> list[str]:
    out = [clean_text(item) for item in items if clean_text(item)]
    return out or fallback


def relpath(target: Path, start: Path) -> str:
    return os.path.relpath(target, start).replace("\\", "/")


def is_ignored_dir(name: str) -> bool:
    return name in IGNORE_DIRS or name.startswith(".") or name.endswith(".egg-info")


def runtime_suffix(text: str) -> str | None:
    for runtime in sorted(RUNTIMES, key=len, reverse=True):
        if text.endswith(f"-{runtime}"):
            return runtime
    return None


def effective_runtime(entry: Entry) -> str:
    return entry.runtime if entry.runtime != "no-runtime" else (runtime_suffix(entry.problem_doc.stem) or "no-runtime")


def extract_list_items(text: str) -> list[str]:
    items: list[str] = []
    for raw in text.splitlines():
        match = re.match(r"^\s*(?:[-*]|\d+\.)\s+(.*)", raw)
        if not match:
            continue
        item = clean_text(match.group(1))
        if not item:
            continue
        if "README.md" in item or "docs/" in item or "notion/" in item or "blog/" in item:
            continue
        items.append(item)
    return items


def normalize_shell_block(block: str) -> str:
    lines: list[str] = []
    for raw in block.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(line)
    if not lines:
        return ""
    if len(lines) == 1:
        return lines[0]
    return " && ".join(lines)


def readme_verify_commands(problem_readme: Path | None) -> list[str]:
    if not problem_readme or not problem_readme.exists():
        return []
    commands: list[str] = []
    for block in re.findall(r"```(?:bash|sh)?\n(.*?)```", read_text(problem_readme), flags=re.S):
        normalized = normalize_shell_block(block)
        if not normalized:
            continue
        lowered = normalized.lower()
        if any(token in lowered for token in ("make ", "pytest", "python", "go test", "npm ", "pnpm ", "mvn", "./gradlew")):
            commands.append(normalized)
    return unique_items(commands, limit=3)


def extract_referenced_files(text: str, anchor: Path) -> list[Path]:
    refs: list[Path] = []
    for match in re.finditer(r"`([^`]+)`", text):
        token = match.group(1).strip()
        if not token or "://" in token:
            continue
        if token.endswith(".gitkeep"):
            continue
        base_candidates = [anchor, ROOT]
        base_candidates.extend(parent for parent in anchor.parents if parent != ROOT)
        candidates = [(base / token).resolve() for base in base_candidates]
        for candidate in candidates:
            if not candidate.exists() or not candidate.is_file():
                continue
            if candidate.suffix.lower() == ".md":
                continue
            rel = candidate.relative_to(ROOT).as_posix() if ROOT in candidate.parents or candidate == ROOT else candidate.as_posix()
            if any(part in {"docs", "notion", "notion-archive", "blog"} for part in Path(rel).parts):
                continue
            refs.append(candidate)
    deduped: list[Path] = []
    for ref in refs:
        if ref not in deduped:
            deduped.append(ref)
    return deduped


def base_slug(entry: Entry) -> str:
    stem = entry.problem_doc.stem
    runtime = effective_runtime(entry)
    suffix = f"-{runtime}"
    if runtime != "no-runtime" and stem.endswith(suffix):
        return stem[: -len(suffix)]
    if runtime != "no-runtime" and entry.slug.endswith(suffix):
        return entry.slug[: -len(suffix)]
    return stem


def title_for(entry: Entry) -> str:
    stem = entry.problem_doc.stem
    runtime = effective_runtime(entry)
    if runtime != "no-runtime" and not stem.endswith(f"-{runtime}"):
        return f"{stem} ({runtime})"
    return stem


def parse_manifest() -> list[Entry]:
    rows: list[Entry] = []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| "):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if cells[0] in {"n", "---"} or len(cells) != 7:
            continue
        _, project, section, slug, runtime, problem_doc, answer_doc = cells
        rows.append(
            Entry(
                project=project,
                section=section,
                slug=slug,
                runtime=runtime,
                problem_doc=ROOT / problem_doc,
                answer_doc=ROOT / answer_doc,
            )
        )
    deduped: dict[tuple[str, str], Entry] = {}
    for entry in rows:
        key = (str(entry.problem_doc), str(entry.answer_doc))
        current = deduped.get(key)
        if current is None:
            deduped[key] = entry
            continue
        if current.runtime == "no-runtime" and entry.runtime != "no-runtime":
            deduped[key] = entry
    return sorted(
        deduped.values(),
        key=lambda item: (item.project, item.section, item.problem_doc.as_posix()),
    )


def discover_candidates(project_dir: Path) -> list[Candidate]:
    candidates: list[Candidate] = []
    for current, dirs, _files in os.walk(project_dir):
        dirs[:] = [name for name in dirs if not is_ignored_dir(name)]
        path = Path(current)
        if path == project_dir:
            continue
        rel = path.relative_to(project_dir)
        if any(is_ignored_dir(part) for part in rel.parts):
            continue
        child_dirs = set(dirs)
        is_candidate = False
        if "problem" in child_dirs or any(runtime in child_dirs for runtime in RUNTIMES):
            is_candidate = True
        else:
            for child in child_dirs:
                child_path = path / child
                grand = {item.name for item in child_path.iterdir() if item.is_dir() and not is_ignored_dir(item.name)}
                if "problem" in grand or any(runtime in grand for runtime in RUNTIMES):
                    is_candidate = True
                    break
        if is_candidate:
            rel_key = slugify("/".join(rel.parts))
            candidates.append(
                Candidate(
                    path=path,
                    name_key=slugify(path.name),
                    rel_key=rel_key,
                    tokens=token_set(rel_key),
                    child_dirs=child_dirs,
                )
            )
    return candidates


def runtime_available(candidate: Candidate, runtime: str) -> bool:
    if runtime == "no-runtime":
        return True
    if runtime in candidate.child_dirs or runtime in candidate.path.parts:
        return True
    aliases = {
        "fastapi": {".py"},
        "go": {".go"},
        "react": {".tsx", ".ts", ".jsx", ".js"},
        "vanilla": {".ts", ".tsx", ".js"},
        "node-server": {".ts", ".js"},
        "nestjs": {".ts", ".js"},
        "spring": {".java", ".kt"},
        "react-native": {".tsx", ".ts"},
        "python": {".py"},
        "c": {".c", ".h"},
        "cpp": {".cpp", ".cc", ".hpp", ".h"},
    }
    exts = aliases.get(runtime, set())
    if not exts:
        return False
    for current, dirs, files in os.walk(candidate.path):
        dirs[:] = [name for name in dirs if not is_ignored_dir(name)]
        for file_name in files:
            if Path(file_name).suffix in exts:
                return True
    return False


def choose_base_dir(entry: Entry, candidates: list[Candidate]) -> Path:
    target_slug = slugify(base_slug(entry))
    target_tokens = token_set(target_slug)
    target_runtime = effective_runtime(entry)
    best_score = -10**9
    best_path = ROOT / entry.project
    for candidate in candidates:
        score = 0
        common = len(target_tokens & candidate.tokens)
        if candidate.name_key == target_slug:
            score += 400
        if candidate.rel_key.endswith(target_slug):
            score += 250
        if target_tokens and common == len(target_tokens):
            score += 160
        score += common * 25
        if runtime_available(candidate, target_runtime):
            score += 80
        if (candidate.path / "problem" / "README.md").exists():
            score += 20
        score -= max(0, len(candidate.tokens) - len(target_tokens)) * 3
        score -= len(candidate.path.relative_to(ROOT / entry.project).parts)
        if score > best_score:
            best_score = score
            best_path = candidate.path
    runtime = effective_runtime(entry)
    if runtime != "no-runtime" and best_path.name == runtime and (best_path.parent / "problem").exists():
        return best_path.parent
    return best_path


def find_problem_readme(base_dir: Path) -> Path | None:
    direct = base_dir / "problem" / "README.md"
    if direct.exists():
        return direct
    for current, dirs, files in os.walk(base_dir):
        dirs[:] = [name for name in dirs if not is_ignored_dir(name)]
        path = Path(current)
        if path.relative_to(base_dir).parts and len(path.relative_to(base_dir).parts) > 3:
            continue
        if path.name == "problem" and "README.md" in files:
            return path / "README.md"
    return None


def refine_base_dir_from_existing_docs(entry: Entry, fallback: Path) -> Path:
    runtime = effective_runtime(entry)
    current_slug = base_slug(entry)
    if (fallback / "problem" / "README.md").exists():
        if runtime == "no-runtime" and runtime_suffix(entry.problem_doc.stem) is None and fallback.name == current_slug:
            return fallback
        if runtime == "no-runtime" and "stages" in fallback.parts:
            return fallback
    anchors: list[Path] = []
    for doc in (entry.problem_doc, entry.answer_doc):
        if not doc.exists():
            continue
        for ref in extract_referenced_files(read_text(doc), doc.parent):
            anchor = first_ancestor_with(ref.parent, ("problem/README.md",))
            if not anchor or anchor == fallback:
                continue
            if runtime != "no-runtime":
                runtime_dir = anchor / runtime
                if runtime_dir.exists():
                    anchors.append(anchor)
                    continue
                if runtime in ref.parts:
                    anchors.append(anchor)
                    continue
            else:
                anchors.append(anchor)
    if not anchors:
        return fallback
    scored = sorted(
        ((anchors.count(anchor), len(anchor.relative_to(ROOT / entry.project).parts), anchor) for anchor in set(anchors)),
        key=lambda item: (-item[0], -item[1], item[2].as_posix()),
    )
    return scored[0][2]


def file_priority(path: Path, runtime: str) -> tuple[int, str]:
    text = path.as_posix().lower()
    name = path.name.lower()
    if "/src/" in text or "/app/" in text or "/internal/" in text or "/cmd/" in text or "/components/" in text:
        return (0, text)
    if "/problem/code/" in text:
        return (1, text)
    if "/tests/" in text or "/__tests__/" in text or name.startswith("test_") or ".test." in name:
        return (2, text)
    if name in {item.lower() for item in CONFIG_NAMES}:
        return (3, text)
    if runtime != "no-runtime" and any(text.endswith(ext) for ext in SOURCE_EXTS):
        return (4, text)
    return (5, text)


def runtime_root(base_dir: Path, runtime: str) -> Path:
    if runtime == "no-runtime":
        return base_dir
    direct = base_dir / runtime
    if direct.exists():
        return direct
    if runtime in base_dir.parts:
        return base_dir
    for current, dirs, _files in os.walk(base_dir):
        dirs[:] = [name for name in dirs if not is_ignored_dir(name)]
        path = Path(current)
        if path.name == runtime:
            return path
    return base_dir


def is_test_file(path: Path) -> bool:
    lower = path.as_posix().lower()
    name = path.name
    return "/tests/" in lower or "/__tests__/" in lower or name.startswith("test_") or ".test." in name or name.endswith("_test.go")


def gather_files(base_dir: Path, runtime: str, problem_readme: Path | None) -> tuple[list[Path], list[Path], list[Path], list[Path], list[Path]]:
    root = runtime_root(base_dir, runtime)
    problem_root = problem_readme.parent if problem_readme and problem_readme.parent.name == "problem" else base_dir / "problem"
    source_files: list[Path] = []
    starter_files: list[Path] = []
    test_files: list[Path] = []
    config_files: list[Path] = []
    evidence_files: list[Path] = []

    for current, dirs, files in os.walk(root):
        dirs[:] = [name for name in dirs if not is_ignored_dir(name)]
        path = Path(current)
        rel_parts = path.relative_to(root).parts
        if len(rel_parts) > 5:
            dirs[:] = []
        for file_name in files:
            file_path = path / file_name
            if file_name == ".gitkeep":
                continue
            if "test-results" in file_path.parts or file_name == ".last-run.json":
                continue
            suffix = file_path.suffix.lower()
            lower = file_path.as_posix().lower()
            if suffix == ".md":
                continue
            if file_name in CONFIG_NAMES:
                config_files.append(file_path)
                continue
            if suffix == ".sh":
                evidence_files.append(file_path)
                continue
            if is_test_file(file_path):
                if suffix in SOURCE_EXTS or file_name in CONFIG_NAMES:
                    test_files.append(file_path)
                continue
            if suffix in SOURCE_EXTS:
                source_files.append(file_path)
            elif suffix in EVIDENCE_EXTS:
                evidence_files.append(file_path)

    problem_code = problem_root / "code"
    if problem_code.exists():
        for child in sorted(problem_code.rglob("*")):
            if child.is_file() and child.suffix.lower() in SOURCE_EXTS:
                starter_files.append(child)
    if (problem_root / "Makefile").exists():
        config_files.append(problem_root / "Makefile")
    if (problem_root / "script").exists():
        for child in sorted((problem_root / "script").rglob("*")):
            if child.is_file() and child.suffix.lower() != ".md" and child.name != ".gitkeep":
                evidence_files.append(child)
    if (problem_root / "data").exists():
        for child in sorted((problem_root / "data").rglob("*")):
            if child.is_file() and child.suffix.lower() != ".md" and child.name != ".gitkeep":
                evidence_files.append(child)

    if runtime == "no-runtime" and not source_files:
        for current, dirs, files in os.walk(base_dir):
            dirs[:] = [name for name in dirs if not is_ignored_dir(name)]
            path = Path(current)
            for file_name in files:
                file_path = path / file_name
                if file_name == ".gitkeep":
                    continue
                if "test-results" in file_path.parts or file_name == ".last-run.json":
                    continue
                suffix = file_path.suffix.lower()
                if suffix == ".md":
                    continue
                if file_name in CONFIG_NAMES:
                    config_files.append(file_path)
                elif suffix == ".sh":
                    evidence_files.append(file_path)
                elif "/tests/" in file_path.as_posix().lower() or file_name.startswith("test_") or ".test." in file_name or file_name.endswith("_test.go"):
                    if suffix in SOURCE_EXTS:
                        test_files.append(file_path)
                elif suffix in SOURCE_EXTS:
                    source_files.append(file_path)
                elif suffix in EVIDENCE_EXTS:
                    evidence_files.append(file_path)

    if problem_readme:
        for ref in extract_referenced_files(read_text(problem_readme), problem_readme.parent):
            if ref.name in CONFIG_NAMES:
                config_files.append(ref)
            elif is_test_file(ref):
                test_files.append(ref)
            elif ref.suffix.lower() in SOURCE_EXTS:
                source_files.append(ref)
            else:
                evidence_files.append(ref)

    if runtime == "no-runtime":
        package_roots: list[Path] = []
        for source in source_files:
            package_root = first_ancestor_with(source.parent, ("package.json",))
            if package_root and package_root not in package_roots:
                package_roots.append(package_root)
        for package_root in package_roots:
            package_json = package_root / "package.json"
            if package_json.exists():
                config_files.append(package_json)
            tests_root = package_root / "tests"
            if tests_root.exists():
                for child in sorted(tests_root.rglob("*")):
                    if child.is_file() and is_test_file(child):
                        test_files.append(child)

    source_files = sorted(dict.fromkeys(source_files), key=lambda path: file_priority(path, runtime))
    starter_files = sorted(dict.fromkeys(starter_files), key=lambda path: file_priority(path, runtime))
    test_files = sorted(dict.fromkeys(test_files), key=lambda path: file_priority(path, runtime))
    config_files = sorted(dict.fromkeys(config_files), key=lambda path: file_priority(path, runtime))
    evidence_files = sorted(dict.fromkeys(evidence_files), key=lambda path: file_priority(path, runtime))
    return source_files, starter_files, test_files, config_files, evidence_files


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def extract_answer_source_refs(answer_doc: Path) -> list[str]:
    if not answer_doc.exists():
        return []
    sections = parse_sections(read_text(answer_doc))
    source_section = find_section(sections, ("소스 근거",))
    refs: list[str] = []
    for match in re.finditer(r"`([^`]+)`", source_section):
        token = match.group(1).strip()
        if not token or token.endswith(".md"):
            continue
        if any(part in token for part in ("docs/", "notion/", "blog/")):
            continue
        if "/" not in token and "." not in token:
            continue
        refs.append(token)
    return unique_items(refs, limit=4)


def extract_symbols(path: Path) -> list[str]:
    text = read_text(path)
    suffix = path.suffix.lower()
    symbols: list[str] = []
    if suffix == ".py":
        symbols = re.findall(r"^(?:async\s+def|def|class)\s+([A-Za-z_]\w*)", text, flags=re.M)
    elif suffix == ".go":
        symbols = re.findall(r"^func\s+(?:\([^)]+\)\s*)?([A-Za-z_]\w*)", text, flags=re.M)
    elif suffix in {".ts", ".tsx", ".js", ".jsx"}:
        symbols = re.findall(
            r"^(?:export\s+)?(?:async\s+function|function|class|const|let)\s+([A-Za-z_]\w*)",
            text,
            flags=re.M,
        )
        symbols.extend(re.findall(r'(?:describe|it|test)\("([^"]+)"', text))
        symbols.extend(re.findall(r"(?:describe|it|test)\('([^']+)'", text))
    elif suffix in {".c", ".cc", ".cpp", ".h", ".hpp"}:
        symbols = re.findall(
            r"^[A-Za-z_][\w\s\*]*\s+([A-Za-z_]\w*)\s*\([^;]*\)\s*\{?",
            text,
            flags=re.M,
        )
    elif suffix in {".java", ".kt", ".swift"}:
        symbols = re.findall(r"^(?:fun|func|class|interface|data class|public class)\s+([A-Za-z_]\w*)", text, flags=re.M)
    cleaned: list[str] = []
    for symbol in symbols:
        stripped = clean_text(symbol)
        if stripped and stripped not in cleaned:
            cleaned.append(stripped)
    return cleaned[:6]


def describe_file(path: Path, symbols: list[str]) -> str:
    lower = path.as_posix().lower()
    name = path.name
    if name in CONFIG_NAMES:
        return "실행 명령과 검증 경로를 고정하는 설정 파일이다."
    if name == "__init__.py":
        if "/routes/" in lower or "/api/" in lower:
            return "패키지 공개 경계와 route wiring 순서를 고정하는 진입 파일이다."
        return "패키지 진입점과 공개 API 경계를 고정하는 파일이다."
    if name == "__main__.py":
        return "CLI나 demo 실행 순서를 묶는 진입점 파일이다."
    if name == "conftest.py":
        return "pytest fixture와 테스트 환경 구성을 고정하는 파일이다."
    if name in {"setup.ts", "setup.js"}:
        return "DOM/브라우저 테스트 환경 shim과 전역 hook을 고정하는 파일이다."
    if lower.endswith("/app/layout.tsx"):
        return "앱 레이아웃과 메타데이터 경계를 고정하는 파일이다."
    if lower.endswith("/app/page.tsx") or lower.endswith("/case-study/page.tsx"):
        return "화면 진입점에서 최상위 composition과 초기 시연 흐름을 고정하는 파일이다."
    if name in {"router.py", "router.ts"}:
        return "endpoint와 route 조합을 묶어 외부 진입 경로를 고정하는 파일이다."
    if path.suffix.lower() == ".sh":
        return "검증 절차나 보조 자동화를 담아 결과를 재현하는 스크립트다."
    if path.suffix.lower() == ".pcapng":
        return "packet/frame 수준 근거를 직접 확인하는 trace 파일이다."
    if path.suffix.lower() in {".json", ".yaml", ".yml", ".csv", ".txt", ".log"}:
        return "입력 fixture나 계약 데이터를 고정하는 근거 파일이다."
    if "/tests/" in lower or "/__tests__/" in lower or name.startswith("test_") or ".test." in name or name.endswith("_test.go"):
        if symbols:
            joined = ", ".join(f"`{symbol}`" for symbol in symbols[:3])
            return f"{joined}가 통과 조건과 회귀 포인트를 잠근다."
        return "통과 조건과 회귀 포인트를 잠그는 테스트 파일이다."
    if symbols:
        joined = ", ".join(f"`{symbol}`" for symbol in symbols[:4])
        return f"{joined}가 핵심 흐름과 상태 전이를 묶는다."
    if "/problem/code/" in lower:
        return "starter skeleton으로 입력 계약과 확장 포인트를 보여 준다."
    return "핵심 구현을 담는 파일이다."


def sentence_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def unique_items[T](items: list[T], limit: int | None = None) -> list[T]:
    deduped: list[T] = []
    for item in items:
        if item not in deduped:
            deduped.append(item)
    return deduped[:limit] if limit is not None else deduped


def symbol_phrase(symbols: list[str], limit: int = 2) -> str:
    picked = [f"`{symbol}`" for symbol in symbols[:limit] if symbol]
    if not picked:
        return ""
    if len(picked) == 1:
        return picked[0]
    return "와 ".join(picked)


def trim_sentence(text: str, fallback: str) -> str:
    cleaned = clean_text(text)
    return cleaned or fallback


def looks_complete_statement(text: str) -> bool:
    stripped = clean_text(text).rstrip(".")
    if not stripped:
        return False
    endings = (
        "다",
        "한다",
        "된다",
        "있다",
        "없다",
        "이다",
        "했다",
        "해야 한다",
        "가능하다",
        "분명해진다",
        "유지된다",
        "노출된다",
        "공유한다",
        "설명할 수 있다",
    )
    return any(stripped.endswith(ending) for ending in endings)


def object_particle(text: str) -> str:
    stripped = clean_text(text).rstrip(".").strip()
    if not stripped:
        return "를"
    last = stripped[-1]
    if "가" <= last <= "힣":
        return "을" if (ord(last) - 0xAC00) % 28 else "를"
    return "를"


def compose_goal_from_requirements(requirements: list[str], fallback: str) -> str:
    focus = [clean_text(item).rstrip(".") for item in requirements if clean_text(item)]
    if not focus:
        return fallback
    if len(focus) == 1:
        item = focus[0]
        return f"시작 위치의 구현을 완성해 {item}{object_particle(item)} 코드와 검증으로 재현한다."
    if len(focus) == 2:
        joined = f"{focus[0]}와 {focus[1]}"
    else:
        joined = f"{focus[0]}, {focus[1]}, {focus[2]}"
    return f"시작 위치의 구현을 완성해 {joined}{object_particle(joined)} 한 흐름으로 설명하고 검증한다."


def summary_from_text(text: str, fallback: str) -> str:
    items = [item for item in bullets_from_text(text) if not item.lower().startswith("프로비넌스:")]
    if items:
        return " ".join(items[:4])
    cleaned = trim_sentence(text, fallback)
    if cleaned.lower().startswith("프로비넌스:") or cleaned == "항목 내용":
        return fallback
    return cleaned


def collect_problem_material(entry: Entry, base_dir: Path) -> tuple[str, list[str], list[str], list[str]]:
    readme = find_problem_readme(base_dir)
    sections = parse_sections(read_text(readme)) if readme else {}
    readme_text = read_text(readme) if readme else ""
    question_items = extract_list_items(find_section(sections, ("풀어야", "질문")) or readme_text)
    problem_section = find_section(sections, ("문제",))
    constraints_section = find_section(sections, ("제약",))
    include_section = find_section(sections, ("포함 범위",))
    deliverables_section = find_section(sections, ("요구 산출물", "기대 산출물"))
    why = summary_from_text(
        find_section(sections, ("왜", "가르치는 것", "역할", "문제 해석")) or problem_section or first_nonempty_line(base_dir / "README.md"),
        f"{title_for(entry)}는 어떤 경계를 구현하고 어디까지 검증해야 하는지 빠르게 잡아야 의미가 살아나는 lab이다.",
    )
    goal_text = summary_from_text(
        find_section(sections, ("목표", "완료 기준", "가르치는 것", "역할", "문제 해석", "원래 과제가 묻는 것"))
        or problem_section
        or deliverables_section
        or first_nonempty_line(readme) if readme else ""
        or sections.get("__lead__", ""),
        f"{title_for(entry)}를 시작 위치의 source와 test만으로 구현하거나 재구성한다.",
    )
    requirements = ensure_bullets(
        bullets_from_text(
            find_section(sections, ("성공 기준", "핵심 요구사항", "문제 계약", "완료 기준"))
            or "\n".join(part for part in (constraints_section, include_section, deliverables_section) if part)
        )
        or question_items[:4],
        [
            f"{title_for(entry)}의 핵심 동작을 source와 test가 같은 방향으로 설명해야 한다.",
            "starter code와 검증 경로를 같은 문서에서 바로 찾을 수 있어야 한다.",
        ],
    )
    if clean_text(goal_text) == clean_text(why):
        goal_text = compose_goal_from_requirements(
            requirements,
            f"{title_for(entry)}의 시작 위치 구현과 검증 경로를 실제로 닫는다.",
        )
    elif not looks_complete_statement(goal_text):
        goal_text = compose_goal_from_requirements(requirements, goal_text)
    excludes = ensure_bullets(
        bullets_from_text(find_section(sections, ("제외 범위", "범위 메모", "범위 밖"))),
        [
            "docs, notion, blog 같은 보조 문서는 이 문제지의 출발점으로 쓰지 않는다.",
            "다른 runtime 구현 세부사항을 함께 설명하지 않는다.",
        ],
    )
    return why, goal_text, requirements, excludes


def common_parent(paths: list[Path]) -> Path | None:
    if not paths:
        return None
    common = Path(os.path.commonpath([str(path) for path in paths]))
    return common


def contextual_excludes(
    entry: Entry,
    runtime: str,
    starter_files: list[Path],
    evidence_files: list[Path],
    config_files: list[Path],
    existing: list[str],
) -> list[str]:
    items = [clean_text(item) for item in existing if clean_text(item)]
    out = [
        item
        for item in items
        if "docs, notion, blog 같은 보조 문서는 이 문제지의 출발점으로 쓰지 않는다." not in item
        and "다른 runtime 구현 세부사항을 함께 설명하지 않는다." not in item
    ]
    if starter_files:
        out.append(f"`{relpath(starter_files[0], entry.problem_doc.parent)}` starter skeleton을 정답 구현으로 착각하지 않는다.")
    if evidence_files:
        out.append(
            f"`{relpath(evidence_files[0], entry.problem_doc.parent)}`{' 등' if len(evidence_files) > 1 else ''} fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다."
        )
    if runtime != "no-runtime":
        out.append("같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.")
    else:
        out.append("상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.")
    if any(path.name == "Makefile" for path in config_files):
        out.append("검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.")
    return unique_items(out, limit=3)


def actionable_checklist(
    entry: Entry,
    starter_files: list[Path],
    evidence_files: list[Path],
    verify_commands: list[str],
    source_clues: list[str],
    test_clues: list[str],
    requirements: list[str],
) -> list[str]:
    items: list[str] = []
    if starter_files:
        items.append(f"`{relpath(starter_files[0], entry.problem_doc.parent)}`의 빈 확장 지점을 실제 구현으로 채웠다.")
    if source_clues:
        focus = symbol_phrase(source_clues)
        items.append(f"핵심 흐름은 {focus}가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.")
    if test_clues:
        locked = symbol_phrase(test_clues)
        items.append(f"검증 기준은 {locked}가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.")
    if evidence_files:
        items.append(
            f"`{relpath(evidence_files[0], entry.problem_doc.parent)}`{' 등' if len(evidence_files) > 1 else ''} fixture/trace 기준으로 결과를 대조했다."
        )
    if verify_commands:
        items.append(f"`{verify_commands[0]}`가 통과한다.")
    if not items:
        items.extend(requirements[:2])
    return unique_items(items, limit=5)


def first_ancestor_with(path: Path, names: tuple[str, ...]) -> Path | None:
    for current in (path,) + tuple(path.parents):
        for name in names:
            if (current / name).exists():
                return current
    return None


def infer_verify(
    entry: Entry,
    base_dir: Path,
    runtime: str,
    config_files: list[Path],
    evidence_files: list[Path],
    problem_readme: Path | None,
    source_files: list[Path],
    test_files: list[Path],
) -> list[str]:
    commands: list[str] = []
    root = runtime_root(base_dir, runtime)
    lab_root = root.parent if runtime != "no-runtime" and (root.parent / "problem").exists() else base_dir
    ancestor_make = first_ancestor_with(lab_root, ("Makefile",))
    commands.extend(readme_verify_commands(problem_readme))
    js_runtimes = {"react", "react-native", "node-server", "nestjs", "vanilla", "fastapi"}
    ordered_configs = config_files[:]
    if runtime in {"react", "react-native", "node-server", "nestjs", "vanilla"}:
        ordered_configs.sort(key=lambda path: (0 if path.name == "package.json" else 1, path.as_posix()))
    elif runtime in {"spring"}:
        ordered_configs.sort(key=lambda path: (0 if path.name in {"build.gradle", "build.gradle.kts", "pom.xml"} else 1, path.as_posix()))
    if runtime == "python":
        if (lab_root / "problem" / "Makefile").exists() and not (root / "tests").exists():
            commands.append(f"make -C {lab_root / 'problem'} test")
        elif (root / "src").exists() and (root / "tests").exists():
            makefile = ancestor_make / "Makefile" if ancestor_make else None
            make_text = read_text(makefile) if makefile and makefile.exists() else ""
            if makefile and "venv:" in make_text and ".venv/bin/python" in make_text:
                src_rel = relpath(root / "src", ancestor_make)
                tests_rel = relpath(root / "tests", ancestor_make)
                commands.append(
                    f"cd {ancestor_make} && make venv && PYTHONPATH={src_rel} .venv/bin/python -m pytest {tests_rel}"
                )
            else:
                commands.append(f"cd {root} && PYTHONPATH=src python3 -m pytest")
    if runtime == "fastapi" and (root / "app").exists() and (root / "tests").exists():
        commands.append(f"cd {root} && PYTHONPATH=. python3 -m pytest")
    for config in ordered_configs:
        name = config.name
        if name == "Makefile":
            text = read_text(config)
            targets = set(re.findall(r"^([A-Za-z0-9_.-]+):", text, flags=re.M))
            for candidate in ("test", "test-unit", "test-capstone", "verify", "smoke", "helm-lint", "helm-template", "lint", "check"):
                if candidate in targets:
                    commands.append(f"make -C {config.parent} {candidate}")
                    break
            else:
                if "all" in targets:
                    commands.append(f"make -C {config.parent}")
        elif name == "package.json":
            try:
                data = json.loads(read_text(config))
            except json.JSONDecodeError:
                data = {}
            scripts = data.get("scripts", {})
            test_script = clean_text(str(scripts.get("test", "")))
            target_test_names = [
                test_path.name
                for test_path in test_files
                if test_path.parent == config.parent / "tests"
                and test_path.name
                in {
                    "manifest-validation.test.ts",
                    "recommendation-service.test.ts",
                    "rerank-service.test.ts",
                    "compatibility-service.test.ts",
                    "release-gate-service.test.ts",
                }
            ]
            for candidate in ("test", "test:unit", "test:e2e", "verify"):
                if candidate in scripts:
                    if candidate == "test" and target_test_names:
                        joined = " ".join(f"tests/{name}" for name in target_test_names)
                        commands.append(f"cd {config.parent} && npm test -- {joined}")
                    elif candidate == "test" and test_script.startswith("vitest") and "--run" not in test_script:
                        commands.append(f"cd {config.parent} && npm run test -- --run")
                    else:
                        commands.append(f"cd {config.parent} && npm run {candidate}")
            if not scripts and (config.parent / "vitest.config.ts").exists():
                commands.append(f"cd {config.parent} && npm test")
        elif name == "pyproject.toml":
            tests_dir = config.parent / "tests"
            if tests_dir.exists():
                if (config.parent / "src").exists():
                    commands.append(f"cd {config.parent} && PYTHONPATH=src python3 -m pytest")
                else:
                    commands.append(f"cd {config.parent} && python3 -m pytest")
        elif name == "pom.xml":
            commands.append(f"cd {config.parent} && mvn test")
        elif name in {"build.gradle", "build.gradle.kts"}:
            gradlew_dir = first_ancestor_with(config.parent, ("gradlew",))
            anchor = gradlew_dir or config.parent
            commands.append(f"cd {anchor} && ./gradlew test")
    for evidence in evidence_files:
        if evidence.name.startswith("verify") and evidence.suffix.lower() == ".sh":
            commands.append(f"bash {evidence}")
    if not commands and runtime == "go":
        commands.append(f"cd {runtime_root(base_dir, runtime)} && GOWORK=off go test ./...")
    if not commands and runtime == "python":
        if (root / "src").exists():
            commands.append(f"cd {root} && PYTHONPATH=src python3 -m pytest")
        else:
            commands.append(f"cd {root} && python3 -m pytest")
    if not commands:
        refs = source_files + test_files + evidence_files
        suffixes = {path.suffix.lower() for path in refs}
        if ".go" in suffixes:
            anchor = common_parent(refs) or base_dir
            commands.append(f"cd {anchor} && GOWORK=off go test ./...")
        elif ".py" in suffixes:
            pyproject_dir = next(
                (first_ancestor_with(path.parent, ("pyproject.toml",)) for path in refs if path.suffix.lower() == ".py"),
                None,
            )
            anchor = pyproject_dir or common_parent(refs) or base_dir
            if (anchor / "src").exists():
                commands.append(f"cd {anchor} && PYTHONPATH=src python3 -m pytest")
            else:
                commands.append(f"cd {anchor} && python3 -m pytest")
        elif {".ts", ".tsx", ".js", ".jsx"} & suffixes:
            package_dir = next(
                (first_ancestor_with(path.parent, ("package.json",)) for path in refs if path.suffix.lower() in {".ts", ".tsx", ".js", ".jsx"}),
                None,
            )
            if package_dir:
                commands.append(f"cd {package_dir} && npm test")
        elif {".c", ".cc", ".cpp", ".h", ".hpp"} & suffixes:
            make_dir = next((first_ancestor_with(path.parent, ("Makefile",)) for path in refs), None)
            if make_dir:
                commands.append(f"make -C {make_dir}")
    if not commands and problem_readme:
        commands.extend(readme_verify_commands(problem_readme))
    deduped: list[str] = []
    for command in commands:
        cleaned = command.strip()
        if cleaned and cleaned not in deduped:
            deduped.append(cleaned)
    return deduped[:3]


def infer_verify_notes(verify_commands: list[str], config_files: list[Path], base_dir: Path, runtime: str) -> list[str]:
    notes: list[str] = []
    joined = "\n".join(verify_commands)
    config_names = {path.name for path in config_files}
    lower = joined.lower()
    if "pytest" in lower or "pyproject.toml" in config_names:
        notes.append("이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.")
    if "npm test" in lower or "npm run" in lower or "package.json" in config_names:
        notes.append("Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.")
    if "./gradlew" in lower or "mvn test" in lower or "pom.xml" in config_names or "build.gradle" in config_names or "build.gradle.kts" in config_names:
        notes.append("Spring/Java 계열 검증은 `JDK/JRE`가 현재 머신에 설치돼 있어야 한다.")
    if "go test" in lower or runtime == "go":
        notes.append("Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.")
    if "helm" in lower:
        notes.append("Helm 검증은 현재 셸에 `helm` CLI가 설치돼 있어야 한다.")
    if "kubectl" in lower:
        notes.append("Kubernetes 관련 검증은 현재 셸에 `kubectl` CLI가 설치돼 있어야 한다.")
    if "make -c" in lower and not notes:
        notes.append(f"`{base_dir.name}`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.")
    return notes or ["검증 명령을 실행하기 전에 필요한 toolchain이 현재 셸에 준비돼 있는지 먼저 확인한다."]


def first_verify_from_problem_doc(problem_doc: Path) -> str:
    commands = readme_verify_commands(problem_doc)
    if commands:
        return commands[0]
    text = problem_doc.read_text(encoding="utf-8")
    blocks = re.findall(r"```bash\n(.*?)```", text, flags=re.S)
    for block in blocks:
        normalized = normalize_shell_block(block)
        if normalized:
            return normalized
    return ""


def problem_doc_text(
    entry: Entry,
    why: str,
    goal_text: str,
    start_refs: list[str],
    starter_bullets: list[str],
    requirements: list[str],
    excludes: list[str],
    checklist: list[str],
    verify_commands: list[str],
    verify_notes: list[str],
) -> str:
    verify_block = "\n\n".join(f"```bash\n{command}\n```" for command in verify_commands)
    title = title_for(entry)
    return (
        f"# {title} 문제지\n\n"
        f"## 왜 중요한가\n\n{why}\n\n"
        f"## 목표\n\n{goal_text}\n\n"
        f"## 시작 위치\n\n{sentence_list(start_refs)}\n\n"
        f"## starter code / 입력 계약\n\n{sentence_list(starter_bullets)}\n\n"
        f"## 핵심 요구사항\n\n{sentence_list(requirements)}\n\n"
        f"## 제외 범위\n\n{sentence_list(excludes)}\n\n"
        f"## 성공 체크리스트\n\n{sentence_list(checklist)}\n\n"
        f"## 검증 방법\n\n{verify_block}\n\n{sentence_list(verify_notes)}\n\n"
        f"## 스포일러 경계\n\n"
        f"정답 코드, 공식 구현 진입점, 해설은 [`{entry.answer_doc.name}`]({entry.answer_doc.name})에서 확인한다.\n"
    )


def answer_doc_text(
    entry: Entry,
    one_line: str,
    strategy_bullets: list[str],
    walkthrough: list[str],
    reconstruct_steps: list[str],
    verify_commands: list[str],
    failure_points: list[str],
    source_refs: list[str],
) -> str:
    verify_block = "\n\n".join(f"```bash\n{command}\n```" for command in verify_commands)
    title = title_for(entry)
    return (
        f"# {title} 답안지\n\n"
        "이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.\n\n"
        f"## 한 줄 해답\n\n{one_line}\n\n"
        f"## 문제를 푸는 핵심 전략\n\n{sentence_list(strategy_bullets)}\n\n"
        f"## 코드 워크스루\n\n{sentence_list(walkthrough)}\n\n"
        f"## 정답을 재구성하는 절차\n\n"
        + "\n".join(f"{index}. {step}" for index, step in enumerate(reconstruct_steps, start=1))
        + "\n\n"
        f"## 검증과 실패 포인트\n\n{verify_block}\n\n{sentence_list(failure_points)}\n\n"
        f"## 소스 근거\n\n{sentence_list(source_refs)}\n"
    )


def answer_doc_text_no_code(
    entry: Entry,
    one_line: str,
    goal_structure: list[str],
    solve_steps: list[str],
    failure_points: list[str],
    verify_commands: list[str],
    why_correct: list[str],
    source_refs: list[str],
) -> str:
    verify_block = "\n\n".join(f"```bash\n{command}\n```" for command in verify_commands)
    title = title_for(entry)
    return (
        f"# {title} 답안지\n\n"
        "이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 source, trace, fixture, 검증 스크립트만 기준으로 정리한 답안지다.\n\n"
        f"## 한 줄 해답\n\n{one_line}\n\n"
        f"## 이 문제의 목표 구조\n\n{sentence_list(goal_structure)}\n\n"
        f"## 단계별 풀이\n\n"
        + "\n".join(f"{index}. {step}" for index, step in enumerate(solve_steps, start=1))
        + "\n\n"
        f"## 흔한 오답과 보완\n\n{sentence_list(failure_points)}\n\n"
        f"## 검증 기준\n\n{verify_block}\n\n"
        f"## 왜 이것이 정답인가\n\n{sentence_list(why_correct)}\n\n"
        f"## 소스 근거\n\n{sentence_list(source_refs)}\n"
    )


def umbrella_problem_text(entry: Entry, children: list[tuple[str, str, str]], verify_command: str) -> str:
    title = title_for(entry)
    runtime_lines = "\n".join(
        f"- `{runtime}`: [`{label}`]({problem_name})" for runtime, label, problem_name in children
    )
    verify_block = f"```bash\n{verify_command}\n```" if verify_command else "```bash\n# 아래 runtime leaf 문제지의 검증 명령을 사용한다.\n```"
    return (
        f"# {title} 문제지\n\n"
        "## 왜 중요한가\n\n이 문서는 runtime이 분리된 구현을 한 장에서 섞어 읽지 않도록 경계를 세우는 umbrella 문제지다.\n\n"
        "## 목표\n\n하나의 개념을 여러 runtime으로 옮긴 구현 중 어떤 문서를 먼저 읽어야 할지 바로 결정한다.\n\n"
        "## 시작 위치\n\n"
        f"{runtime_lines}\n"
        "- runtime leaf 문제지에서 실제 source, test, fixture를 다시 확인한다.\n\n"
        "## starter code / 입력 계약\n\n"
        "- 실제 starter code와 입력 계약은 각 runtime 문제지에서 직접 확인한다.\n\n"
        "## 핵심 요구사항\n\n"
        "- 필요한 runtime을 하나 고른 뒤 그 문서만 기준으로 구현을 시작한다.\n"
        "- runtime 사이 구현을 섞어 읽지 않는다.\n\n"
        "## 제외 범위\n\n"
        "- 이 umbrella 문서는 구현 해설을 대신하지 않는다.\n"
        "- 검증 명령은 runtime leaf 문서에서 사용한다.\n\n"
        "## 성공 체크리스트\n\n"
        "- 어떤 runtime 문서를 읽어야 하는지 즉시 결정할 수 있다.\n"
        "- 선택한 runtime 문서만으로 구현을 시작할 수 있다.\n\n"
        f"## 검증 방법\n\n{verify_block}\n\n"
        "- umbrella 문서는 첫 번째 runtime leaf의 검증 명령을 대표값으로 보여 준다.\n"
        "- 실제 구현 검증은 선택한 runtime leaf 문제지에서 다시 확인한다.\n\n"
        f"## 스포일러 경계\n\n정답 코드, 공식 구현 진입점, 해설은 [`{entry.answer_doc.name}`]({entry.answer_doc.name})에서 확인한다.\n"
    )


def umbrella_answer_text(entry: Entry, children: list[tuple[str, str, str, list[str]]]) -> str:
    title = title_for(entry)
    runtime_lines = "\n".join(
        f"- `{runtime}`: [`{label}`]({answer_name})" for runtime, label, answer_name, _source_refs in children
    )
    source_lines: list[str] = []
    for runtime, label, answer_name, source_refs in children:
        source_lines.append(f"`{runtime}` 해설 진입점: [`{label}`]({answer_name})")
        if source_refs:
            source_lines.append(
                f"`{runtime}` 실제 source/test 근거: {', '.join(f'`{ref}`' for ref in source_refs[:4])}"
            )
    return (
        f"# {title} 답안지\n\n"
        "이 문서는 umbrella 답안지다. 실제 해답은 runtime별 답안지로 분리했고, 여기서는 어떤 runtime 답안지를 읽어야 막히지 않는지만 정리한다.\n\n"
        "## 이 umbrella의 역할\n\n"
        "- 같은 개념을 여러 runtime 구현으로 섞어 읽지 않게 진입 순서를 고정한다.\n"
        "- 실제 코드 워크스루, 검증 명령, 실패 포인트는 아래 runtime 답안지에서 직접 확인한다.\n\n"
        "## 문제를 푸는 핵심 전략\n\n"
        "- 지금 구현하려는 runtime 하나만 선택한다.\n"
        "- 선택한 runtime의 문제지로 입력 계약을 고정한 뒤 같은 이름의 `_answer.md`로 내려간다.\n"
        "- 여러 runtime을 동시에 참고하지 않고 하나를 끝까지 닫은 뒤 필요하면 다른 runtime을 비교한다.\n\n"
        "## 정답을 재구성하는 절차\n\n"
        "1. 아래 runtime 답안지 중 현재 구현할 대상 하나를 고른다.\n"
        "2. 해당 runtime 답안지의 코드 워크스루와 검증 명령만 따라가며 해답을 재구성한다.\n"
        "3. 다른 runtime이 필요해질 때만 비교용으로 다시 올라온다.\n\n"
        f"## 런타임별 답안지\n\n{runtime_lines}\n\n"
        "## 읽는 순서\n\n"
        "- 지금 구현하려는 runtime 하나만 고른다.\n"
        "- 고른 runtime의 문제지에서 입력 계약을 확인한 뒤, 같은 이름의 `_answer.md`로 바로 내려간다.\n"
        "\n## 소스 근거\n\n"
        f"{sentence_list(source_lines or [runtime_lines])}\n"
    )


def build_docs(entry: Entry, candidates: list[Candidate]) -> tuple[str, str, str, str]:
    base_dir = choose_base_dir(entry, candidates)
    base_dir = refine_base_dir_from_existing_docs(entry, base_dir)
    problem_readme = find_problem_readme(base_dir)
    why, goal_text, requirements, excludes = collect_problem_material(entry, base_dir)
    target_runtime = effective_runtime(entry)
    source_files, starter_files, test_files, config_files, evidence_files = gather_files(base_dir, target_runtime, problem_readme)

    if target_runtime == "no-runtime":
        siblings: list[tuple[str, str, str, str, list[str]]] = []
        stem = entry.problem_doc.stem
        for runtime in RUNTIMES:
            problem_name = f"{stem}-{runtime}.md"
            answer_name = f"{stem}-{runtime}_answer.md"
            problem_path = entry.problem_doc.with_name(problem_name)
            answer_path = entry.answer_doc.with_name(answer_name)
            if problem_path.exists() and answer_path.exists():
                siblings.append(
                    (
                        runtime,
                        problem_path.stem,
                        problem_path.name,
                        answer_path.name,
                        extract_answer_source_refs(answer_path),
                    )
                )
        if siblings and runtime_suffix(stem) is None:
            child_verify = first_verify_from_problem_doc(entry.problem_doc.with_name(siblings[0][2]))
            problem_text = umbrella_problem_text(
                entry,
                [(runtime, label, problem_name) for runtime, label, problem_name, _answer_name, _source_refs in siblings],
                child_verify,
            )
            answer_text = umbrella_answer_text(
                entry,
                [(runtime, label, answer_name, source_refs) for runtime, label, _problem_name, answer_name, source_refs in siblings],
            )
            return problem_text, answer_text, goal_text, "runtime별 답안지를 직접 읽으면 된다."

    problem_refs_abs = unique_items(starter_files[:2] + source_files[:4] + test_files[:2] + evidence_files[:3] + config_files[:2], limit=8)
    walkthrough_refs_abs = unique_items(
        source_files[:5] + starter_files[:2] + test_files[:3] + evidence_files[:3] + config_files[:2],
        limit=10,
    )
    answer_refs_abs = unique_items(
        source_files[:5] + starter_files[:2] + test_files[:3] + evidence_files[:4] + config_files[:2],
        limit=12,
    )
    if not answer_refs_abs:
        answer_refs_abs = (starter_files[:2] + test_files[:3] + evidence_files[:3] + config_files[:2])[:8]
    if not problem_refs_abs:
        problem_refs_abs = answer_refs_abs[:6]

    problem_refs = [f"`{relpath(path, entry.problem_doc.parent)}`" for path in problem_refs_abs]
    answer_refs = [f"`{relpath(path, entry.answer_doc.parent)}`" for path in answer_refs_abs]

    starter_bullets = [
        f"{relpath(path, entry.problem_doc.parent)}에서 starter 코드와 입력 경계를 잡는다."
        for path in starter_files[:3]
    ]
    if not starter_bullets:
        starter_bullets = (
            [f"`{relpath(problem_refs_abs[0], entry.problem_doc.parent)}`부터 읽으면 가장 짧게 구현을 시작할 수 있다."]
            if problem_refs_abs
            else ["별도 starter 디렉터리가 없더라도 이 문서의 시작 위치가 가장 짧은 진입점이다."]
        )

    symbol_map = {path: extract_symbols(path) for path in walkthrough_refs_abs}
    walkthrough = [
        f"`{relpath(path, entry.answer_doc.parent)}`: {describe_file(path, symbol_map[path])}"
        for path in walkthrough_refs_abs
    ]
    if not walkthrough:
        walkthrough = [
            "이 단계는 stage-local source가 없는 설계형 단계다.",
            "정답은 요구사항을 산출물 계약, 평가 기준, 검토 순서로 고정하는 것이다.",
        ]

    source_clues = []
    test_clues = []
    for path in walkthrough_refs_abs:
        lower = path.as_posix().lower()
        if "/tests/" in lower or "/__tests__/" in lower or path.name.startswith("test_") or ".test." in path.name or path.name.endswith("_test.go"):
            test_clues.extend(symbol_map[path])
        else:
            source_clues.extend(symbol_map[path])
    source_clues = [item for index, item in enumerate(source_clues) if item and item not in source_clues[:index]]
    test_clues = [item for index, item in enumerate(test_clues) if item and item not in test_clues[:index]]
    verify_commands = infer_verify(
        entry,
        base_dir,
        target_runtime,
        config_files,
        evidence_files,
        problem_readme,
        source_files,
        test_files,
    )

    walkthrough_extras: list[str] = []
    if source_clues and test_clues:
        walkthrough_extras.append(
            f"`{source_clues[0]}` 구현은 `{test_clues[0]}`{' 등' if len(test_clues) > 1 else ''}이 잠근 입력 계약과 상태 전이를 그대로 만족해야 한다."
        )
    elif source_clues:
        walkthrough_extras.append(
            f"`{source_clues[0]}`{' 등' if len(source_clues) > 1 else ''}이 맡는 책임을 한 함수에 뭉개지 말고 상태 전이 단위로 분리한다."
        )
    if verify_commands:
        walkthrough_extras.append(
            f"회귀 게이트는 `{verify_commands[0]}`이며, 핵심 상태 전이를 바꿀 때마다 중간 검증으로 다시 실행한다."
        )
    if config_files:
        walkthrough_extras.append(
            f"`{relpath(config_files[0], entry.answer_doc.parent)}`는 실행 루트와 모듈 경계를 고정해 검증이 어느 위치에서 돌아야 하는지 알려 준다."
        )
    elif evidence_files:
        walkthrough_extras.append(
            f"`{relpath(evidence_files[0], entry.answer_doc.parent)}`{' 등' if len(evidence_files) > 1 else ''}을 함께 읽어 입력 fixture나 trace를 추측이 아니라 근거로 고정한다."
        )
    walkthrough = unique_items(walkthrough + walkthrough_extras, limit=8)

    if len(requirements) >= 2 and requirements[0].endswith("핵심 동작을 source와 test가 같은 방향으로 설명해야 한다."):
        dynamic_requirements: list[str] = []
        if source_clues:
            dynamic_requirements.append(
                f"핵심 구현은 `{source_clues[0]}`{'와 ' + ', '.join(f'`{name}`' for name in source_clues[1:3]) if len(source_clues) > 1 else ''} 흐름이 같은 상태 전이를 유지해야 한다."
            )
        if test_clues:
            dynamic_requirements.append(
                f"검증 기준은 `{test_clues[0]}`{' 등' if len(test_clues) > 1 else ''}이 잠근 입력 계약과 결과를 그대로 재현하는 것이다."
            )
        if starter_files:
            dynamic_requirements.append(
                f"starter 파일 `{relpath(starter_files[0], entry.problem_doc.parent)}`가 비워 둔 확장 지점을 실제 구현으로 닫아야 한다."
            )
        elif problem_refs_abs:
            dynamic_requirements.append(
                f"시작 위치 `{relpath(problem_refs_abs[0], entry.problem_doc.parent)}`부터 읽어 구현 경계를 흔들리지 않게 고정해야 한다."
            )
        dynamic_requirements.append("검증 명령을 실행했을 때 회귀 없이 통과해야 한다.")
        requirements = dynamic_requirements[:4]

    if entry.project == "cs-core" and entry.problem_doc.stem == "datalab":
        verify_commands = [
            "cd /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/datalab/c/tests && ./test_bits",
            "cd /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/datalab/cpp/tests && ./test_bits_cpp",
        ]
    if not verify_commands:
        if not answer_refs_abs:
            verify_commands = ["문제지의 성공 체크리스트와 산출물 계약을 항목별로 대조한다."]
        else:
            verify_commands = ["구현 파일과 테스트 파일을 함께 열어 동작과 계약이 일치하는지 확인한다."]
    verify_notes = infer_verify_notes(verify_commands, config_files, base_dir, target_runtime)
    excludes = contextual_excludes(entry, target_runtime, starter_files, evidence_files, config_files, excludes)
    checklist = actionable_checklist(entry, starter_files, evidence_files, verify_commands, source_clues, test_clues, requirements)

    strategy_bullets = requirements[:3]
    if source_clues:
        primary_source = relpath(source_files[0], entry.answer_doc.parent) if source_files else relpath(answer_refs_abs[0], entry.answer_doc.parent)
        focus = symbol_phrase(source_clues)
        strategy_bullets.append(
            f"첫 진입점은 `{primary_source}`이고, 여기서 {focus} 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다."
        )
    if test_clues:
        locked = symbol_phrase(test_clues)
        strategy_bullets.append(
            f"검증 기준은 {locked} 테스트가 먼저 잠근 동작부터 맞추는 것이다."
        )
    strategy_bullets = strategy_bullets[:4]

    one_line = clean_text(goal_text)
    if source_clues:
        one_line = f"{one_line} 핵심은 `{source_clues[0]}`{'와 ' + ', '.join(f'`{name}`' for name in source_clues[1:3]) if len(source_clues) > 1 else ''} 흐름을 구현하고 테스트를 통과시키는 것이다."
    elif test_clues:
        one_line = f"{one_line} 핵심은 `{test_clues[0]}`{' 등' if len(test_clues) > 1 else ''}이 요구하는 동작을 source에 반영하는 것이다."

    reconstruct_steps = [
        (
            f"`{relpath(starter_files[0], entry.answer_doc.parent)}`와 `{relpath(answer_refs_abs[0], entry.answer_doc.parent)}`를 나란히 열어 먼저 바뀌는 경계를 잡는다."
            if starter_files and answer_refs_abs
            else (
                f"`{relpath(answer_refs_abs[0], entry.answer_doc.parent)}`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다."
                if answer_refs_abs
                else "문제지의 산출물 계약을 먼저 고정하고, 어떤 결과물이 있어야 통과인지 글로 잠근다."
            )
        ),
        (
            f"`{test_clues[0]}`{' 등' if len(test_clues) > 1 else ''}이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다."
            if test_clues
            else (
                f"`{source_clues[0]}`{' 등' if len(source_clues) > 1 else ''}이 맡는 책임을 분리해 각 출력 계약을 완성한다."
                if source_clues
                else "성공 체크리스트 각 항목이 어떤 산출물로 검증되는지 일대일로 대응시킨다."
            )
        ),
        f"`{verify_commands[0]}`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.",
    ]
    failure_points = [
        (
            f"`{relpath(starter_files[0], entry.answer_doc.parent)}` starter skeleton의 빈칸을 그대로 정답으로 착각하지 않는다."
            if starter_files
            else "상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다."
        ),
        (
            f"{symbol_phrase(test_clues)}가 잠근 상태 전이와 입력 계약을 빼먹지 않는다."
            if test_clues
            else (
                f"`{relpath(evidence_files[0], entry.answer_doc.parent)}`{' 등' if len(evidence_files) > 1 else ''} fixture/trace를 읽지 않고 동작을 추측하지 않는다."
                if evidence_files
                else "문제지의 성공 체크리스트와 산출물 계약이 서로 어긋나지 않게 유지한다."
            )
        ),
        f"완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `{verify_commands[0]}`로 회귀를 조기에 잡는다.",
    ]

    has_code_surface = bool(source_files or starter_files or test_files)
    if not has_code_surface:
        goal_structure = requirements[:3] or [goal_text]
        if evidence_files:
            goal_structure.append(
                f"근거 파일은 `{relpath(evidence_files[0], entry.answer_doc.parent)}`{' 등' if len(evidence_files) > 1 else ''}처럼 실제 trace/fixture/스크립트로 고정한다."
            )
        answer_ref_paths = [f"`{relpath(path, entry.answer_doc.parent)}`" for path in answer_refs_abs[:2]]
        solve_steps = [
            (
                f"`{relpath(problem_refs_abs[0], entry.answer_doc.parent)}`를 먼저 열어 어떤 입력과 근거 파일이 이 lab의 사실 원천인지 고정한다."
                if problem_refs_abs
                else "문제지의 목표와 산출물 계약을 먼저 고정한다."
            ),
            (
                f"{'와 '.join(answer_ref_paths)}에서 요구하는 값과 근거를 한 항목씩 대응시킨다."
                if answer_ref_paths
                else "질문, 산출물, 검증 기준을 한 항목씩 대응시킨다."
            ),
            f"`{verify_commands[0]}`를 사용해 빠진 근거와 누락된 항목이 없는지 마지막에 다시 잠근다.",
        ]
        why_correct = [
            "문제 원문이 요구한 질문이나 산출물 계약이 실제 trace, fixture, 검증 스크립트와 일대일로 연결되면 답안이 임의 설명이 아니라 근거 기반 결과가 된다.",
            (
                f"`{verify_commands[0]}`가 통과하면 누락된 질문, 빠진 산출물, 형식 오류가 없는 상태를 재현할 수 있다."
                if verify_commands
                else "검증 기준을 문서와 근거 파일로 다시 대조하면 산출물 완결성을 확인할 수 있다."
            ),
        ]
        answer_text = answer_doc_text_no_code(
            entry=entry,
            one_line=one_line,
            goal_structure=goal_structure[:4],
            solve_steps=solve_steps,
            failure_points=failure_points,
            verify_commands=verify_commands,
            why_correct=why_correct,
            source_refs=answer_refs or ["문제 원문과 근거 파일을 먼저 잠가 산출물 계약을 완성한다."],
        )
    else:
        answer_text = answer_doc_text(
            entry=entry,
            one_line=one_line,
            strategy_bullets=strategy_bullets,
            walkthrough=walkthrough[:8],
            reconstruct_steps=reconstruct_steps,
            verify_commands=verify_commands,
            failure_points=failure_points,
            source_refs=answer_refs[:10] or ["stage-local source가 없으면 문제지의 산출물 계약을 직접 작성해 정답을 고정한다."],
        )

    problem_text = problem_doc_text(
        entry=entry,
        why=why,
        goal_text=goal_text,
        start_refs=problem_refs or answer_refs,
        starter_bullets=starter_bullets,
        requirements=requirements,
        excludes=excludes,
        checklist=checklist[:4],
        verify_commands=verify_commands,
        verify_notes=verify_notes,
    )
    problem_summary = trim_sentence(goal_text, title_for(entry))
    answer_summary = trim_sentence(one_line, title_for(entry))
    return problem_text, answer_text, problem_summary, answer_summary


def section_intro(readme: Path) -> list[str]:
    if not readme.exists():
        return []
    lines: list[str] = []
    previous_heading = ""
    for raw in readme.read_text(encoding="utf-8").splitlines():
        if raw.startswith("| ") or raw.startswith("## 스포일러 경계") or raw.startswith("## 읽는 방법"):
            break
        if raw.startswith("## "):
            if raw == previous_heading:
                continue
            previous_heading = raw
        elif raw.strip():
            previous_heading = ""
        lines.append(raw)
    return lines


def rewrite_catalogs(entries: list[Entry], summaries: dict[str, tuple[str, str]]) -> None:
    grouped: dict[tuple[str, str], list[Entry]] = {}
    for entry in entries:
        grouped.setdefault((entry.project, entry.section), []).append(entry)

    for (project, section), section_entries in grouped.items():
        section_dir = ROOT / project / section
        readme = section_dir / "README.md"
        answer_readme = section_dir / "README_answer.md"
        intro_problem = section_intro(readme)
        intro_answer = section_intro(answer_readme)
        problem_rows = []
        answer_rows = []
        for entry in sorted(section_entries, key=lambda item: item.problem_doc.name):
            problem_summary, answer_summary = summaries[str(entry.problem_doc)]
            verify = next(
                (
                    line.strip()
                    for line in entry.problem_doc.read_text(encoding="utf-8").splitlines()
                    if line.strip() and not line.startswith("#") and not line.startswith("```")
                ),
                "문제지를 열어 확인",
            )
            verify_cmd = "# 검증 명령은 leaf 문제지에서 확인"
            for block in re.findall(r"```bash\n(.*?)```", entry.problem_doc.read_text(encoding="utf-8"), flags=re.S):
                command = next((line.strip() for line in block.splitlines() if line.strip()), "")
                if command:
                    verify_cmd = command
                    break
            problem_rows.append(
                f"| [{entry.problem_doc.stem}]({entry.problem_doc.name}) | {clean_text(problem_summary)} | `{verify_cmd}` |"
            )
            answer_rows.append(
                f"| [{entry.problem_doc.stem}]({entry.answer_doc.name}) | {clean_text(answer_summary)} | `{verify_cmd}` |"
            )
        readme.write_text(
            "\n\n".join(
                part
                for part in [
                    "\n".join(intro_problem).strip(),
                    "| lab | 한 줄 문제 요약 | 검증 시작점 |\n| --- | --- | --- |\n" + "\n".join(problem_rows),
                    "## 스포일러 경계\n\n각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.",
                ]
                if part
            ).strip()
            + "\n",
            encoding="utf-8",
        )
        answer_readme.write_text(
            "\n\n".join(
                part
                for part in [
                    "\n".join(intro_answer).strip(),
                    "| lab | 해답 요약 | 검증 |\n| --- | --- | --- |\n" + "\n".join(answer_rows),
                    "## 읽는 방법\n\n각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.",
                ]
                if part
            ).strip()
            + "\n",
            encoding="utf-8",
        )


def rewrite_manifest(entries: list[Entry]) -> None:
    lines = [
        "# problem-subject lab manifest",
        "",
        "| n | project | section | slug | runtime | problem doc | answer doc |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for index, entry in enumerate(entries, start=1):
        problem_doc = entry.problem_doc.relative_to(ROOT).as_posix()
        answer_doc = entry.answer_doc.relative_to(ROOT).as_posix()
        lines.append(
            f"| {index} | `{entry.project}` | `{entry.section}` | `{entry.slug}` | `{entry.runtime}` | `{problem_doc}` | `{answer_doc}` |"
        )
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    entries = parse_manifest()
    candidates = {
        project_dir.name: discover_candidates(project_dir)
        for project_dir in sorted(
            directory
            for directory in ROOT.iterdir()
            if directory.is_dir() and any((directory / section).exists() for section in SECTIONS)
        )
    }
    summaries: dict[str, tuple[str, str]] = {}
    total = len(entries)
    for index, entry in enumerate(entries, start=1):
        problem_text, answer_text, problem_summary, answer_summary = build_docs(entry, candidates[entry.project])
        entry.problem_doc.parent.mkdir(parents=True, exist_ok=True)
        entry.answer_doc.parent.mkdir(parents=True, exist_ok=True)
        entry.problem_doc.write_text(problem_text, encoding="utf-8")
        entry.answer_doc.write_text(answer_text, encoding="utf-8")
        summaries[str(entry.problem_doc)] = (problem_summary, answer_summary)
        print(f"{index} / {total} {entry.problem_doc.relative_to(ROOT)}")
    rewrite_catalogs(entries, summaries)
    rewrite_manifest(entries)
    print(f"done {total} / {total}")


if __name__ == "__main__":
    main()

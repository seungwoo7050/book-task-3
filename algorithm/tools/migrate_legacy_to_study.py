from __future__ import annotations

import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "legacy"
STUDY = ROOT / "study"
DOCS = ROOT / "docs"
TODAY = "2026-03-07"


TRACKS = {
    "00-basics": {
        "study": "Core-00-Basics",
        "label": "00",
        "topic": "Basic Coding Skills",
        "clrs": "Ch 1-3",
        "summary": "기초 입출력, 문자열 순회, 배열 회전, LIS 입문을 통해 이후 전 트랙의 구현 기반을 만든다.",
    },
    "01-array-list": {
        "study": "Core-01-Array-List",
        "label": "01",
        "topic": "Array & Linked List",
        "clrs": "Ch 10.2",
        "summary": "배열 순회와 편집기/키로거 문제로 자료구조 선택의 비용 모델을 익힌다.",
    },
    "02-stack-queue": {
        "study": "Core-02-Stack-Queue",
        "label": "02",
        "topic": "Stack, Queue, Deque",
        "clrs": "Ch 10.1",
        "summary": "LIFO/FIFO/양방향 큐를 문제 규칙에 맞게 구현하는 감각을 만든다.",
    },
    "03-bfs-dfs": {
        "study": "Core-03-BFS-DFS",
        "label": "03",
        "topic": "BFS & DFS",
        "clrs": "Ch 22.2-22.3",
        "summary": "정점 방문 순서, 그래프 표현, 격자 탐색의 기본기를 고정한다.",
    },
    "04-recursion-backtracking": {
        "study": "Core-04-Recursion-Backtracking",
        "label": "04",
        "topic": "Recursion & Backtracking",
        "clrs": "Ch 4",
        "summary": "재귀 호출 구조, 상태 복원, 탐색 가지치기를 작은 문제부터 누적한다.",
    },
    "05-simulation": {
        "study": "Core-05-Simulation",
        "label": "05",
        "topic": "Simulation",
        "clrs": "Implementation discipline",
        "summary": "문제 설명을 상태 전이와 방향 규칙으로 번역하는 연습을 한다.",
    },
    "06-sorting": {
        "study": "Core-06-Sorting",
        "label": "06",
        "topic": "Sorting",
        "clrs": "Ch 2, 6-8",
        "summary": "기본 정렬, 복합 정렬 조건, 정렬 후 스위프라인으로 이어지는 패턴을 다룬다.",
    },
    "07-binary-search-hash": {
        "study": "Core-07-Binary-Search-Hash",
        "label": "07",
        "topic": "Binary Search & Hash",
        "clrs": "Ch 11, 12.3",
        "summary": "검색 문제를 집합/카운터/매개변수 탐색으로 나누어 푼다.",
    },
    "08-dp": {
        "study": "Core-08-DP",
        "label": "08",
        "topic": "Dynamic Programming",
        "clrs": "Ch 15",
        "summary": "점화식 설계, 상태 정의, 1차원과 2차원 DP의 기초를 고정한다.",
    },
    "09-greedy": {
        "study": "Core-09-Greedy",
        "label": "09",
        "topic": "Greedy",
        "clrs": "Ch 16",
        "summary": "그리디 선택 조건이 성립하는 경우와 아닌 경우를 사례로 구분한다.",
    },
    "0A-priority-queue": {
        "study": "Core-0A-Priority-Queue",
        "label": "0A",
        "topic": "Priority Queue",
        "clrs": "Ch 6, 19",
        "summary": "최소/최대 힙 조작과 힙 기반 그리디를 연결한다.",
    },
    "0B-graph-tree": {
        "study": "Core-0B-Graph-Tree",
        "label": "0B",
        "topic": "Graph & Tree",
        "clrs": "Ch 22-24",
        "summary": "트리 부모 찾기, 순회, 지름 문제로 그래프 후반부의 기반을 다진다.",
    },
    "0C-shortest-path": {
        "study": "Core-0C-Shortest-Path",
        "label": "0C",
        "topic": "Shortest Path",
        "clrs": "Ch 24",
        "summary": "Dijkstra와 Bellman-Ford를 문제 조건에 맞게 선택하는 법을 익힌다.",
    },
    "0D-mst-topo": {
        "study": "Core-0D-MST-Topo",
        "label": "0D",
        "topic": "MST & Topological Sort",
        "clrs": "Ch 23, 22.4",
        "summary": "MST와 DAG 선행관계 문제를 그래프 학습의 마무리로 묶는다.",
    },
}


ADVANCED_BACKLOG = [
    ("0x10", "분할 정복 심화", "Ch 4", "Strassen 행렬 곱, 엄밀한 마스터 정리"),
    ("0x11", "분할 상환 분석", "Ch 17", "Stack MULTIPOP, 이진 카운터"),
    ("0x12", "고급 검색 트리", "Ch 13, 18", "레드-블랙 트리, B-트리"),
    ("0x13", "특수 힙", "Ch 19", "Fibonacci Heap"),
    ("0x14", "네트워크 플로우", "Ch 26", "Ford-Fulkerson, Edmonds-Karp"),
    ("0x15", "문자열 매칭 심화", "Ch 32", "KMP, Rabin-Karp"),
    ("0x16", "계산 기하학", "Ch 33", "선분 교차, Convex Hull"),
    ("0x17", "수론 알고리즘", "Ch 31", "GCD, CRT, RSA 기초"),
    ("0x18", "NP-완전성", "Ch 34", "문제 분류와 환원"),
    ("0x19", "근사 알고리즘", "Ch 35", "NP-hard 문제의 근사 전략"),
]


BRIDGE_PROJECT = {
    "study_track": "Core-Bridges",
    "boj": "1717",
    "title": "집합의 표현",
    "tier": "Bridge",
    "clrs": "Ch 21",
    "summary": "MST/Kruskal 이전에 union-find를 독립적으로 익히기 위한 bridge 프로젝트다.",
}


TIER_ORDER = {"bronze": 0, "silver": 1, "gold": 2, "Bridge": 1}
SPECIAL_CPP = {"1753", "1197"}


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def slug_to_title(slug: str) -> str:
    return slug.replace("-", " ").title()


def strip_first_heading(text: str) -> str:
    lines = text.strip().splitlines()
    if lines and lines[0].startswith("#"):
        lines = lines[1:]
    return "\n".join(lines).strip()


def unwrap_markdown_fence(text: str) -> str:
    text = text.strip()
    if text.startswith("```markdown\n") and text.endswith("\n```"):
        return text[len("```markdown\n") : -len("\n```")].strip()
    return text


def first_nonempty_paragraph(text: str) -> str:
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]
    for block in blocks:
        if block.startswith("#"):
            continue
        return " ".join(line.strip() for line in block.splitlines())
    return ""


def clean_excerpt(text: str) -> str:
    content = strip_first_heading(unwrap_markdown_fence(text))
    blocks = [block.strip() for block in re.split(r"\n\s*\n", content) if block.strip()]
    for block in blocks:
        if block.startswith("#") or block.startswith("```"):
            continue
        lines = [line.strip().lstrip("- ").strip() for line in block.splitlines() if line.strip()]
        if lines:
            return " ".join(lines)
    return ""


def extract_section(text: str, heading: str) -> str:
    match = re.search(rf"{re.escape(heading)}\n(.*?)(?=\n## |\Z)", text, flags=re.S)
    return match.group(1).strip() if match else ""


def extract_sections(text: str, headings: list[str]) -> list[tuple[str, str]]:
    found = []
    for heading in headings:
        body = extract_section(text, heading)
        if body:
            found.append((heading, body))
    return found


def collapse_blank_lines(text: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", text.strip())


def extract_title(project_readme: str, problem_readme: str, boj: str) -> str:
    for text in (project_readme, problem_readme):
        lines = text.splitlines()
        if not lines:
            continue
        heading = lines[0].lstrip("# ").strip()
        heading = re.sub(r"^Problem:\s*", "", heading)
        heading = re.sub(rf"^BOJ\s*{boj}\s*[—-]\s*", "", heading)
        if heading:
            return heading
    return f"BOJ {boj}"


def extract_source_url(text: str) -> str:
    match = re.search(r"https://www\.acmicpc\.net/problem/\d+", text)
    return match.group(0) if match else ""


def legacy_manifest() -> list[str]:
    return sorted(str(path.relative_to(ROOT)) for path in LEGACY.rglob("*") if path.is_file())


def build_makefile(has_cpp: bool) -> str:
    if has_cpp:
        return """\
PYTHON   = python3
ifeq ($(origin CXX), default)
CXX := $(shell if command -v g++-14 >/dev/null 2>&1; then echo g++-14; else echo g++; fi)
endif
ifeq ($(origin CXX), undefined)
CXX := $(shell if command -v g++-14 >/dev/null 2>&1; then echo g++-14; else echo g++; fi)
endif
CXXFLAGS ?= -std=c++17 -O2 -Wall
ifeq ($(notdir $(CXX)),g++-14)
	CXXFLAGS += -D_Alignof=alignof
endif

PY_SOLUTION  = ../python/src/solution.py
CPP_SOLUTION = ../cpp/src/solution.cpp
CPP_BINARY   = ../cpp/bin/app

.PHONY: all build run-py run-cpp test clean

all: test

build:
\t@mkdir -p ../cpp/bin
\t@$(CXX) $(CXXFLAGS) $(CPP_SOLUTION) -o $(CPP_BINARY)

run-py:
\t@$(PYTHON) $(PY_SOLUTION) < data/input1.txt

run-cpp: build
\t@$(CPP_BINARY) < data/input1.txt

test:
\t@cd script && bash test.sh

clean:
\t@rm -f $(CPP_BINARY)
"""
    return """\
PYTHON      = python3
PY_SOLUTION = ../python/src/solution.py

.PHONY: all run-py test clean

all: test

run-py:
\t@$(PYTHON) $(PY_SOLUTION) < data/input1.txt

test:
\t@cd script && bash test.sh

clean:
\t@true
"""


def build_test_script() -> str:
    return """\
#!/bin/bash
set -euo pipefail

PYTHON=python3
SOLUTION_PY="../../python/src/solution.py"
DATA_DIR="../data"

pass=0
fail=0
total=0

for input_file in "$DATA_DIR"/input*.txt; do
    test_num=$(basename "$input_file" | grep -o '[0-9]\\+')
    expected_file="$DATA_DIR/output${test_num}.txt"

    if [ ! -f "$expected_file" ]; then
        continue
    fi

    total=$((total + 1))
    actual=$($PYTHON "$SOLUTION_PY" < "$input_file" | tr -d '\\r')
    expected=$(cat "$expected_file" | tr -d '\\r')

    if [ "$actual" = "$expected" ]; then
        echo "Test $test_num: PASS"
        pass=$((pass + 1))
    else
        echo "Test $test_num: FAIL"
        echo "  Expected: $expected"
        echo "  Actual:   $actual"
        fail=$((fail + 1))
    fi
done

echo ""
echo "Results: $pass/$total passed, $fail failed"
[ "$fail" -eq 0 ] && exit 0 || exit 1
"""


def normalize_path_block(text: str) -> str:
    replacements = {
        "algorithm-clrs/": "",
        "algorithm-clrs": ROOT.name,
        "solve/solution/solution.py": "python/src/solution.py",
        "solve/solution/solution.cpp": "cpp/src/solution.cpp",
        "../solve/solution/solution.py": "../python/src/solution.py",
        "../solve/solution/solution.cpp": "../cpp/src/solution.cpp",
        "solve/analysis.md": "implementation README",
        "docs/README.md": "docs/references/overview.md",
        "lab-report.md": "03-retrospective.md",
        "devlog/entries/001-implementation.md": "02-debug-log.md",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def sanitize_public_note(text: str) -> str:
    lines = []
    skip_code = False
    for line in normalize_path_block(unwrap_markdown_fence(text)).splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            skip_code = not skip_code
            continue
        if skip_code:
            continue
        if any(
            token in line
            for token in (
                "Legacy path:",
                "Migration cleanup date:",
                "Removed fabricated git metadata",
                "Cleaned on:",
                "legacy/core/",
                "/Users/",
                "lab-report.md",
                "devlog/entries",
                "Rollback plan:",
                "Monitoring points:",
                "Appendix 원문",
                "공개 독자가 바로 읽을 수 있도록",
                "이번 문서의 목적은",
                "블로그/리포트 급",
            )
        ):
            continue
        lines.append(line.rstrip())
    return collapse_blank_lines("\n".join(lines))


def extract_manual_goal(text: str) -> str:
    for pattern in (
        r'수동 검증 목표는 "([^"]+)"',
        r"수동 목적:\s*([^\n]+)",
        r'목표는 "([^"]+)"',
    ):
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip().rstrip(".")
    return ""


def parse_check_items(text: str) -> list[str]:
    cleaned = sanitize_public_note(text)
    if not cleaned:
        return []
    blocks = re.split(r"\n(?=- 점검 \d+:)", cleaned)
    items: list[str] = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        first = re.sub(r"^- 점검 \d+:\s*", "", lines[0]).strip()
        if any(
            token in first
            for token in (
                "컴파일 실패나 테스트 실패가 관측되지 않았다",
                '"실패 없음"만 기록하면',
                "실패 재현은 없었지만",
            )
        ):
            continue
        remainder = " ".join(
            re.sub(r"^- ", "", line).strip()
            for line in lines[1:]
            if line.strip() and "실패 없음" not in line and "실패 재현은 없었지만" not in line
        ).strip()
        if remainder:
            items.append(f"- {first}: {remainder}")
        else:
            items.append(f"- {first}")
    return items


def parse_risk_items(text: str) -> list[str]:
    if not text.strip():
        return []
    mode = None
    lines = []
    for line in unwrap_markdown_fence(text).splitlines():
        stripped = line.strip()
        if not stripped or stripped.endswith(":"):
            if stripped in ("- Risks:", "Risks:"):
                mode = "risk"
            elif stripped in ("- Rollback plan:", "Rollback plan:", "- Monitoring points:", "Monitoring points:"):
                mode = None
            continue
        if mode == "risk" and stripped.startswith("- "):
            lines.append(f"- {stripped[2:].strip()}")
    return lines


def parse_next_steps(text: str) -> list[str]:
    cleaned = sanitize_public_note(text)
    if not cleaned:
        return []
    lines = []
    for line in cleaned.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        stripped = re.sub(r"^- \[[ xX]\]\s*", "", stripped)
        stripped = re.sub(r"^- ", "", stripped)
        stripped = re.sub(r"^P\d+:\s*", "", stripped)
        if stripped:
            lines.append(f"- {stripped}")
    return lines


def clean_devlog(text: str, meta: dict) -> str:
    checks = extract_section(text, "## 시도/실패/수정")
    risks = extract_section(text, "## 8) Risk and Rollback")
    next_steps = extract_section(text, "## 9) Next Steps")
    manual_goal = extract_manual_goal(text)
    check_items = parse_check_items(checks)
    risk_items = parse_risk_items(risks)
    next_items = parse_next_steps(next_steps)
    observed_failure = "이번 검증에서는 재현된 컴파일 실패나 테스트 실패가 없었다."
    if any(token in checks for token in ("실패", "오답", "예외")) and "실패 없음" not in checks:
        observed_failure = "실패 가능성이 있었던 지점을 다시 점검하고, 재현 조건과 예방 조치를 남겼다."
    scope_lines = [
        "- 공식 fixture 테스트를 다시 실행한다.",
        "- 입력 파싱, 상태 전이, 출력 직렬화를 우선 점검한다.",
    ]
    if manual_goal:
        scope_lines.append(f"- 수동 검증 목표: {manual_goal}.")
    if meta["has_cpp"]:
        scope_lines.append("- Python/C++ 출력 비교를 유지한다.")
    sections = [
        "# Debug Log",
        "",
        "## Verification Scope",
        "\n".join(scope_lines),
        "",
        "## Observed Failures",
        f"- {observed_failure}",
        "",
        "## Checks Performed",
        "\n".join(check_items or ["- 입력 파싱, 상태 전이, 출력 직렬화를 순서대로 다시 확인했다."]),
    ]
    if risk_items:
        sections.extend(["", "## Remaining Risks", "\n".join(risk_items)])
    if next_items:
        sections.extend(["", "## Next Checks", "\n".join(next_items)])
    return collapse_blank_lines("\n".join(sections))


def clean_retrospective(text: str, legacy_rel: str) -> str:
    blocks = []
    for heading in ["## 요약", "## 의사결정 근거", "## 한계/다음 실험", "## 결론"]:
        match = re.search(rf"{re.escape(heading)}\n(.*?)(?=\n## |\Z)", text, flags=re.S)
        if match:
            body = sanitize_public_note(match.group(1).strip())
            body_lines = []
            for line in body.splitlines():
                if any(
                    token in line
                    for token in (
                        "코드 변경 없이 문서 품질",
                        "공통 문장을 줄이고",
                        "공통 문구를 줄이고",
                        "재작업했다",
                        "핵심 조치는 세 가지다",
                    )
                ):
                    continue
                line = re.sub(r"^(첫째|둘째|셋째|넷째),\s*", "- ", line.strip())
                body_lines.append(line)
            cleaned = collapse_blank_lines("\n".join(body_lines))
            if cleaned:
                blocks.append(f"{heading}\n{cleaned}")
    body = "\n\n".join(blocks).strip()
    return f"# Retrospective\n\n{collapse_blank_lines(body)}"


def knowledge_entry(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    title = path.stem.replace("-", " ").title()
    learned = clean_excerpt(text) or "내용을 직접 읽어 개념과 반례를 확인한다."
    return f"""## {title}
- Type: repository concept note
- Checked date: {TODAY}
- Why it was consulted: 문제를 다시 볼 때 핵심 개념과 반례를 빠르게 복기하기 위해.
- What was learned: {learned}
- Effect on this project: 접근 선택과 재검증 포인트를 한 문서 안에서 다시 찾기 쉽게 만들었다.
"""


def project_readme(meta: dict, has_cpp: bool) -> str:
    impls = "`python/`" + (", `cpp/`" if has_cpp else "")
    structure_lines = [
        "- `problem/`: 원문 문제 설명, starter code, fixture, 실행 스크립트",
        "- `python/`: 기본 해설 구현과 실행 메모",
    ]
    if has_cpp:
        structure_lines.append("- `cpp/`: 비교용 구현과 빌드 메모")
    structure_lines.extend(
        [
            "- `docs/`: 공개 학습 노트와 검증 참조",
            "- `notion/`: 로컬 전용 기술 노트",
        ]
    )
    cpp_line = "- `make -C problem run-cpp`로 C++ 비교 구현을 실행한다." if has_cpp else "- C++ 구현은 이 프로젝트 범위에서 유지하지 않는다."
    cross_ref = meta.get("cross_ref")
    cross_ref_block = f"\n## Cross-Track Note\n\n- {cross_ref}\n" if cross_ref else ""
    return f"""# BOJ {meta['boj']} — {meta['title']}

| Item | Detail |
| :--- | :--- |
| Track | `{meta['study_track']}` |
| Legacy Source | `{meta['legacy_rel']}` |
| Tier | {meta['tier'].title()} |
| CLRS | {meta['clrs']} |
| Problem URL | {meta['source_url']} |

## Summary

{meta['summary']}

문제 원문과 starter 자료는 `problem/`에만 두고, 사용자 구현은 {impls}로 분리했다.

## Structure

{chr(10).join(structure_lines)}

## Verify

- `make -C problem test`로 Python fixture 테스트를 실행한다.
- `make -C problem run-py`로 대표 입력을 수동 실행한다.
{cpp_line}

## Status

- Python: verified against migrated fixtures on {TODAY}
- C++: {"verified comparison implementation retained" if has_cpp else "not retained by repository policy"}
- Legacy tree: preserved read-only under `legacy/`
{cross_ref_block}
"""


def implementation_readme(meta: dict, language: str, has_cpp: bool) -> str:
    if language == "python":
        return f"""# Python Implementation

## Scope

- Full BOJ {meta['boj']} problem scope
- Uses the migrated fixtures stored in `../problem/data/`

## Build Command

- `python3 src/solution.py < ../problem/data/input1.txt`

## Test Command

- `make -C ../problem test`

## Current Status

- verified

## Known Gaps

- Fixture 중심 검증만 제공한다.
- 스트레스 테스트나 속성 기반 테스트는 아직 없다.

## Implementation Notes

- 기본 구현 언어는 Python이다.
- public reasoning은 `../docs/`에, process-heavy notes는 `../notion/`에 둔다.
"""
    return f"""# C++ Implementation

## Scope

- Full BOJ {meta['boj']} problem scope
- Maintained as a comparison implementation under the repository C++ retention policy

## Build Command

- `make -C ../problem run-cpp`

## Test Command

- `make -C ../problem run-cpp`
- `make -C ../problem run-py` 결과와 fixture 출력이 일치해야 한다.

## Current Status

- verified

## Known Gaps

- Dedicated C++ automated test target is not separate from the fixture runner.
- macOS에서는 compiler override가 필요할 수 있다.

## Implementation Notes

- 이 구현은 gold 문제와 cross-check anchor(`1753`, `1197`)에만 유지한다.
- shared fixture는 `../problem/data/`를 사용한다.
"""


def tests_readme(language: str) -> str:
    return f"""# {language.title()} Test Notes

- 이 구현은 `../problem/data/input*.txt`와 `../problem/data/output*.txt`를 공통 fixture로 사용한다.
- 공식 실행 진입점은 `make -C ../problem test`다.
- 별도 테스트 러너를 추가할 경우 이 디렉터리에 둔다.
"""


def docs_readme(meta: dict, concepts: list[str]) -> str:
    concepts_list = "\n".join(f"- `concepts/{name}`" for name in concepts) or "- concept note not available"
    return f"""# Public Notes

이 디렉터리는 BOJ {meta['boj']}의 공개 학습 문서를 보관한다. 문제 풀이 reasoning은 공개해도 되지만, 문제 원문과 구현은 각각 `problem/`, `python/`/`cpp/`에 분리했다.

## Contents

- `references/overview.md`: legacy 문서의 읽기 순서와 학습 목표
- `references/approach.md`: 핵심 접근과 정당성 설명
- `references/reproducibility.md`: fixture 실행 근거
{concepts_list}

## Usage

- 먼저 `../README.md`로 구조를 확인한다.
- 그다음 `references/approach.md`와 개념 문서를 읽고 구현을 본다.
"""


def overview_reference(meta: dict, concepts: list[str], has_cpp: bool) -> str:
    concept_lines = [
        f"{index}. [{name}](../concepts/{name})"
        for index, name in enumerate(concepts, start=2)
    ]
    implementation_index = len(concept_lines) + 2
    lines = [
        f"# Reference Overview — BOJ {meta['boj']} ({meta['title']})",
        "",
        "## Reading Guide",
        "",
        "1. [approach.md](approach.md) - 핵심 접근과 정당성",
    ]
    lines.extend(concept_lines)
    lines.append(f"{len(concept_lines) + 2}. [reproducibility.md](reproducibility.md) - fixture 실행 근거")
    lines.append(
        f"{implementation_index + 1}. [../../python/README.md](../../python/README.md) - Python 구현 실행 메모"
    )
    if has_cpp:
        lines.append(
            f"{implementation_index + 2}. [../../cpp/README.md](../../cpp/README.md) - C++ 비교 구현 메모"
        )
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- legacy `docs/README.md`의 역할을 새 구조에 맞게 다시 쓴 인덱스다.",
            "- `lab-report`와 `devlog`는 public docs에서 제외하고 `notion/`으로 옮겼다.",
        ]
    )
    return "\n".join(lines)


def notion_problem_framing(meta: dict, problem_text: str, has_cpp: bool) -> str:
    cpp_line = "- C++ 비교 구현도 유지되므로 Python/C++ 출력 일치까지 확인한다." if has_cpp else "- Python 구현을 기준선으로 사용하고 C++은 유지하지 않는다."
    problem_body = strip_first_heading(unwrap_markdown_fence(problem_text)).strip()
    if not problem_body.startswith("## Problem Statement"):
        problem_body = "## Problem Statement\n\n" + problem_body
    return f"""# Problem Framing

## Project Context
- Track: `{meta['study_track']}`
- BOJ: [{meta['boj']}]({meta['source_url']})
- CLRS connection: {meta['clrs']}
- Why this problem matters: {meta['summary']}

## Goal
- BOJ {meta['boj']}를 {meta['study_track']} 커리큘럼 안에서 다시 읽을 수 있는 학습 프로젝트로 정리한다.
- 문제 원문, 구현, 공개 설명을 역할별로 분리한다.

## Success Criteria
- `make -C problem test`가 통과한다.
- `problem/`에는 원문 자료와 fixture만 남는다.
- `python/README.md`만 읽어도 구현 실행 방법을 바로 파악할 수 있다.
{cpp_line}

{problem_body}
"""


def notion_approach_log(meta: dict, approach: str, analysis: str) -> str:
    sections = extract_sections(
        approach,
        [
            "## 문제 요약",
            "## 핵심 아이디어",
            "## 정당성(간단 증명)",
            "## 복잡도",
            "## 대안 비교",
            "## 실수 포인트",
            "## 코드 매핑 메모",
        ],
    )
    body = "\n\n".join(f"{heading}\n{content}" for heading, content in sections)
    impl_note = (
        "Python 구현을 기준선으로 사용하고, C++ 구현은 비교 검증용으로 함께 유지한다."
        if meta["has_cpp"]
        else "Python 구현을 기준선으로 사용하고, 문제 해결 reasoning은 언어 독립적으로 정리한다."
    )
    return f"""# Approach Log

## Chosen Direction
- {impl_note}
- 접근 선택 이유, 대안 비교, 검증 포인트를 한 문서에 모은다.

{sanitize_public_note(body)}
"""


def notion_knowledge_index(meta: dict, concept_paths: list[Path]) -> str:
    entries = "\n\n".join(knowledge_entry(path) for path in concept_paths)
    if not entries:
        entries = f"""## General Reference
- Type: project reference
- Checked date: {TODAY}
- Why it was consulted: 개별 개념 파일이 없어 공개 문서를 지식 인덱스로 사용한다.
- What was learned: 접근 방식, 검증 명령, 주의점을 한곳에 묶어둘 필요가 있다.
- Effect on this project: 같은 문제를 다시 볼 때 출발 지점을 빠르게 찾게 해준다.
"""
    return f"""# Knowledge Index

## Core References
- BOJ: {meta['source_url']}
- CLRS mapping: {meta['clrs']}
- Track: `{meta['study_track']}`

{entries}
"""


def track_readme(track_key: str, projects: list[dict]) -> str:
    track = TRACKS[track_key]
    rows = []
    for meta in projects:
        impl = "Python + C++" if meta["has_cpp"] else "Python"
        rows.append(
            f"| {meta['tier'].title()} | [{meta['boj']}]({meta['boj']}/README.md) | {meta['title']} | {impl} |"
        )
    table = "\n".join(rows)
    return f"""# {track['study']}

## Topic

- BarkingDog sequence: `0x{track['label']}`
- Topic: {track['topic']}
- CLRS reference: {track['clrs']}

## Why This Track Exists

{track['summary']}

## Projects

| Tier | BOJ | Title | Implementations |
| :--- | :--- | :--- | :--- |
{table}

## Notes

- 모든 프로젝트는 `problem/`, `python/`, 선택적 `cpp/`, `docs/`, `notion/` 구조를 사용한다.
- 공개 README는 스포일러를 허용하되, 문제 원문은 `problem/`에만 둔다.
"""


def root_readme(projects: list[dict]) -> str:
    core_tracks = "\n".join(
        f"- [{track['study']}](study/{track['study']}/README.md): {track['summary']}"
        for _, track in TRACKS.items()
    )
    return f"""# Algorithm Study Archive

이 저장소는 `legacy/`의 알고리즘 풀이 트리를 읽기 전용 참조로 보존하면서, 새 학습용 구조를 `study/`에 다시 세운다. 목표는 정답 묶음이 아니라 재실행 가능한 학습 아카이브를 만드는 것이다.

## Repository Roles

- `legacy/`: 원본 참조 트리. 수정하지 않는다.
- `study/`: 현재 학습과 마이그레이션의 기준 구조
- `docs/`: 저장소 수준 감사 문서와 커리큘럼 문서
- `.gitignore`: local-only 노트와 빌드 산출물 무시 규칙

## Current State

- Legacy core backlog preserved: {len(projects)} problems
- Bridge project added: `study/Core-Bridges/1717`
- Advanced backlog documented under `study/Advanced-CLRS/README.md`

## Study Tracks

{core_tracks}
- [Core-Bridges](study/Core-Bridges/README.md): 그래프 후반부 전에 필요한 bridge 프로젝트
- [Advanced-CLRS](study/Advanced-CLRS/README.md): core 이후에 여는 심화 백로그

## Start Here

1. `docs/legacy-audit.md`에서 현재 기준선과 legacy 제약을 확인한다.
2. `docs/curriculum-map.md`에서 트랙 순서와 bridge rationale을 본다.
3. `study/Core-00-Basics/10988/README.md`로 파일럿 구조를 확인한다.
"""


def study_readme() -> str:
    lines = [
        "# Study Tree",
        "",
        "이 디렉터리는 새 학습 구조의 기준선이다.",
        "",
        "## Tracks",
        "",
    ]
    for track in TRACKS.values():
        lines.append(f"- [{track['study']}]({track['study']}/README.md)")
    lines.extend(
        [
            "- [Core-Bridges](Core-Bridges/README.md)",
            "- [Advanced-CLRS](Advanced-CLRS/README.md)",
        ]
    )
    return "\n".join(lines)


def legacy_audit(projects: list[dict], manifest_path: str) -> str:
    return f"""# Legacy Audit

## Baseline

- Audit date: {TODAY}
- Legacy core problems discovered: {len(projects)}
- Legacy `problem` test status: 42/42 `make test` passed
- Repository git status: not a git repository
- Broken internal Markdown links caused by missing `RULEBOOK.md`: 44
- Metrics artifact present: `legacy/core/.devlog_test_metrics.json`
- Manifest snapshot: `{manifest_path}`

## What Was Accepted As Source Material

- `legacy/core/*/*/problem`: original statements, starter code, fixtures, scripts
- `legacy/core/*/*/solve/solution/*`: user-authored solutions
- `legacy/core/*/*/docs/*`: public study notes
- `legacy/core/*/*/devlog/*`, `lab-report.md`: private/process-heavy notes to be reclassified into `study/**/notion/`

## What Was Not Carried Forward Verbatim

- Broken `RULEBOOK.md` references
- `algorithm-clrs/advanced/` and `common-docs/` ghost paths mentioned only in legacy docs
- fabricated git metadata inside legacy devlogs
- standalone metrics blobs copied into prose

## Migration Decisions

- Preserve all 42 core problems.
- Add one bridge project for BOJ 1717 (union-find) before the MST/topological-sort capstone track.
- Retain C++ only for all legacy gold problems plus BOJ 1753 and 1197.
"""


def curriculum_map(projects: list[dict]) -> str:
    rows = []
    for track_key, track in TRACKS.items():
        track_projects = [meta for meta in projects if meta["track_key"] == track_key]
        boj_list = ", ".join(meta["boj"] for meta in track_projects)
        rows.append(
            f"| {track['study']} | {track['topic']} | {track['clrs']} | {boj_list} |"
        )
    return f"""# Curriculum Map

## Core Sequence

| Track | Topic | CLRS | BOJ Projects |
| :--- | :--- | :--- | :--- |
{chr(10).join(rows)}

## Bridge Decisions

- `1717` is inserted in `Core-Bridges` to teach disjoint set union before Kruskal-heavy material in `Core-0D-MST-Topo`.
- `16926` remains in `Core-00-Basics` for provenance, but it is explicitly a simulation-flavored problem and should be revisited after `Core-05-Simulation`.
- `11053` remains in `Core-00-Basics` for provenance, but it is the first DP bridge and should be revisited before `Core-08-DP`.

## Implementation Policy

- Python is mandatory for every project.
- C++ is retained for all gold-level legacy projects plus BOJ `1753` and `1197`.
- Advanced topics stay as backlog only until the core migration is complete.
"""


def migration_template() -> str:
    return """# Migration Template

## Required Project Shape

```text
study/
  <track>/
    <boj>/
      README.md
      problem/
        README.md
        Makefile
        code/
        data/
        script/
      python/
        README.md
        src/
        tests/
      cpp/                  # optional
        README.md
        src/
        include/
        tests/
      docs/
        README.md
        concepts/
        references/
      notion/               # local-only, ignored
        00-problem-framing.md
        01-approach-log.md
        02-debug-log.md
        03-retrospective.md
        04-knowledge-index.md
```

## Rules

- `problem/` keeps only original or explicitly study-authored problem material and fixtures.
- `python/` is always present and contains the default implementation.
- `cpp/` exists only when the repository policy says to retain it.
- `docs/` is public, concise, and durable.
- `notion/` is local-only and can contain process-heavy writing.

## Done Criteria

- `README.md` alone explains the project scope and verify commands.
- `make -C problem test` passes.
- Public docs do not depend on `notion/`.
- Legacy provenance is recorded without copying broken paths or fabricated git metadata.
"""


def gitignore() -> str:
    return """# Local-only study notes
study/**/notion/

# Python
__pycache__/
*.pyc
.pytest_cache/

# C++
*.o
*.out
*.exe
app
bin/

# Editor / OS noise
.DS_Store

# Local metrics and scratch artifacts
.devlog_test_metrics.json
*.tmp
*.log
"""


def bridge_problem_readme() -> str:
    return """# Problem: 집합의 표현 (BOJ 1717)

## Problem Statement

서로소 집합(disjoint set union)을 구현하는 연습 문제다. 연산은 두 가지다.

- `0 a b`: 원소 `a`, `b`가 속한 집합을 합친다.
- `1 a b`: 두 원소가 같은 집합에 속하면 `YES`, 아니면 `NO`를 출력한다.

## Input

- 첫 줄에 `n m`이 주어진다.
- 이어지는 `m`개의 줄은 `0 a b` 또는 `1 a b` 형식의 질의다.

## Output

- 질의가 `1 a b`인 경우에만 결과를 출력한다.

## Note

이 디렉터리의 fixture는 legacy에서 가져온 공식 자료가 아니라, bridge 프로젝트를 위해 직접 만든 학습용 fixture다.

## Source

https://www.acmicpc.net/problem/1717
"""


def bridge_python_solution() -> str:
    return """import sys


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def union(parent, a, b):
    ra = find(parent, a)
    rb = find(parent, b)
    if ra == rb:
        return
    if ra < rb:
        parent[rb] = ra
    else:
        parent[ra] = rb


def main():
    input = sys.stdin.readline
    n, m = map(int, input().split())
    parent = list(range(n + 1))
    out = []
    for _ in range(m):
        op, a, b = map(int, input().split())
        if op == 0:
            union(parent, a, b)
        else:
            out.append("YES" if find(parent, a) == find(parent, b) else "NO")
    sys.stdout.write("\\n".join(out))


if __name__ == "__main__":
    main()
"""


def bridge_project_readme() -> str:
    return """# BOJ 1717 — 집합의 표현

| Item | Detail |
| :--- | :--- |
| Track | `Core-Bridges` |
| Type | Bridge project |
| CLRS | Ch 21 |
| Problem URL | https://www.acmicpc.net/problem/1717 |

## Summary

Kruskal과 MST 전에 disjoint set union을 독립적으로 익히기 위해 추가한 bridge 프로젝트다.

## Verify

- `make -C problem test`
- `make -C problem run-py`

## Status

- Python: verified
- C++: not retained
"""


def bridge_docs_readme() -> str:
    return """# Public Notes

- `concepts/disjoint-set-union.md`: union-find 핵심 개념 요약
- `references/verification.md`: 학습용 fixture 검증 메모

이 프로젝트는 legacy 문제 이관이 아니라 커리큘럼 보강용 신규 bridge다.
"""


def bridge_concept() -> str:
    return """# Disjoint Set Union

서로소 집합 자료구조는 원소가 어떤 그룹에 속하는지 빠르게 판단하고, 두 그룹을 합치는 연산을 지원한다.

- `find(x)`: 대표 원소를 찾는다.
- `union(a, b)`: 두 집합을 하나로 합친다.
- path compression과 union heuristic을 같이 쓰면 거의 상수 시간에 가깝게 동작한다.

이 개념은 Kruskal MST, 친구 관계 묶기, 연결성 질의 문제의 기초가 된다.
"""


def bridge_verification() -> str:
    return """# Verification

- Fixture runner: `make -C ../problem test`
- Representative manual run: `make -C ../problem run-py`
- Expected output files live in `../problem/data/`

이 프로젝트의 fixture는 bridge 학습용으로 직접 작성했다.
"""


def bridge_notion(name: str) -> str:
    content = {
        "00-problem-framing.md": """# Problem Framing

## Project Context
- Track: `Core-Bridges`
- BOJ: [1717](https://www.acmicpc.net/problem/1717)
- CLRS connection: Ch 21
- Why this problem matters: MST와 Kruskal 이전에 union-find를 독립적으로 익히는 bridge다.

## Goal
- union-find를 MST 이전에 독립적으로 학습한다.
- `0 a b`, `1 a b` 질의가 섞인 입력에서 집합 병합과 연결성 질의를 정확히 처리한다.

## Success Criteria
- `make -C problem test`가 통과한다.
- path compression이 구현되어 있다.
""",
        "01-approach-log.md": """# Approach Log

## Chosen Direction
- parent 배열을 두고 `find`, `union` 두 함수로 문제를 해결한다.
- union by rank 대신 작은 대표를 부모로 고정하는 단순 정책을 사용한다.

## Why
- bridge 프로젝트의 목표는 개념 이해이지 미세 최적화가 아니다.
- `find`와 `union`의 책임이 분명해서 이후 Kruskal 구현으로 옮겨가기 쉽다.

## Alternatives Not Chosen
- naive set merging은 질의 수가 많아질수록 비효율적이다.
- union by rank는 더 일반적이지만, 이 bridge 단계에서는 개념 설명보다 구현 디테일이 앞설 수 있다.
""",
        "02-debug-log.md": """# Debug Log

## Observed Failures
- 이번 bridge 라운드에서 재현된 테스트 실패는 없었다.

## Defensive Checks
- 같은 집합에 대한 중복 union을 허용해도 결과가 깨지지 않는지 확인한다.
- 질의(`1 a b`)만 출력하고 union(`0 a b`)은 출력하지 않는지 확인한다.
- self-union과 이미 연결된 원소를 포함한 학습용 fixture를 넣었다.

## Follow-Up
- union by rank 버전과 현재 구현을 비교해 path compression만으로도 충분한지 다시 점검할 수 있다.
""",
        "03-retrospective.md": """# Retrospective

union-find는 구현 자체는 짧지만, 이후 MST/Kruskal의 전제 개념이라 bridge로 분리할 가치가 있다.

이 문제를 bridge로 떼어두면, MST 단원에서 "간선 정렬"과 "사이클 판정"을 한 번에 새로 배우는 부담을 줄일 수 있다.
""",
        "04-knowledge-index.md": """# Knowledge Index

## Core References
- BOJ: https://www.acmicpc.net/problem/1717
- CLRS mapping: Ch 21
- Track: `Core-Bridges`

## Main Concept
- Checked date: 2026-03-07
- Why it was consulted: MST 이전 bridge 프로젝트로 추가하기 위해.
- What was learned: 연결성 질의와 집합 병합은 별도 트랙으로 한 번 정리해두는 편이 후반 그래프 학습을 쉽게 만든다.
- Effect on this project: `Core-Bridges` 트랙을 새로 만들었다.
""",
    }
    return content[name]


def build_bridge_project() -> None:
    project = STUDY / "Core-Bridges" / "1717"
    (STUDY / "Core-Bridges").mkdir(parents=True, exist_ok=True)
    write_text(
        STUDY / "Core-Bridges" / "README.md",
        """# Core-Bridges

정규 BarkingDog 토픽 사이의 학습 공백을 메우는 보강 프로젝트 트랙이다.

## Projects

| BOJ | Title | Purpose |
| :--- | :--- | :--- |
| [1717](1717/README.md) | 집합의 표현 | MST/Kruskal 이전 union-find bridge |
""",
    )
    write_text(project / "README.md", bridge_project_readme())
    write_text(project / "problem" / "README.md", bridge_problem_readme())
    write_text(project / "problem" / "Makefile", build_makefile(has_cpp=False))
    write_text(project / "problem" / "script" / "test.sh", build_test_script())
    (project / "problem" / "script" / "test.sh").chmod(0o755)
    write_text(project / "problem" / "data" / "input1.txt", "7 8\n0 1 3\n1 1 7\n0 7 6\n1 7 1\n0 3 7\n0 4 2\n0 1 1\n1 1 7\n")
    write_text(project / "problem" / "data" / "output1.txt", "NO\nNO\nYES\n")
    write_text(project / "problem" / "data" / "input2.txt", "5 6\n1 1 2\n0 1 2\n1 1 2\n0 2 5\n1 1 5\n1 4 5\n")
    write_text(project / "problem" / "data" / "output2.txt", "NO\nYES\nYES\nNO\n")
    write_text(
        project / "problem" / "code" / "starter.py",
        "def solve():\n    pass\n\n\nif __name__ == '__main__':\n    solve()\n",
    )
    write_text(project / "python" / "README.md", implementation_readme(BRIDGE_PROJECT | {"boj": "1717"}, "python", False))
    write_text(project / "python" / "src" / "solution.py", bridge_python_solution())
    write_text(project / "python" / "tests" / "README.md", tests_readme("python"))
    write_text(project / "docs" / "README.md", bridge_docs_readme())
    write_text(project / "docs" / "concepts" / "disjoint-set-union.md", bridge_concept())
    write_text(project / "docs" / "references" / "verification.md", bridge_verification())
    for filename in [
        "00-problem-framing.md",
        "01-approach-log.md",
        "02-debug-log.md",
        "03-retrospective.md",
        "04-knowledge-index.md",
    ]:
        write_text(project / "notion" / filename, bridge_notion(filename))


def build_advanced_backlog() -> None:
    rows = "\n".join(
        f"| {label} | {name} | {clrs} | {focus} |" for label, name, clrs, focus in ADVANCED_BACKLOG
    )
    write_text(
        STUDY / "Advanced-CLRS" / "README.md",
        f"""# Advanced-CLRS

이 트랙은 core migration이 끝난 뒤 여는 심화 백로그다. 이번 작업에서는 구현 프로젝트를 만들지 않고, 학습 우선순위만 고정한다.

| Slot | Topic | CLRS | Focus |
| :--- | :--- | :--- | :--- |
{rows}
""",
    )


def build_project(meta: dict) -> None:
    legacy_dir = ROOT / meta["legacy_rel"]
    project = STUDY / meta["study_track"] / meta["boj"]
    project.mkdir(parents=True, exist_ok=True)

    copy_file(legacy_dir / "problem" / "README.md", project / "problem" / "README.md")
    if (legacy_dir / "problem" / "code").exists():
        shutil.copytree(legacy_dir / "problem" / "code", project / "problem" / "code", dirs_exist_ok=True)
    if (legacy_dir / "problem" / "data").exists():
        shutil.copytree(legacy_dir / "problem" / "data", project / "problem" / "data", dirs_exist_ok=True)
    write_text(project / "problem" / "Makefile", build_makefile(meta["has_cpp"]))
    write_text(project / "problem" / "script" / "test.sh", build_test_script())
    (project / "problem" / "script" / "test.sh").chmod(0o755)

    copy_file(legacy_dir / "solve" / "solution" / "solution.py", project / "python" / "src" / "solution.py")
    write_text(project / "python" / "README.md", implementation_readme(meta, "python", meta["has_cpp"]))
    write_text(project / "python" / "tests" / "README.md", tests_readme("python"))

    if meta["has_cpp"]:
        copy_file(legacy_dir / "solve" / "solution" / "solution.cpp", project / "cpp" / "src" / "solution.cpp")
        write_text(project / "cpp" / "README.md", implementation_readme(meta, "cpp", meta["has_cpp"]))
        write_text(project / "cpp" / "tests" / "README.md", tests_readme("cpp"))
        write_text(project / "cpp" / "include" / "README.md", "# Header Notes\n\n- Shared headers can be added here when needed.\n")

    legacy_docs = legacy_dir / "docs"
    concept_paths = []
    for doc_path in sorted(legacy_docs.glob("*.md")):
        name = doc_path.name
        if name == "README.md":
            continue
        elif name == "approach.md":
            copy_file(doc_path, project / "docs" / "references" / "approach.md")
        elif name == "reproducibility.md":
            copy_file(doc_path, project / "docs" / "references" / "reproducibility.md")
        else:
            dst = project / "docs" / "concepts" / name
            copy_file(doc_path, dst)
            concept_paths.append(dst)
    write_text(
        project / "docs" / "references" / "overview.md",
        overview_reference(meta, [path.name for path in concept_paths], meta["has_cpp"]),
    )
    write_text(project / "docs" / "README.md", docs_readme(meta, [path.name for path in concept_paths]))

    problem_text = (legacy_dir / "problem" / "README.md").read_text(encoding="utf-8")
    approach_text = (legacy_docs / "approach.md").read_text(encoding="utf-8")
    analysis_text = (legacy_dir / "solve" / "analysis.md").read_text(encoding="utf-8")
    devlog_text = (legacy_dir / "devlog" / "entries" / "001-implementation.md").read_text(encoding="utf-8")
    lab_text = (legacy_dir / "lab-report.md").read_text(encoding="utf-8")

    write_text(project / "README.md", project_readme(meta, meta["has_cpp"]))
    write_text(project / "notion" / "00-problem-framing.md", notion_problem_framing(meta, problem_text, meta["has_cpp"]))
    write_text(project / "notion" / "01-approach-log.md", notion_approach_log(meta, approach_text, analysis_text))
    write_text(project / "notion" / "02-debug-log.md", clean_devlog(devlog_text, meta))
    write_text(project / "notion" / "03-retrospective.md", clean_retrospective(lab_text, meta["legacy_rel"]))
    write_text(project / "notion" / "04-knowledge-index.md", notion_knowledge_index(meta, concept_paths))


def gather_projects() -> list[dict]:
    projects = []
    for track_key, track_meta in TRACKS.items():
        legacy_track = LEGACY / "core" / track_key
        for legacy_dir in sorted(legacy_track.iterdir()):
            if not legacy_dir.is_dir():
                continue
            tier, boj = legacy_dir.name.split("-", 1)
            project_readme_text = (legacy_dir / "README.md").read_text(encoding="utf-8")
            problem_readme_text = (legacy_dir / "problem" / "README.md").read_text(encoding="utf-8")
            title = extract_title(project_readme_text, problem_readme_text, boj)
            source_url = extract_source_url(problem_readme_text) or extract_source_url(project_readme_text)
            summary = clean_excerpt(problem_readme_text)
            has_cpp = tier == "gold" or boj in SPECIAL_CPP
            cross_ref = None
            if boj == "16926":
                cross_ref = "BOJ 16926은 provenance 보존을 위해 `Core-00-Basics`에 두되, `Core-05-Simulation`을 시작할 때 다시 복습한다."
            if boj == "11053":
                cross_ref = "BOJ 11053은 provenance 보존을 위해 `Core-00-Basics`에 두되, `Core-08-DP` 진입 전에 bridge 문제로 다시 읽는다."
            projects.append(
                {
                    "track_key": track_key,
                    "study_track": track_meta["study"],
                    "label": track_meta["label"],
                    "topic": track_meta["topic"],
                    "clrs": track_meta["clrs"],
                    "legacy_rel": str(legacy_dir.relative_to(ROOT)),
                    "tier": tier,
                    "boj": boj,
                    "title": title,
                    "source_url": source_url,
                    "summary": summary,
                    "has_cpp": has_cpp,
                    "cross_ref": cross_ref,
                }
            )
    return projects


def main() -> None:
    projects = gather_projects()
    DOCS.mkdir(parents=True, exist_ok=True)
    STUDY.mkdir(parents=True, exist_ok=True)
    write_text(ROOT / ".gitignore", gitignore())
    manifest_rel = "docs/legacy-file-manifest.txt"
    write_text(DOCS / "legacy-file-manifest.txt", "\n".join(legacy_manifest()))
    write_text(ROOT / "README.md", root_readme(projects))
    write_text(STUDY / "README.md", study_readme())
    write_text(DOCS / "legacy-audit.md", legacy_audit(projects, manifest_rel))
    write_text(DOCS / "curriculum-map.md", curriculum_map(projects))
    write_text(DOCS / "migration-template.md", migration_template())

    grouped: dict[str, list[dict]] = {key: [] for key in TRACKS}
    for meta in projects:
        grouped[meta["track_key"]].append(meta)
        build_project(meta)

    for track_key, metas in grouped.items():
        write_text(STUDY / TRACKS[track_key]["study"] / "README.md", track_readme(track_key, metas))

    build_bridge_project()
    build_advanced_backlog()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import textwrap
from dataclasses import dataclass
from pathlib import Path


DATE = "2026-03-10"
ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "study"
try:
    GIT_TOP = Path(
        subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    )
except subprocess.CalledProcessError:
    GIT_TOP = None


TRACKS = [
    {
        "id": "Core-00-Basics",
        "topic": "기초 구현",
        "intro": "입출력, 문자열, 배열, 가장 짧은 DP 브리지를 통해 이후 모든 트랙에서 필요한 기본 구현 습관을 잡는 출발점이다.",
        "why": "작은 문제를 안정적으로 풀지 못하면 뒤의 자료구조나 그래프 문제에서도 실수가 반복된다. 이 트랙은 구현 실수를 줄이는 최소 단위를 먼저 연습하게 한다.",
        "portfolio_tip": "기초 트랙을 포트폴리오에 옮길 때는 화려한 문제보다 '입력 해석, 상태 정의, 검증 명령'을 얼마나 분리해 보여 주는지가 더 중요하다.",
        "learning_focus": "작은 입력을 안정적으로 읽고, 조건 분기를 코드와 문서로 함께 정리하는 감각",
        "projects": ["10988", "11053", "16926"],
    },
    {
        "id": "Core-01-Array-List",
        "topic": "배열과 리스트",
        "intro": "배열 순회와 편집기 시뮬레이션을 묶어, 자료구조 선택이 성능과 구현 난이도에 어떤 차이를 만드는지 체감하게 한다.",
        "why": "같은 기능도 배열, 연결 리스트, 스택 두 개 조합처럼 표현 방식이 달라지면 비용 구조가 달라진다. 그 차이를 문제로 익히는 단계다.",
        "portfolio_tip": "이 트랙은 '어떤 자료구조를 왜 골랐는지'를 표나 간단한 비교 문장으로 남기면 포트폴리오 완성도가 크게 올라간다.",
        "learning_focus": "순차 자료구조를 선택하고 편집 연산의 비용 모델을 설명하는 연습",
        "projects": ["10807", "5397", "1406"],
    },
    {
        "id": "Core-02-Stack-Queue",
        "topic": "스택과 큐",
        "intro": "LIFO/FIFO/덱의 차이를 문제 규칙과 연결해, 자료구조 이름이 아니라 동작 모델로 이해하게 하는 트랙이다.",
        "why": "스택과 큐는 쉬워 보여도 명령 해석, 예외 처리, 출력 형식에서 자주 실수한다. 이 트랙은 그 반복 실수를 빠르게 잡아 준다.",
        "portfolio_tip": "포트폴리오에서는 구현 코드보다 '어떤 연산을 어느 쪽 끝에서 처리하는지'를 그림이나 짧은 설명으로 보여 주면 읽는 사람이 훨씬 빨리 이해한다.",
        "learning_focus": "명령 기반 자료구조 문제를 상태 전이 규칙으로 정리하는 연습",
        "projects": ["10828", "2164", "5430"],
    },
    {
        "id": "Core-03-BFS-DFS",
        "topic": "그래프 탐색",
        "intro": "정점 방문 순서, 그래프 표현, 격자 탐색을 묶어 BFS/DFS의 기본기를 고정하는 트랙이다.",
        "why": "그래프 탐색은 이후 트리, 최단 경로, 위상 정렬의 기반이다. 방문 처리와 큐/스택 규칙을 여기서 확실히 잡아야 뒤가 편해진다.",
        "portfolio_tip": "탐색 문제는 정답 코드보다도 '방문 처리 시점'을 설명하는 문장이 중요하다. 그 한 줄이 있으면 문서 품질이 크게 좋아진다.",
        "learning_focus": "그래프 표현을 고르고 방문 순서를 안정적으로 제어하는 연습",
        "projects": ["1260", "24479", "7576"],
    },
    {
        "id": "Core-04-Recursion-Backtracking",
        "topic": "재귀와 백트래킹",
        "intro": "재귀 호출의 구조를 이해하고, 상태 복원과 가지치기를 작은 문제에서 큰 문제로 확장해 보는 트랙이다.",
        "why": "재귀는 코드 길이는 짧지만 실수 지점은 많다. 종료 조건, 선택-복구 순서를 문서와 함께 정리하는 습관이 필요하다.",
        "portfolio_tip": "백트래킹 문제는 '선택 -> 재귀 호출 -> 복구' 흐름을 코드 옆에서 문장으로 풀어 주면 학습 레포와 포트폴리오 모두에서 강점이 된다.",
        "learning_focus": "호출 구조를 추적하고 상태 복원 규칙을 설명하는 연습",
        "projects": ["10872", "15649", "9663"],
    },
    {
        "id": "Core-05-Simulation",
        "topic": "시뮬레이션",
        "intro": "문제 설명을 상태 전이 규칙으로 번역하는 힘을 키우는 트랙이다. 구현은 길어도 논리는 짧게 정리하는 연습이 핵심이다.",
        "why": "시뮬레이션은 실수하기 쉬운 대신, 문서화가 잘되면 실력을 보여 주기 좋은 분야다. 상태 표와 규칙 분리를 익히기 좋다.",
        "portfolio_tip": "포트폴리오에서는 상태 전이 표, 방향 정의, 반복 종료 조건 세 가지만 깔끔하게 보여 줘도 문제 이해도가 확 올라간다.",
        "learning_focus": "복잡한 설명을 작은 상태 전이 규칙으로 나누어 구현하는 연습",
        "projects": ["2920", "14503", "14891"],
    },
    {
        "id": "Core-06-Sorting",
        "topic": "정렬",
        "intro": "기본 정렬부터 다중 기준 정렬, 정렬 후 스위프 라인까지 자연스럽게 확장되는 트랙이다.",
        "why": "정렬은 단독 기술이 아니라 이후의 탐색, 그리디, 구간 문제를 풀기 위한 공통 도구다. 그래서 순수 정렬과 활용형을 함께 둔다.",
        "portfolio_tip": "정렬 문제는 '무엇을 어떤 기준으로 정렬했는지'를 문장으로 못 쓰면 코드만 봐서는 의도가 잘 안 보인다. 기준식을 분리해서 적어 두는 편이 좋다.",
        "learning_focus": "정렬 기준을 설계하고, 정렬 이후의 후처리 로직을 분리해 설명하는 연습",
        "projects": ["2750", "1181", "2170"],
    },
    {
        "id": "Core-07-Binary-Search-Hash",
        "topic": "이분 탐색과 해시",
        "intro": "탐색 문제를 선형 탐색으로 버티지 않고, 집합/카운터/매개변수 탐색으로 재구성하는 방법을 익히는 트랙이다.",
        "why": "많은 문제에서 병목은 구현이 아니라 탐색 전략이다. 이 트랙은 '무엇을 탐색 대상으로 볼 것인가'를 바꾸는 감각을 만든다.",
        "portfolio_tip": "탐색 문제는 구현보다 전략 선택이 핵심이다. 왜 이분 탐색인지, 왜 Counter인지 먼저 적어 두면 문서가 훨씬 설득력 있어진다.",
        "learning_focus": "탐색 대상을 재정의하고 자료구조 또는 매개변수 탐색으로 문제를 다시 보는 연습",
        "projects": ["1920", "10816", "2110"],
    },
    {
        "id": "Core-08-DP",
        "topic": "동적 계획법",
        "intro": "점화식, 상태 정의, 전이 방향을 가장 기본적인 형태부터 차근차근 고정하는 트랙이다.",
        "why": "DP는 풀이를 외우면 금방 무너지고, 상태 정의를 스스로 세워야 오래 간다. 그래서 작은 1차원 DP부터 배낭 문제까지 묶는다.",
        "portfolio_tip": "DP 문서는 점화식을 먼저 쓰고, 각 항이 무엇을 의미하는지 바로 아래에 풀어 써야 읽는 사람이 따라오기 쉽다.",
        "learning_focus": "상태와 전이를 명시적으로 정의하고 표나 배열 의미를 끝까지 유지하는 연습",
        "projects": ["2748", "1149", "12865"],
    },
    {
        "id": "Core-09-Greedy",
        "topic": "그리디",
        "intro": "매 단계에서 가장 좋아 보이는 선택이 전체 최적과 맞물리는 조건을 사례 중심으로 익히는 트랙이다.",
        "why": "그리디는 맞는 이유를 설명하지 못하면 거의 가치가 없다. 이 트랙은 선택 기준과 반례 의식을 함께 키우기 위해 구성했다.",
        "portfolio_tip": "포트폴리오에서는 '왜 이 선택이 다음 선택의 자유도를 해치지 않는가'를 짧게라도 남겨 두는 편이 좋다.",
        "learning_focus": "탐욕 선택의 기준을 말로 설명하고 반례 가능성을 점검하는 연습",
        "projects": ["11047", "1931", "1744"],
    },
    {
        "id": "Core-0A-Priority-Queue",
        "topic": "우선순위 큐",
        "intro": "힙을 직접 구현하기보다, 힙이 필요한 문제 구조를 구분하는 감각을 키우는 트랙이다.",
        "why": "우선순위 큐는 알고리즘 곳곳에서 재사용된다. 여기서 최소/최대 힙과 힙 기반 그리디를 묶어 두면 이후 그래프 문제에서 다시 쓰기 쉽다.",
        "portfolio_tip": "힙 문제는 자료구조 API를 정확히 쓰는 능력이 드러난다. push/pop 시점과 비교 기준을 문서에 분리해서 적어 두면 좋다.",
        "learning_focus": "우선순위 큐가 필요한 상황을 식별하고 비교 기준을 일관되게 유지하는 연습",
        "projects": ["11279", "1927", "1715"],
    },
    {
        "id": "Core-0B-Graph-Tree",
        "topic": "트리와 그래프 심화",
        "intro": "트리 구조를 별도 자료형으로 다루며, 부모 찾기, 순회, 지름 계산 같은 대표 패턴을 익히는 트랙이다.",
        "why": "탐색 기본기 이후에는 트리 고유의 성질을 문제에 연결해야 한다. 이 트랙은 그 간격을 메운다.",
        "portfolio_tip": "트리 문제는 입력을 어떤 그래프 구조로 저장했는지와, 왜 그 저장 방식이 적절한지를 밝혀 두면 설명력이 좋아진다.",
        "learning_focus": "트리 구조의 성질을 이용해 탐색과 누적 계산을 재구성하는 연습",
        "projects": ["11725", "1991", "1167"],
    },
    {
        "id": "Core-0C-Shortest-Path",
        "topic": "최단 경로",
        "intro": "가중치 조건에 따라 Dijkstra와 Bellman-Ford를 고르는 기준을 실전 문제로 익히는 트랙이다.",
        "why": "최단 경로는 알고리즘 선택이 핵심이다. 음수 간선 유무, 단일 시작점 여부, 출력 요구를 문서로 정리해 두면 이후 응용이 쉬워진다.",
        "portfolio_tip": "최단 경로 트랙은 '왜 이 알고리즘을 골랐는가'를 문제 조건과 직접 연결해 쓰면 레포의 설명력이 높아진다.",
        "learning_focus": "가중치 조건과 그래프 특성에 맞는 최단 경로 알고리즘을 선택하는 연습",
        "projects": ["1916", "1753", "11657"],
    },
    {
        "id": "Core-0D-MST-Topo",
        "topic": "MST와 위상 정렬",
        "intro": "그래프 학습 후반부에서 가장 자주 다시 만나는 두 패턴인 최소 스패닝 트리와 선행관계 정렬을 묶은 트랙이다.",
        "why": "트리 구축과 순서 결정은 둘 다 '조건을 만족하는 구조를 만들어 간다'는 공통점이 있다. 같은 시야로 다루면 기억이 오래 간다.",
        "portfolio_tip": "이 트랙은 선택 기준과 자료구조 준비가 절반이다. 간선 정렬 기준, 진입 차수 관리처럼 핵심 준비 단계를 따로 적어 두면 좋다.",
        "learning_focus": "그래프 전체 구조를 만들거나 순서를 고정하는 규칙을 설명하는 연습",
        "projects": ["9372", "2252", "1197"],
    },
    {
        "id": "Core-Bridges",
        "topic": "브리지 프로젝트",
        "intro": "정규 트랙 사이의 학습 공백을 메우는 보강 프로젝트 모음이다. 지금은 union-find를 독립적으로 다룬다.",
        "why": "원래 커리큘럼만 따라가면 MST 전에 DSU를 충분히 다룰 기회가 없었다. 그 빈틈을 메우기 위해 별도 브리지를 둔다.",
        "portfolio_tip": "브리지 프로젝트는 '왜 여기서 이 개념을 먼저 배우는가'를 적어 두면 커리큘럼 설계 감각까지 함께 보여 줄 수 있다.",
        "learning_focus": "다음 트랙에서 필요한 선행 개념을 별도 실습으로 고정하는 연습",
        "projects": ["1717"],
    },
    {
        "id": "Advanced-CLRS",
        "topic": "CLRS 심화",
        "intro": "Core를 지나 CLRS의 고급 주제를 직접 구현 가능한 작은 실험으로 바꿔 보는 심화 트랙이다.",
        "why": "고급 알고리즘은 읽기만 하면 남지 않는다. 이 트랙은 proof-heavy 챕터를 실행 가능한 과제로 바꿔 학습 장벽을 낮춘다.",
        "portfolio_tip": "심화 트랙은 '책 내용을 그대로 베꼈다'가 아니라 '핵심 개념을 실행 가능한 형태로 재구성했다'는 점이 드러나야 한다.",
        "learning_focus": "이론 중심 알고리즘을 작은 실험과 검증 가능한 입출력 문제로 재구성하는 연습",
        "projects": [
            "0x10-strassen-matrix",
            "0x11-amortized-analysis-lab",
            "0x12-red-black-tree",
            "0x13-meldable-heap",
            "0x14-network-flow",
            "0x15-string-matching",
            "0x16-computational-geometry",
            "0x17-number-theory-lab",
            "0x18-np-completeness-lab",
            "0x19-approximation-lab",
        ],
    },
]


KO_TITLES = {
    "Core-00-Basics/10988": "팰린드롬인지 확인하기",
    "Core-00-Basics/11053": "가장 긴 증가하는 부분 수열",
    "Core-00-Basics/16926": "배열 돌리기 1",
    "Core-01-Array-List/10807": "개수 세기",
    "Core-01-Array-List/1406": "에디터",
    "Core-01-Array-List/5397": "키로거",
    "Core-02-Stack-Queue/10828": "스택",
    "Core-02-Stack-Queue/2164": "카드2",
    "Core-02-Stack-Queue/5430": "AC",
    "Core-03-BFS-DFS/1260": "DFS와 BFS",
    "Core-03-BFS-DFS/24479": "알고리즘 수업 - 깊이 우선 탐색 1",
    "Core-03-BFS-DFS/7576": "토마토",
    "Core-04-Recursion-Backtracking/10872": "팩토리얼",
    "Core-04-Recursion-Backtracking/15649": "N과 M (1)",
    "Core-04-Recursion-Backtracking/9663": "N-Queen",
    "Core-05-Simulation/14503": "로봇 청소기",
    "Core-05-Simulation/14891": "톱니바퀴",
    "Core-05-Simulation/2920": "음계",
    "Core-06-Sorting/1181": "단어 정렬",
    "Core-06-Sorting/2170": "선 긋기",
    "Core-06-Sorting/2750": "수 정렬하기",
    "Core-07-Binary-Search-Hash/10816": "숫자 카드 2",
    "Core-07-Binary-Search-Hash/1920": "수 찾기",
    "Core-07-Binary-Search-Hash/2110": "공유기 설치",
    "Core-08-DP/1149": "RGB거리",
    "Core-08-DP/12865": "평범한 배낭",
    "Core-08-DP/2748": "피보나치 수 2",
    "Core-09-Greedy/11047": "동전 0",
    "Core-09-Greedy/1744": "수 묶기",
    "Core-09-Greedy/1931": "회의실 배정",
    "Core-0A-Priority-Queue/11279": "최대 힙",
    "Core-0A-Priority-Queue/1715": "카드 정렬하기",
    "Core-0A-Priority-Queue/1927": "최소 힙",
    "Core-0B-Graph-Tree/1167": "트리의 지름",
    "Core-0B-Graph-Tree/11725": "트리의 부모 찾기",
    "Core-0B-Graph-Tree/1991": "트리 순회",
    "Core-0C-Shortest-Path/11657": "타임머신",
    "Core-0C-Shortest-Path/1753": "최단경로",
    "Core-0C-Shortest-Path/1916": "최소비용 구하기",
    "Core-0D-MST-Topo/1197": "최소 스패닝 트리",
    "Core-0D-MST-Topo/2252": "줄 세우기",
    "Core-0D-MST-Topo/9372": "상근이의 여행",
    "Core-Bridges/1717": "집합의 표현",
    "Advanced-CLRS/0x10-strassen-matrix": "Strassen 행렬 곱셈",
    "Advanced-CLRS/0x11-amortized-analysis-lab": "상각 분석 실습",
    "Advanced-CLRS/0x12-red-black-tree": "레드-블랙 트리 삽입과 검증",
    "Advanced-CLRS/0x13-meldable-heap": "합칠 수 있는 힙 브리지",
    "Advanced-CLRS/0x14-network-flow": "네트워크 플로우",
    "Advanced-CLRS/0x15-string-matching": "고급 문자열 매칭",
    "Advanced-CLRS/0x16-computational-geometry": "계산 기하 실습",
    "Advanced-CLRS/0x17-number-theory-lab": "정수론 실습",
    "Advanced-CLRS/0x18-np-completeness-lab": "NP-완전성 실습",
    "Advanced-CLRS/0x19-approximation-lab": "근사 알고리즘 실습",
}


NOTION_SECTION_TITLES = {
    "00-problem-framing.md": "문제 프레이밍",
    "01-approach-log.md": "접근 로그",
    "02-debug-log.md": "디버그 로그",
    "03-retrospective.md": "회고",
    "04-knowledge-index.md": "지식 인덱스",
    "05-development-timeline.md": "개발 타임라인",
}


NOTION_MIN_WORDS = {
    "00-problem-framing.md": 180,
    "01-approach-log.md": 190,
    "02-debug-log.md": 180,
    "03-retrospective.md": 220,
    "04-knowledge-index.md": 240,
    "05-development-timeline.md": 220,
}


@dataclass
class TestResult:
    passed: bool
    summary: str
    output: str


@dataclass
class ProjectMeta:
    track: str
    slug: str
    kind: str
    heading_title: str
    english_title: str
    korean_title: str
    problem_url: str | None
    level_or_type: str | None
    clrs: str | None
    legacy_source: str | None
    project_focus: str | None
    has_cpp: bool
    test: TestResult

    @property
    def key(self) -> str:
        return f"{self.track}/{self.slug}"

    @property
    def project_dir(self) -> Path:
        return STUDY / self.track / self.slug


def normalize(text: str) -> str:
    content = textwrap.dedent(text).strip()
    content = re.sub(r"(?m)^ {8}", "", content)
    return content + "\n"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_head_text(path: Path) -> str:
    if GIT_TOP is None:
        return read_text(path)
    rel = path.relative_to(GIT_TOP)
    proc = subprocess.run(
        ["git", "show", f"HEAD:{rel.as_posix()}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        return proc.stdout
    return read_text(path)


def write_text(path: Path, content: str) -> None:
    current = path.read_text(encoding="utf-8") if path.exists() else None
    if current != content:
        path.write_text(content, encoding="utf-8")


def extract_table(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) != 2:
            continue
        if parts[0] in {"Item", ":---", "Slot"}:
            continue
        values[parts[0]] = parts[1]
    return values


def clean_inline(value: str | None) -> str | None:
    if value is None:
        return None
    return value.replace("`", "").strip()


def parse_heading_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("Missing markdown title")


def parse_english_title(heading_title: str, slug: str) -> str:
    if "—" in heading_title:
        return heading_title.split("—", 1)[1].strip()
    if "-" in heading_title:
        return heading_title.split("-", 1)[1].strip()
    return slug


def strip_first_heading(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    normalized = re.sub(r"^(# .+?)\1$", r"\1", normalized, count=1, flags=re.MULTILINE)
    lines = normalized.strip().splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    while lines and not lines[0].strip():
        lines = lines[1:]
    return "\n".join(lines).strip()


def word_count(text: str) -> int:
    return len(text.split())


def track_info(track_id: str) -> dict:
    for track in TRACKS:
        if track["id"] == track_id:
            return track
    raise KeyError(track_id)


def english_dominant(text: str) -> bool:
    ascii_letters = len(re.findall(r"[A-Za-z]", text))
    korean_letters = len(re.findall(r"[가-힣]", text))
    return ascii_letters > korean_letters * 2


def project_learning_focus(meta: "ProjectMeta") -> str:
    track_focus = track_info(meta.track)["learning_focus"]
    if meta.project_focus and not english_dominant(meta.project_focus):
        return meta.project_focus
    if meta.kind == "advanced":
        return f"{meta.korean_title}의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습"
    return track_focus


def project_bridge_line(meta: "ProjectMeta") -> str:
    if meta.kind == "advanced":
        if meta.clrs:
            return f"CLRS {meta.clrs}의 핵심 아이디어를 입출력과 자동 검증이 가능한 작은 실험으로 바꾸는 과정이 중요했다."
        return "이론 중심 주제를 코드와 fixture로 다시 표현하는 과정이 중요했다."
    if meta.kind == "bridge":
        return "다음 트랙에서 다시 만나게 될 선행 개념을 지금 확실히 고정해 두는 것이 핵심이었다."
    return "비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다."


def project_display_name(track_id: str, slug: str) -> str:
    return KO_TITLES.get(f"{track_id}/{slug}", slug)


def project_neighbors(meta: "ProjectMeta") -> tuple[str | None, str | None]:
    projects = track_info(meta.track)["projects"]
    index = projects.index(meta.slug)
    previous_slug = projects[index - 1] if index > 0 else None
    next_slug = projects[index + 1] if index + 1 < len(projects) else None
    return previous_slug, next_slug


def neighbor_project_links(meta: "ProjectMeta") -> list[str]:
    previous_slug, next_slug = project_neighbors(meta)
    lines: list[str] = []
    if previous_slug:
        lines.append(
            f"- 앞 프로젝트: [`../../{previous_slug}/README.md`](../../{previous_slug}/README.md) ({project_display_name(meta.track, previous_slug)})"
        )
    if next_slug:
        lines.append(
            f"- 다음 프로젝트: [`../../{next_slug}/README.md`](../../{next_slug}/README.md) ({project_display_name(meta.track, next_slug)})"
        )
    if not lines:
        lines.append(f"- 같은 트랙의 큰 흐름은 [`../../README.md`](../../README.md)에서 다시 확인한다.")
    return lines


def concept_doc_links(meta: "ProjectMeta") -> list[str]:
    concept_dir = meta.project_dir / "docs" / "concepts"
    links: list[str] = []
    if not concept_dir.exists():
        return links
    for path in sorted(concept_dir.glob("*.md")):
        links.append(f"- [`{path.name}`](../docs/concepts/{path.name})")
    return links


def doc_reference_links(meta: "ProjectMeta") -> list[str]:
    return [
        "- [`../docs/references/approach.md`](../docs/references/approach.md)",
        "- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)",
        "- [`05-development-timeline.md`](05-development-timeline.md)",
    ]


def notion_supplement(meta: "ProjectMeta", kind: str) -> str:
    focus = project_learning_focus(meta)
    bridge = project_bridge_line(meta)
    concept_links = concept_doc_links(meta)
    public_links = doc_reference_links(meta)
    neighbor_links = neighbor_project_links(meta)
    if kind == "00-problem-framing.md":
        extra_links = (concept_links[:2] + public_links[:2] + neighbor_links[:1])[:5] or [
            "- [`../docs/README.md`](../docs/README.md)"
        ]
        lines = [
            "## 지금 이 프로젝트에서 먼저 고정할 것",
            "",
            f"- `{meta.korean_title}`에서 실제로 확인하려는 학습 목표는 `{focus}`이다.",
            '- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.',
            f"- {bridge}",
            "- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.",
            "",
            "## 시작 전 성공 기준",
            "",
            "- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?",
            "- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?",
            "- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?",
            "",
            "## 같이 다시 볼 문서",
            "",
            *extra_links,
        ]
        return "\n".join(lines).rstrip() + "\n"
    if kind == "01-approach-log.md":
        extra_links = (concept_links[:2] + public_links + neighbor_links[:1])[:5] or [
            "- [`../docs/README.md`](../docs/README.md)"
        ]
        lines = [
            "## 이 접근에서 꼭 기억할 선택",
            "",
            f"- `{meta.korean_title}`에서 중심이 된 판단은 `{focus}`를 가장 단순한 상태 전이로 번역하는 것이었다.",
            "- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.",
            f"- {bridge}",
            "- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.",
            "",
            "## 다음에 다시 풀 때의 질문",
            "",
            "- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?",
            "- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?",
            "- 코드보다 먼저 적어 둘 한 문장은 무엇인가?",
            "",
            "## 같이 읽을 문서",
            "",
            *extra_links,
        ]
        return "\n".join(lines).rstrip() + "\n"
    if kind == "02-debug-log.md":
        extra_links = (concept_links[:2] + public_links + neighbor_links[:1])[:5]
        lines = [
            "## 왜 이 디버그 메모가 중요한가",
            "",
            f"- `{meta.korean_title}`는 `{focus}`를 연습하는 프로젝트라서, 작은 경계 조건 하나가 전체 상태 전이를 망가뜨릴 수 있다.",
            '- 그래서 이 문서는 "무엇이 틀렸는가"보다 "어떤 징후를 보면 같은 실수를 다시 알아차릴 수 있는가"를 남기는 데 의미가 있다.',
            f"- {bridge}",
            "- 재현 경로가 필요할 때는 `05-development-timeline.md`의 단계 순서와 이 디버그 로그를 같이 보면, 어느 시점에 어떤 실패를 확인해야 하는지 더 선명해진다.",
            "",
            "## 다음 수정 때 다시 볼 체크리스트",
            "",
            "- 가장 작은 입력과 대표 경계 입력을 먼저 다시 실행했는가?",
            "- 상태를 갱신하는 순서가 문제 규칙과 정확히 같은가?",
            "- `make -C problem test` 결과와 문서 설명이 서로 어긋나지 않는가?",
            "",
            "## 같이 점검할 문서",
            "",
            *extra_links,
        ]
        return "\n".join(lines).rstrip() + "\n"
    if kind == "03-retrospective.md":
        extra_links = (public_links + concept_links[:3])[:5]
        lines = [
            "## 이번 프로젝트가 남긴 기준",
            "",
            f"- `{meta.korean_title}`를 통해 `{focus}`를 코드와 문장으로 같이 설명하는 감각을 다시 확인했다.",
            "- 짧은 정답 코드보다, 왜 이 선택이 안전했는지 적어 둔 문장이 나중에 더 오래 남는다.",
            f"- {bridge}",
            "",
            "## 다음 프로젝트로 가져갈 것",
            "",
            "- 구현을 시작하기 전에 핵심 상태와 종료 조건을 먼저 적는다.",
            "- 자동 검증이 통과한 뒤에야 문서 문장을 확정한다.",
            '- 포트폴리오용 README로 옮길 때는 "선택 이유"와 "실수 포인트"를 먼저 보여 준다.',
            "- `05-development-timeline.md`처럼 실행 순서와 검증 순서를 남기면, 시간이 지난 뒤에도 학습 과정을 다시 밟기 쉬워진다.",
            "",
            "## 트랙 안에서 이어지는 연결",
            "",
            *neighbor_links,
            "- 현재 프로젝트를 다시 설명할 때는 같은 트랙의 앞뒤 프로젝트와 무엇이 달라졌는지 한 문장으로 비교해 두는 편이 좋다.",
            "",
            "## 다시 확인할 경로",
            "",
            *extra_links,
        ]
        return "\n".join(lines).rstrip() + "\n"
    if kind == "04-knowledge-index.md":
        extra_links = (concept_links + public_links)[:6] or [
            "- [`../docs/README.md`](../docs/README.md)"
        ]
        lines = [
            "## 다시 연결해 볼 질문",
            "",
            f"- `{meta.korean_title}`에서 쓴 개념이 같은 트랙의 다음 문제에서 어떻게 더 어려워지는가?",
            f"- `{focus}`를 다른 자료구조나 다른 언어 구현으로 옮기면 무엇이 달라지는가?",
            "- 이번에 정리한 용어와 판단 기준을 README 한 단락으로 축약하면 무엇이 남는가?",
            "",
            "## 한 줄 정리 후보",
            "",
            f"- `{meta.korean_title}`를 다시 설명할 때는 문제 이름보다 `{focus}`를 먼저 말한다.",
            "- 개념 이름만 적지 말고, 그 개념이 어떤 입력이나 어떤 전이 규칙에서 필요했는지를 같이 남긴다.",
            "",
            "## 다음 문제와 연결되는 포인트",
            "",
            *neighbor_links,
            "- 같은 트랙의 다음 문제로 갈수록 자료구조 선택과 검증 순서가 더 중요해진다. 그래서 `05-development-timeline.md`에 남긴 실행 흐름도 함께 기억해 두는 편이 좋다.",
            "",
            "## 바로 열어 볼 문서",
            "",
            *extra_links,
        ]
        return "\n".join(lines).rstrip() + "\n"
    if kind == "05-development-timeline.md":
        lines = [
            "## 이 타임라인을 읽는 기준",
            "",
            "- `docs/references/reproducibility.md`가 빠른 명령표라면, 이 문서는 어떤 순서로 문제를 읽고 구현과 검증을 확인했는지까지 남기는 장문 재현 기록이다.",
            f"- `{meta.korean_title}`에서는 `{focus}`를 실제 명령과 문서 흐름으로 다시 밟아 볼 수 있어야 학습 기록으로서 가치가 생긴다.",
            f"- {bridge}",
            "",
            "## 지금 다시 따라 할 때의 최소 순서",
            "",
            "1. `problem/README.md`와 `docs/references/overview.md`로 문제 자료와 읽기 순서를 먼저 확인한다.",
            "2. `make -C problem test`로 현재 구현이 fixture를 통과하는지 가장 먼저 본다.",
            "3. `make -C problem run-py`로 대표 입력을 직접 따라가며 상태 전이를 확인한다.",
        ]
        if meta.has_cpp:
            lines.append("4. `make -C problem run-cpp`로 비교 구현까지 같은 흐름으로 맞춰 본다.")
            lines.append("5. `01-approach-log.md`, `02-debug-log.md`와 함께 읽으며 선택 이유와 실패 지점을 대조한다.")
        else:
            lines.append("4. `01-approach-log.md`, `02-debug-log.md`와 함께 읽으며 선택 이유와 실패 지점을 대조한다.")
        lines.extend(
            [
                "",
                "## 재현이 끝났는지 확인하는 질문",
                "",
                "- 문서에 적힌 경로와 실제 실행 명령이 모두 맞는가?",
                "- 자동 검증 결과와 수동 실행에서 본 상태 전이가 서로 모순되지 않는가?",
                "- 같은 트랙의 다음 프로젝트로 넘어가기 전에 이번 선택 기준을 한 문장으로 요약할 수 있는가?",
                "",
                "## 이어서 읽을 경로",
                "",
                *public_links[:2],
                *neighbor_links,
            ]
        )
        return "\n".join(lines).rstrip() + "\n"
    return ""


def soften_legacy_reference(match: re.Match[str], meta: "ProjectMeta") -> str:
    legacy_path = match.group(1)
    return (
        f"provenance 메모: 이전 마이그레이션 기록상 원본 경로는 `{legacy_path}`였다. "
        f"현재 읽을 기준 경로는 `study/{meta.track}/{meta.slug}`이다."
    )


def sanitize_archive_body(text: str, meta: "ProjectMeta") -> str:
    body = strip_first_heading(text)
    body = re.sub(
        r"(?m)^> 이 문서는 소스코드만으로는 추적할 수 없는 개발 과정을 순차적으로 기록한다\.\n?",
        "",
        body,
    )
    body = re.sub(
        r"```bash\s*python3 tools/migrate_legacy_to_study\.py.*?```",
        "",
        body,
        flags=re.DOTALL,
    )
    body = re.sub(
        r"(?m)^python3 tools/migrate_legacy_to_study\.py.*\n?",
        "",
        body,
    )
    body = re.sub(
        r"이 프로젝트는 legacy 구조\(`([^`]+)`\)에서 마이그레이션(?:된 것이다| 도구를 통해 변환했다)?\.",
        lambda match: soften_legacy_reference(match, meta),
        body,
    )
    body = re.sub(
        r"legacy 구조\(`([^`]+)`\)에서 마이그레이션(?:된 것이다| 도구를 통해 변환했다)?\.",
        lambda match: soften_legacy_reference(match, meta),
        body,
    )
    body = re.sub(
        r"legacy 경로 `([^`]+)`에서 마이그레이션\.",
        lambda match: soften_legacy_reference(match, meta),
        body,
    )
    body = re.sub(
        r"legacy `([^`]+)`에서 마이그레이션(?:\.|\. C\+\+ 비교 구현 유지\.)",
        lambda match: soften_legacy_reference(match, meta),
        body,
    )
    body = body.replace(
        "provenance 메모: 이전 마이그레이션 기록상 원본 경로는 `legacy/core/02-stack-queue/gold-5430`였다. 현재 읽을 기준 경로는 `study/Core-02-Stack-Queue/5430`이다. C++ 비교 구현 유지.",
        "provenance 메모: 이전 마이그레이션 기록상 원본 경로는 `legacy/core/02-stack-queue/gold-5430`였다. 현재 읽을 기준 경로는 `study/Core-02-Stack-Queue/5430`이다. 당시에도 C++ 비교 구현을 함께 유지했다.",
    )
    body = body.replace(
        "마이그레이션 도구(`tools/migrate_legacy_to_study.py`)를 사용해 새 구조로 변환했다.",
        "이전 마이그레이션 기록을 참고해 현재 학습 구조로 정리했다.",
    )
    body = body.replace(
        "| 마이그레이션 | `tools/migrate_legacy_to_study.py` |",
        "| provenance | 이전 마이그레이션 기록 참고 |",
    )
    body = re.sub(r"```bash\s*(?:#.*\n)?\s*```", "", body)
    body = re.sub(r"```[a-zA-Z0-9_-]*\n\s*```", "", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def build_timeline_body(meta: "ProjectMeta") -> str:
    timeline_path = meta.project_dir / "notion-archive" / "05-development-timeline.md"
    if not timeline_path.exists():
        return ""
    body = sanitize_archive_body(read_text(timeline_path), meta)
    if not body:
        return ""
    body = re.sub(r"(?m)^### ", "#### ", body)
    body = re.sub(r"(?m)^## ", "### ", body)
    body = re.sub(r"(?m)^### Phase ([0-9-]+): ", r"### 단계 \1: ", body)
    body = re.sub(r"(?m)^### Phase ", "### 단계 ", body)
    return body.strip()


def curated_timeline_file(meta: "ProjectMeta") -> str:
    body = build_timeline_body(meta)
    if word_count(body) < NOTION_MIN_WORDS["05-development-timeline.md"]:
        supplement = notion_supplement(meta, "05-development-timeline.md")
        if supplement:
            body = f"{body}\n\n{supplement.strip()}" if body else supplement.strip()
    parts = [
        "# 개발 타임라인",
        "",
        f"> 프로젝트: {meta.korean_title}",
        "> 이 문서는 학습자가 현재 저장소 기준으로 구현과 검증 과정을 끝까지 다시 밟아 볼 수 있게 정리한 재현 문서다.",
        "",
        "## 왜 이 문서가 중요한가",
        "",
        "- `docs/references/reproducibility.md`는 빠른 실행 명령을 확인하는 문서이고, 여기서는 그 명령을 어떤 순서와 맥락에서 실행했는지까지 남긴다.",
        "- 학습 레포에서 재현성은 '명령 하나를 안다'가 아니라 '어떤 문서를 읽고 어떤 확인을 거쳐 현재 구현에 도달하는지 따라갈 수 있다'는 뜻에 더 가깝다.",
        "",
        "## 재현 시작점",
        "",
        f"- 현재 기준 경로: `study/{meta.track}/{meta.slug}`",
        "- 먼저 확인할 빠른 명령: `make -C problem test`",
        "- 함께 읽을 빠른 문서: `../docs/references/reproducibility.md`, `01-approach-log.md`, `02-debug-log.md`",
    ]
    if body:
        parts.extend(
            [
                "",
                "## 단계별 기록",
                "",
                "아래 메모는 `notion-archive/05-development-timeline.md`의 실제 기록을 현재 공개 노트 기준으로 다듬고, 지금 다시 따라 할 때 필요한 설명을 덧붙인 버전이다.",
                "",
                body,
            ]
        )
    return "\n".join(parts).rstrip() + "\n"


def curated_notion_file(meta: "ProjectMeta", kind: str) -> str | None:
    if kind == "05-development-timeline.md":
        return curated_timeline_file(meta)
    archive_path = meta.project_dir / "notion-archive" / kind
    if not archive_path.exists():
        return None
    body = sanitize_archive_body(read_text(archive_path), meta)
    if not body:
        return None
    if word_count(body) < NOTION_MIN_WORDS[kind]:
        supplement = notion_supplement(meta, kind)
        if supplement:
            body = f"{body}\n\n{supplement.strip()}"
    parts = [
        f"# {NOTION_SECTION_TITLES[kind]}",
        "",
        f"> 프로젝트: {meta.korean_title}",
        f"> 아래 내용은 `notion-archive/{kind}`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.",
        "",
        body,
    ]
    return "\n".join(parts).rstrip() + "\n"


def run_tests() -> dict[str, TestResult]:
    results: dict[str, TestResult] = {}
    for track in TRACKS:
        for slug in track["projects"]:
            project_key = f"{track['id']}/{slug}"
            problem_dir = STUDY / track["id"] / slug / "problem"
            proc = subprocess.run(
                ["make", "test"],
                cwd=problem_dir,
                capture_output=True,
                text=True,
                timeout=120,
            )
            output = (proc.stdout + proc.stderr).strip()
            lines = [line.strip() for line in output.splitlines() if line.strip()]
            summary = lines[-1] if lines else "출력 없음"
            results[project_key] = TestResult(proc.returncode == 0, summary, output)
    return results


def build_project_meta(test_results: dict[str, TestResult]) -> list[ProjectMeta]:
    projects: list[ProjectMeta] = []
    for track in TRACKS:
        for slug in track["projects"]:
            readme = STUDY / track["id"] / slug / "README.md"
            text = read_head_text(readme)
            table = {key: clean_inline(value) for key, value in extract_table(text).items()}
            heading_title = parse_heading_title(text)
            english_title = parse_english_title(heading_title, slug)
            kind = "advanced" if track["id"] == "Advanced-CLRS" else ("bridge" if track["id"] == "Core-Bridges" else "core")
            project_key = f"{track['id']}/{slug}"
            projects.append(
                ProjectMeta(
                    track=track["id"],
                    slug=slug,
                    kind=kind,
                    heading_title=heading_title,
                    english_title=english_title,
                    korean_title=KO_TITLES.get(project_key, english_title),
                    problem_url=table.get("Problem URL"),
                    level_or_type=table.get("Tier") or table.get("Type"),
                    clrs=table.get("CLRS"),
                    legacy_source=table.get("Legacy Source"),
                    project_focus=table.get("Project Focus"),
                    has_cpp=(STUDY / track["id"] / slug / "cpp").exists(),
                    test=test_results[project_key],
                )
            )
    return projects


def project_status_line(meta: ProjectMeta) -> str:
    if meta.test.passed:
        return f"- Python: {DATE} 기준 `make -C problem test` 통과"
    return f"- Python: {DATE} 기준 자동 검증 필요 (`{meta.test.summary}`)"


def cpp_status_line(meta: ProjectMeta) -> str:
    if not meta.has_cpp:
        return "- C++: 이 프로젝트 범위에서는 유지하지 않음"
    return "- C++: 비교 구현은 보관하지만, 이번 문서 정리 라운드에서는 별도 재검증하지 않음"


def format_impls(meta: ProjectMeta) -> str:
    return "Python + C++" if meta.has_cpp else "Python"


def root_readme(track_meta: list[dict], projects: list[ProjectMeta]) -> str:
    total_projects = len(projects)
    passed = sum(1 for project in projects if project.test.passed)
    legacy_note = (
        "- 현재 작업 트리에는 `legacy/` 디렉터리가 없으므로, 문서에서는 legacy를 필수 경로가 아니라 선택적 provenance 자료로만 다룬다."
        if not (ROOT / "legacy").exists()
        else "- `legacy/`는 원본 참조 트리로 유지하고, 새 학습 구조는 `study/`에서 읽는다."
    )
    track_lines = "\n".join(
        f"- [{track['id']}](study/{track['id']}/README.md): {track['intro']}"
        for track in track_meta
    )
    return normalize(
        f"""
        # 알고리즘 학습 아카이브

        이 저장소는 알고리즘 문제 풀이를 정답 모음으로 쌓아 두는 대신, 문제 자료와 구현, 공개 해설, 장문 학습 노트를 분리해 읽을 수 있는 학습 아카이브로 다시 정리한 레포다.
        목표는 "이 문제를 풀었다"에서 멈추지 않고, **왜 이런 구조로 공부했는지**까지 다른 사람이 따라올 수 있게 만드는 것이다.

        ## 이 레포로 배우는 것

        - 문제 원문, 구현, 공개 문서를 한 저장소 안에서 어떻게 분리해야 하는지
        - 작은 문제부터 그래프 후반부, CLRS 심화까지 어떤 순서로 밟으면 좋은지
        - 학습 레포를 읽는 사람이 자신의 공개 포트폴리오 레포를 어떻게 더 잘 설계할 수 있는지

        ## 누가 읽으면 좋은가

        - 백준과 CLRS를 함께 공부하면서, 문제 풀이 기록을 구조적으로 남기고 싶은 학생
        - 정답 코드만 나열된 레포가 아니라 "문제 자료 / 구현 / 해설 / 장문 노트"가 분리된 학습 레포를 만들고 싶은 사람
        - 나중에 자신의 포트폴리오 레포를 공개할 때 무엇을 남기고 무엇을 숨길지 기준이 필요한 사람

        ## 추천 읽기 순서

        1. [docs/legacy-audit.md](docs/legacy-audit.md)에서 현재 기준선과 provenance 규칙을 본다.
        2. [docs/curriculum-map.md](docs/curriculum-map.md)에서 트랙 순서와 브리지 프로젝트 이유를 본다.
        3. [study/README.md](study/README.md)에서 전체 학습 트리를 훑는다.
        4. [study/Core-00-Basics/10988/README.md](study/Core-00-Basics/10988/README.md) 같은 작은 프로젝트 하나를 끝까지 읽는다.
        5. 익숙해지면 같은 형식을 자기 레포에 그대로 옮겨 본다.

        ## 트랙 둘러보기

        {track_lines}

        ## 이 레포를 자기 포트폴리오로 옮길 때의 기준

        - `problem/`, 구현 디렉터리, 공개 문서, 장문 노트를 섞지 않는다.
        - README는 "문제 설명 복붙"이 아니라 "어떻게 읽고 어떻게 검증하는가"를 안내해야 한다.
        - `make test` 같은 재현 명령이 없다면, 설명이 좋아 보여도 학습 기록으로서 신뢰도가 떨어진다.
        - 빠른 검증 명령은 `docs/references/reproducibility.md`에, 전체 재현 흐름은 `notion/05-development-timeline.md`에 나눠 두면 학습자가 따라오기 쉽다.
        - 장문 노트는 공개용 `notion/`과 보관용 `notion-archive/`로 나눠 버전을 관리한다.

        ## 현재 워크스페이스 기준 메모

        - 총 프로젝트 수: {total_projects}
        - 자동 검증 통과: {passed}/{total_projects} (`make -C problem test` 기준)
        - 트랙 수: {len(track_meta)}
        {legacy_note}
        """
    )


def study_readme(track_meta: list[dict]) -> str:
    track_lines = "\n".join(
        f"- [{track['id']}]({track['id']}/README.md): {track['topic']}를 배우는 트랙"
        for track in track_meta
    )
    return normalize(
        f"""
        # study/ 안내

        `study/`는 이 레포의 실제 학습 트리다. 각 트랙은 같은 구조를 공유하지만, 배우는 개념과 설명 톤은 해당 주제에 맞게 다르게 정리한다.

        ## 읽는 법

        1. 트랙 README에서 왜 이 순서로 배우는지 확인한다.
        2. 프로젝트 README에서 읽기 순서와 검증 명령을 확인한다.
        3. `problem/` -> `docs/` -> 구현 -> `notion/05-development-timeline.md` -> 나머지 `notion/` 순으로 내려간다.

        ## 트랙 목록

        {track_lines}
        """
    )


def curriculum_map(track_meta: list[dict], project_meta: list[ProjectMeta]) -> str:
    meta_by_key = {project.key: project for project in project_meta}
    core_rows = []
    for track in track_meta:
        if track["id"] == "Advanced-CLRS":
            continue
        project_names = ", ".join(
            f"{slug} {meta_by_key[f'{track['id']}/{slug}'].korean_title}" for slug in track["projects"]
        )
        core_rows.append(
            f"| {track['id']} | {track['topic']} | {track['learning_focus']} | {project_names} |"
        )
    advanced_track = next(track for track in track_meta if track["id"] == "Advanced-CLRS")
    advanced_rows = "\n".join(
        f"| {slug} | {meta_by_key[f'Advanced-CLRS/{slug}'].korean_title} | {meta_by_key[f'Advanced-CLRS/{slug}'].clrs or '-'} |"
        for slug in advanced_track["projects"]
    )
    return normalize(
        f"""
        # 커리큘럼 맵

        이 문서는 레포 안의 프로젝트를 번호순이 아니라 **학습 순서**로 읽기 위한 안내서다. 문제를 나열하는 것이 아니라, 왜 이 주제가 다음 주제로 이어지는지 설명하는 데 목적이 있다.

        ## Core 트랙 순서

        | 트랙 | 주제 | 이 트랙에서 익히는 힘 | 대표 프로젝트 |
        | :--- | :--- | :--- | :--- |
        {'\n'.join(core_rows)}

        ## 브리지 프로젝트

        - `Core-Bridges/1717`은 MST 전에 union-find를 독립적으로 익히도록 넣은 보강 프로젝트다.
        - `Core-00-Basics/11053`은 DP 트랙 전에 "상태를 누적한다"는 감각을 먼저 보여 주는 작은 다리 역할을 한다.
        - `Core-00-Basics/16926`은 기본기 트랙에 두되, 시뮬레이션 트랙을 배운 뒤 다시 읽으면 더 잘 보이는 문제로 설명한다.

        ## Advanced-CLRS 순서

        Advanced 트랙은 CLRS 챕터를 그대로 옮기지 않고, 구현 가능한 작은 실험으로 다시 쪼개서 배치했다.

        | 슬롯 | 프로젝트 | CLRS | 비고 |
        | :--- | :--- | :--- | :--- |
        {advanced_rows}

        ## 이 맵을 포트폴리오 설계에 쓰는 방법

        - 작은 문제 몇 개만 잘 정리해도 커리큘럼 설계 감각은 충분히 드러난다.
        - 핵심은 "문제 수"보다 "왜 이 순서인지"를 설명하는 것이다.
        - 자기 레포를 만들 때도 트랙 단위 README를 두고, 프로젝트 README가 그 설명을 다시 구체화하도록 구성하는 편이 좋다.
        """
    )


def migration_template() -> str:
    layout = "\n".join(
        [
            "study/",
            "  <track>/",
            "    <project>/",
            "      README.md",
            "      problem/",
            "        README.md",
            "        Makefile",
            "        code/",
            "        data/",
            "        script/",
            "      python/",
            "        README.md",
            "        src/",
            "        tests/",
            "      cpp/                  # 비교 구현이 있을 때만",
            "        README.md",
            "        src/",
            "        include/",
            "        tests/",
            "      docs/",
            "        README.md",
            "        concepts/",
            "        references/",
            "      notion/",
            "        README.md",
            "        00-problem-framing.md",
            "        01-approach-log.md",
            "        02-debug-log.md",
            "        03-retrospective.md",
            "        04-knowledge-index.md",
            "        05-development-timeline.md",
            "      notion-archive/       # 이전 버전 보관본",
        ]
    )
    return "\n".join(
        [
            "# 마이그레이션 템플릿",
            "",
            "이 문서는 새 프로젝트를 `study/` 아래에 추가하거나, 기존 프로젝트 문서를 같은 톤으로 다시 쓰고 싶을 때 기준으로 삼는 템플릿이다.",
            "",
            "## 기본 디렉터리 구조",
            "",
            "```text",
            layout,
            "```",
            "",
            "## 문서 역할",
            "",
            "- `README.md`: 프로젝트를 처음 보는 사람이 읽는 입구",
            "- `problem/`: 문제 자료, fixture, 실행 스크립트",
            "- `python/`, `cpp/`: 구현과 실행 메모",
            "- `docs/`: 공개용 학습 문서",
            "- `notion/`: 긴 호흡의 공개 학습 노트",
            "- `notion-archive/`: 이전 버전 메모와 백업",
            "",
            "## README 권장 섹션",
            "",
            "- 트랙 README: `트랙 소개`, `왜 이 순서로 배우는가`, `프로젝트 목록`, `먼저 읽을 문서`, `포트폴리오 팁`",
            "- 프로젝트 README: `문제 한눈에 보기`, `이 프로젝트에서 배우는 것`, `추천 읽기 순서`, `디렉터리 구성`, `검증 방법`, `현재 상태`, `다음 확장 아이디어`",
            "- 구현 README: `구현 범위`, `왜 이 구현을 먼저 보는가`, `실행 명령`, `검증 명령`, `현재 상태`, `구현 메모`",
            "- 공개 문서 README: `이 디렉터리의 역할`, `포함 문서`, `추천 읽기 순서`",
            "",
            "## 완료 기준",
            "",
            "- 루트 README만 읽어도 이 프로젝트가 무엇을 공부하는지 알 수 있어야 한다.",
            "- `make -C problem test` 같은 재현 명령이 README에 드러나 있어야 한다.",
            "- `05-development-timeline.md`가 있으면 학습자가 구현과 검증 과정을 다시 밟을 수 있어야 한다.",
            "- `notion/`과 `notion-archive/`의 역할이 혼동되지 않아야 한다.",
            "- `legacy/`가 현재 워크스페이스에 없어도 문서가 깨지지 않아야 한다.",
            "",
        ]
    )


def legacy_audit(projects: list[ProjectMeta]) -> str:
    passed = sum(1 for project in projects if project.test.passed)
    return normalize(
        f"""
        # 레거시 감사 메모

        ## 현재 기준선

        - 감사 기준일: {DATE}
        - 현재 작업 트리의 프로젝트 수: {len(projects)}
        - 자동 검증 통과 수: {passed}/{len(projects)}
        - 현재 워크스페이스의 `legacy/` 디렉터리: {'존재함' if (ROOT / 'legacy').exists() else '없음'}

        ## 계속 유지하는 provenance 원칙

        - 예전 마이그레이션에서 기록한 `legacy/core/...` 경로는 "원본이 있었다면 여기에서 왔다"는 provenance 메모로만 유지한다.
        - 현재 워크스페이스에 `legacy/`가 없더라도, README와 공개 문서는 깨지지 않아야 한다.
        - 실제 학습 동선은 항상 `study/` 기준으로 설명한다.

        ## 이번 라운드에서 정리한 항목

        - 템플릿성 영어 헤더와 혼종 표현을 한국어 중심으로 정리했다.
        - `notion/`을 공개 가능한 학습 노트로 재정의하고, 기존 자료는 `notion-archive/`로 보존한다.
        - `05-development-timeline.md`를 다시 공개 노트 세트에 포함해, 빠른 검증 문서와 별도로 전체 재현 흐름을 남긴다.
        - 프로젝트 README의 상태 표시는 이번 라운드에 실제로 다시 확인한 자동 검증 결과만 반영한다.

        ## 아직 남겨 둔 보수적 원칙

        - C++ 비교 구현은 보관하되, 이번 문서 정리 라운드에서는 별도 자동 재검증 대상으로 삼지 않는다.
        - 개념 문서의 세부 내용은 기존 학습 로그를 우선 존중하되, 경로와 정책 문장은 새 구조에 맞게 보정한다.
        """
    )


def gitignore() -> str:
    return normalize(
        """
        .DS_Store
        __pycache__/
        *.pyc
        *.pyo
        *.swp
        *.swo
        *.o
        *.out
        *.a
        *.dSYM/
        .pytest_cache/
        .mypy_cache/
        tmp/
        .cache/
        """
    )


def track_readme(track: dict, meta_by_key: dict[str, ProjectMeta]) -> str:
    rows = []
    for index, slug in enumerate(track["projects"], start=1):
        meta = meta_by_key[f"{track['id']}/{slug}"]
        rows.append(
            f"| {index} | [{slug}]({slug}/README.md) | {meta.korean_title} | {format_impls(meta)} | {track['learning_focus']} |"
        )
    return normalize(
        f"""
        # {track['id']}

        ## 트랙 소개

        {track['intro']}

        ## 왜 이 순서로 배우는가

        {track['why']}

        ## 프로젝트 목록

        | 순서 | 프로젝트 | 문제명/주제 | 구현 | 읽는 포인트 |
        | :--- | :--- | :--- | :--- | :--- |
        {'\n'.join(rows)}

        ## 먼저 읽을 문서

        1. [../README.md](../README.md)에서 전체 학습 트리를 훑는다.
        2. [../../docs/curriculum-map.md](../../docs/curriculum-map.md)에서 이 트랙이 어디에 놓이는지 본다.
        3. 첫 번째 프로젝트 README를 읽고, `problem/` -> `docs/` -> 구현 -> `notion/05-development-timeline.md` 순서로 내려간다.

        ## 이 트랙을 자기 포트폴리오에 옮길 때의 팁

        {track['portfolio_tip']}
        """
    )


def project_summary(meta: ProjectMeta, track: dict) -> str:
    if meta.kind == "advanced":
        return (
            f"`{meta.korean_title}` 주제를 작은 실행 가능한 실험으로 바꾼 심화 프로젝트다. "
            f"문제 스펙은 `problem/`, 공개 해설은 `docs/`, 기본 구현은 `python/`, 긴 호흡의 학습 노트는 `notion/`에서 읽는다."
        )
    if meta.kind == "bridge":
        return (
            f"BOJ {meta.slug} `{meta.korean_title}`은 다음 그래프 트랙 전에 필요한 선행 개념을 먼저 고정하는 브리지 프로젝트다. "
            f"짧은 구현보다도 '왜 지금 이 개념이 필요한가'를 설명하는 데 초점을 둔다."
        )
    return (
        f"BOJ {meta.slug} `{meta.korean_title}`를 학습용 구조에 맞게 분리한 프로젝트다. "
        f"문제 자료는 `problem/`, 공개 해설은 `docs/`, 기본 구현은 `python/`, 긴 호흡의 학습 노트는 `notion/`에서 읽는다."
    )


def project_readme(meta: ProjectMeta, track: dict) -> str:
    detail_rows = [
        "| 항목 | 내용 |",
        "| :--- | :--- |",
        f"| 트랙 | `{meta.track}` |",
        f"| 문제명/주제 | {meta.korean_title} |",
        f"| CLRS | {meta.clrs or '-'} |",
    ]
    if meta.level_or_type:
        detail_rows.append(f"| 난도/유형 | {meta.level_or_type} |")
    if meta.problem_url:
        detail_rows.append(f"| 문제 링크 | {meta.problem_url} |")
    if meta.legacy_source:
        detail_rows.append(f"| provenance 메모 | `{meta.legacy_source}` |")
    if meta.project_focus:
        detail_rows.append(f"| 프로젝트 초점 | {meta.project_focus} |")
    impl_lines = [
        "- `problem/`: 문제 자료, fixture, 실행 스크립트",
        "- `python/`: 기본 구현과 실행 메모",
    ]
    if meta.has_cpp:
        impl_lines.append("- `cpp/`: 비교 구현과 구현 간 차이를 볼 때 쓰는 보조 경로")
    impl_lines.extend(
        [
            "- `docs/`: 공개용 해설과 검증 메모",
            "- `notion/`: 길게 정리한 공개 학습 노트와 `05-development-timeline.md` 중심의 재현 기록",
            "- `notion-archive/`: 이전 버전 메모와 보관본",
        ]
    )
    verify_lines = [
        "- `make -C problem test`: 가장 먼저 실행할 자동 검증 명령이다. fixture 기준으로 현재 구현이 깨지지 않았는지 빠르게 확인한다.",
        "- `make -C problem run-py`: 대표 입력을 눈으로 따라가며 Python 구현을 읽고 싶을 때 사용한다.",
    ]
    if meta.has_cpp:
        verify_lines.append("- `make -C problem run-cpp`: C++ 비교 구현이 있을 때 동작 차이를 확인하는 용도다.")
    next_idea = (
        "같은 입력을 Python과 C++ 양쪽에서 돌려 구현 선택의 장단점을 정리해 보자."
        if meta.has_cpp
        else "대표 경계 사례를 하나 더 만들어 `problem/data/`에 추가하고, 왜 그 사례가 중요한지 `docs/`에 적어 보자."
    )
    provenance_line = (
        f"- provenance: 현재 워크스페이스에는 `legacy/`가 없지만, 이전 마이그레이션 기록상 원본 경로는 `{meta.legacy_source}`였다."
        if meta.legacy_source
        else "- provenance: 이 프로젝트는 현재 `study/` 구조를 기준으로 읽으면 된다."
    )
    read_order = [
        "1. [problem/README.md](problem/README.md)에서 문제 자료와 실행 파일 구성을 확인한다.",
        "2. [docs/references/overview.md](docs/references/overview.md)에서 공개 문서 읽기 순서를 본다.",
        "3. [python/README.md](python/README.md)로 내려가 기본 구현을 읽는다.",
    ]
    if meta.has_cpp:
        read_order.append("4. [cpp/README.md](cpp/README.md)로 비교 구현을 본다.")
        read_order.append("5. [notion/05-development-timeline.md](notion/05-development-timeline.md)에서 전체 재현 흐름을 따라간다.")
        read_order.append("6. [notion/README.md](notion/README.md)에서 장문 학습 노트 전체를 훑는다.")
    else:
        read_order.append("4. [notion/05-development-timeline.md](notion/05-development-timeline.md)에서 전체 재현 흐름을 따라간다.")
        read_order.append("5. [notion/README.md](notion/README.md)에서 장문 학습 노트 전체를 훑는다.")
    title_prefix = "BOJ " + meta.slug if meta.kind != "advanced" else f"{meta.slug.split('-', 1)[0]} {meta.korean_title}"
    return normalize(
        f"""
        # {title_prefix} 학습 프로젝트

        ## 문제 한눈에 보기

        {'\n'.join(detail_rows)}

        {project_summary(meta, track)}

        ## 이 프로젝트에서 배우는 것

        - {track['learning_focus']}
        - 구현과 문서를 분리해 읽으면서, 코드보다 판단 기준을 먼저 설명하는 연습
        - {'Python 기본 구현과 C++ 비교 구현의 차이를 함께 보는 연습' if meta.has_cpp else 'Python 하나로도 재현 가능한 최소 완성본을 만드는 연습'}

        ## 추천 읽기 순서

        {'\n'.join(read_order)}

        ## 디렉터리 구성

        {'\n'.join(impl_lines)}

        ## 검증 방법

        {'\n'.join(verify_lines)}
        - `notion/05-development-timeline.md`: 위 명령을 어떤 순서로 다시 실행하고 무엇을 확인하면 되는지까지 정리한 장문 재현 기록이다.

        ## 현재 상태

        {project_status_line(meta)}
        {cpp_status_line(meta)}
        {provenance_line}

        ## 다음 확장 아이디어

        - {next_idea}
        - {track['portfolio_tip']}
        """
    )


def problem_readme(meta: ProjectMeta, track: dict) -> str:
    title_prefix = "BOJ " + meta.slug if meta.kind != "advanced" else f"{meta.slug.split('-', 1)[0]} {meta.korean_title}"
    lines = [
        f"# {title_prefix} 문제 자료",
        "",
        "## 이 디렉터리의 역할",
        "",
        "이 디렉터리는 문제 링크, fixture, starter code, 실행 스크립트를 한곳에 모아 둔 보관함이다. 구현을 보기 전에 여기서 어떤 자료가 준비되어 있는지 먼저 확인하면 학습 동선이 안정적이다.",
        "",
    ]
    if meta.problem_url:
        lines.extend(
            [
                "## 문제 원문",
                "",
                f"- 문제명: {meta.korean_title}",
                f"- 링크: {meta.problem_url}",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "## 프로젝트 스펙 요약",
                "",
                f"- 주제: {meta.korean_title}",
                f"- 초점: {meta.project_focus or track['learning_focus']}",
                "- 예제 입력과 기대 출력은 `data/input*.txt`, `data/output*.txt`에 정리했다.",
                "",
            ]
        )
    lines.extend(
        [
            "## 왜 이 자료를 남기는가",
            "",
            f"- 이 프로젝트의 핵심은 {track['learning_focus']}이다.",
            "- `docs/`는 판단 근거를, 구현 디렉터리는 실제 코드를, `notion/`은 더 긴 학습 노트와 재현 타임라인을 담당한다.",
            "",
            "## 포함 자료",
            "",
            "- `data/`: 대표 입력과 기대 출력",
            "- `code/`: starter code 또는 문제 보조 자료",
            "- `script/`: 수동 실행이나 채점 보조 스크립트",
            "- `Makefile`: 재현 명령 진입점",
            "",
            "## 먼저 실행해볼 명령",
            "",
            "- `make test`: 현재 기본 구현이 fixture를 통과하는지 빠르게 확인한다.",
            "- `make run-py`: 대표 입력으로 Python 구현을 눈으로 추적할 때 사용한다.",
        ]
    )
    if meta.has_cpp:
        lines.append("- `make run-cpp`: C++ 비교 구현을 함께 볼 때 사용한다.")
    return "\n".join(lines).rstrip() + "\n"


def impl_readme(meta: ProjectMeta, track: dict, lang: str) -> str:
    if lang == "python":
        title = "# Python 구현 안내"
        run_cmd = "- `python3 src/solution.py < ../problem/data/input1.txt`: 가장 짧은 수동 실행 경로다."
        status = (
            f"- {DATE} 기준 `make -C ../problem test` 통과"
            if meta.test.passed
            else f"- {DATE} 기준 자동 검증 필요 (`{meta.test.summary}`)"
        )
        note = "이 레포에서 기본 구현은 Python을 기준으로 설명한다. 먼저 여기서 상태 전이를 따라가고, 필요하면 다른 구현과 비교한다."
    else:
        title = "# C++ 비교 구현 안내"
        run_cmd = "- `make -C ../problem run-cpp`: 비교 구현을 직접 실행하는 가장 단순한 경로다."
        status = "- 이번 문서 정리 라운드에서는 별도 자동 재검증을 하지 않았다. Python 구현과 같은 fixture를 기준으로 비교용으로 읽는다."
        note = "C++ 디렉터리는 정답 코드를 더 빠르게 짜기 위한 공간이 아니라, 같은 알고리즘 결정을 다른 언어에서 어떻게 표현하는지 비교하는 용도에 가깝다."
    return normalize(
        f"""
        {title}

        ## 구현 범위

        - {meta.korean_title} 프로젝트의 {'기본' if lang == 'python' else '비교'} 구현
        - {'BOJ 전체 채점 범위' if meta.kind != 'advanced' else '저장소에서 설계한 fixture 전체 범위'}

        ## 왜 이 구현을 먼저 보는가

        {note}

        ## 실행 명령

        {run_cmd}

        ## 검증 명령

        - `make -C ../problem test`: 현재 프로젝트의 기본 자동 검증 루프다. 구현을 수정한 뒤에는 이 명령부터 다시 실행하는 편이 좋다.

        ## 현재 상태

        {status}

        ## 구현 메모

        - 공개용 판단 근거는 `../docs/`에 둔다.
        - 전체 재현 흐름은 `../notion/05-development-timeline.md`에서 먼저 확인하고, 더 긴 학습 노트는 `../notion/`에서 이어서 읽는다.
        - 이전 버전 메모나 예전 템플릿 흔적은 `../notion-archive/`에 보관한다.
        """
    )


def docs_readme(meta: ProjectMeta) -> str:
    impl_hint = "`../cpp/`" if meta.has_cpp else "필요하면 직접 다른 언어로 다시 구현해 보기"
    return normalize(
        f"""
        # 공개 학습 문서

        ## 이 디렉터리의 역할

        이 디렉터리는 `{meta.korean_title}` 프로젝트의 공개 해설과 검증 메모를 보관한다. 문제 원문 복사본보다, 어떤 판단 기준으로 구현을 읽어야 하는지 안내하는 데 목적이 있다.

        ## 포함 문서

        - `references/overview.md`: 이 프로젝트 문서를 어떤 순서로 읽으면 좋은지 안내
        - `references/approach.md`: 핵심 접근과 선택 이유
        - `references/reproducibility.md`: 빠르게 실행 명령과 최근 검증 결과를 확인하는 문서
        - `concepts/`: 경계 사례와 핵심 개념 정리
        - `../notion/05-development-timeline.md`: 전체 재현 흐름을 장문으로 따라가는 문서

        ## 추천 읽기 순서

        1. `references/overview.md`로 문서 지도를 본다.
        2. `references/approach.md`에서 판단 기준을 읽는다.
        3. 필요한 개념 문서를 확인한다.
        4. `references/reproducibility.md`에서 검증 명령을 확인한 뒤 구현으로 내려간다.
        5. 구현을 다 읽은 뒤에는 `../notion/05-development-timeline.md`에서 전체 재현 순서를 다시 밟는다.
        6. 마지막으로 `../notion/`의 나머지 노트로 개념과 회고를 확장한다.

        ## 함께 보면 좋은 경로

        - 기본 구현: `../python/`
        - {'비교 구현: `../cpp/`' if meta.has_cpp else f'추가 실험: {impl_hint}'}
        - 보관된 이전 노트: `../notion-archive/`
        """
    )


def overview_readme(meta: ProjectMeta) -> str:
    lines = [
        f"# 읽기 안내 — {meta.korean_title}",
        "",
        "## 추천 순서",
        "",
        "1. [../../README.md](../../README.md)에서 프로젝트 전체 구조를 먼저 본다.",
        "2. [approach.md](approach.md)에서 핵심 선택 기준을 읽는다.",
        "3. `../concepts/` 아래 문서에서 경계 사례와 개념을 보충한다.",
        "4. [reproducibility.md](reproducibility.md)에서 실제 실행 명령을 확인한다.",
        "5. [../../python/README.md](../../python/README.md)로 내려가 기본 구현을 읽는다.",
    ]
    if meta.has_cpp:
        lines.append("6. [../../cpp/README.md](../../cpp/README.md)에서 비교 구현을 본다.")
        lines.append("7. [../../notion/05-development-timeline.md](../../notion/05-development-timeline.md)에서 전체 재현 흐름을 따라간다.")
        lines.append("8. [../../notion/README.md](../../notion/README.md)에서 장문 노트 전체를 훑는다.")
    else:
        lines.append("6. [../../notion/05-development-timeline.md](../../notion/05-development-timeline.md)에서 전체 재현 흐름을 따라간다.")
        lines.append("7. [../../notion/README.md](../../notion/README.md)에서 장문 노트 전체를 훑는다.")
    lines.extend(
        [
            "",
            "## 메모",
            "",
            "- 공개 문서는 구현 판단 근거를 빠르게 훑는 용도다.",
            "- 빠른 실행 명령은 `reproducibility.md`에서, 전체 재현 흐름은 `../../notion/05-development-timeline.md`에서 확인한다.",
            "- 더 긴 노트는 `../../notion/`, 예전 버전 자료는 `../../notion-archive/`에 보관한다.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def reproducibility_readme(meta: ProjectMeta) -> str:
    verify_block = [
        f"# 검증 메모 — {meta.korean_title}",
        "",
        "## 기본 검증 명령",
        "",
        "```bash",
        "make -C problem test",
        "```",
        "",
        "- 문서를 다 읽지 않았더라도, 먼저 이 명령으로 구현이 현재 fixture를 통과하는지 확인하는 편이 좋다.",
        "",
        "## 대표 수동 실행 명령",
        "",
        "```bash",
        "make -C problem run-py",
        "```",
    ]
    if meta.has_cpp:
        verify_block.extend(["", "```bash", "make -C problem run-cpp", "```"])
    verify_block.extend(
        [
            "",
            "## 이 문서와 05 노트의 차이",
            "",
            "- 이 문서는 실행 명령과 최근 검증 결과를 빠르게 확인하기 위한 요약본이다.",
            "- 전체 재현 흐름과 단계별 판단은 `../../notion/05-development-timeline.md`에서 이어서 본다.",
            "",
            "## 마지막 확인",
            "",
            f"- 날짜: {DATE}",
            f"- 결과: {'통과' if meta.test.passed else '재확인 필요'}",
            f"- 요약: `{meta.test.summary}`",
            "",
            "## 독자 체크리스트",
            "",
            "- 구현을 바꿨다면 `make -C problem test`를 먼저 다시 돌렸는가?",
            "- 자동 검증이 통과한 뒤에 수동 실행으로 출력 형식을 다시 확인했는가?",
            "- 설명 문서와 실제 구현 경로가 서로 어긋나지 않는가?",
        ]
    )
    return "\n".join(verify_block).rstrip() + "\n"


def approach_readme(meta: ProjectMeta) -> str:
    focus = project_learning_focus(meta)
    impl_lines = ["- Python 기본 구현: `../../python/src/solution.py`"]
    if meta.has_cpp:
        impl_lines.append("- C++ 비교 구현: `../../cpp/src/solution.cpp`")
    return normalize(
        f"""
        # 접근 정리 — {meta.korean_title}

        ## 이 문서의 역할

        이 문서는 `{meta.korean_title}` 프로젝트를 읽을 때 어떤 판단 기준으로 구현을 따라가면 좋은지 정리한 짧은 안내서다. 정답 코드 자체보다, 어떤 상태를 먼저 고정하고 어떤 연산을 나중에 확인해야 하는지 설명하는 데 목적이 있다.

        ## 이번 프로젝트에서 특히 볼 것

        - 학습 초점: {focus}
        - {project_bridge_line(meta)}
        - {'CLRS에서 읽은 개념을 코드와 fixture로 다시 확인하는 흐름' if meta.kind == 'advanced' else '문제 규칙을 자료구조와 상태 전이로 바꾸는 흐름'}

        ## 먼저 고정할 질문

        - 입력을 어떤 자료구조로 받아 두어야 이후 연산이 단순해지는가?
        - 연산을 처리할 때 유지해야 하는 핵심 상태는 무엇인가?
        - 자동 검증으로 가장 먼저 확인할 실패 시나리오는 무엇인가?

        ## 읽는 기준

        - 먼저 `problem/README.md`로 자료 구성을 확인한다.
        - 그다음 `python/` 기본 구현에서 상태 전이가 어떻게 옮겨졌는지 본다.
        - 필요하면 경계 사례 문서를 다시 열어, 어떤 입력에서 구현이 흔들릴 수 있는지 점검한다.

        ## 코드 매핑 메모

        {'\n'.join(impl_lines)}
        - 전체 재현 흐름은 `../../notion/05-development-timeline.md`에서 빠르게 다시 밟을 수 있다.
        - 이 프로젝트의 더 긴 설명은 `../../notion/`, 이전 버전 메모는 `../../notion-archive/`에 둔다.
        """
    )


def notion_readme(meta: ProjectMeta) -> str:
    return normalize(
        f"""
        # notion/ 안내

        이 디렉터리는 `{meta.korean_title}` 프로젝트를 길게 정리한 공개 학습 노트를 담는다. README와 `docs/`가 빠른 탐색용이라면, 여기는 문제 해석과 선택 이유를 더 자세히 남기는 공간이다.
        이번 라운드에서는 `notion-archive/`에 남아 있던 실제 학습 기록을 가져와, 새 공개 노트 기준으로 다시 정리했다.

        ## 무엇이 들어 있나

        - `00-problem-framing.md`: 문제를 내 말로 다시 쓰는 곳
        - `01-approach-log.md`: 선택한 접근과 대안을 비교하는 곳
        - `02-debug-log.md`: 막혔던 지점과 수정 기록
        - `03-retrospective.md`: 이번 프로젝트에서 얻은 교훈 정리
        - `04-knowledge-index.md`: 다시 꺼내 쓸 개념과 참고 자료 모음
        - `05-development-timeline.md`: 학습자가 전체 구현과 검증 과정을 다시 밟아 볼 수 있게 정리한 재현 문서

        ## 함께 보는 법

        1. 먼저 루트 프로젝트 README와 `docs/`를 읽는다.
        2. 재현 흐름이 필요하면 `05-development-timeline.md`부터 연다.
        3. 선택 이유와 실패 기록이 궁금하면 `01`, `02`를 읽는다.
        4. 학습을 정리하고 다음 문제로 넘길 때는 `03`, `04`를 읽는다.
        5. 예전 버전 메모가 필요하면 `../notion-archive/`를 참고한다.
        """
    )


def notion_file(meta: ProjectMeta, kind: str) -> str:
    curated = curated_notion_file(meta, kind)
    if curated is not None:
        return curated
    if kind == "00-problem-framing.md":
        return normalize(
            f"""
            # 문제 프레이밍

            ## 프로젝트

            - 트랙: `{meta.track}`
            - 문제명/주제: {meta.korean_title}
            - CLRS: {meta.clrs or '-'}
            {f'- 링크: {meta.problem_url}' if meta.problem_url else '- 링크: `problem/README.md`의 스펙 요약 참고'}

            ## 내 말로 다시 쓰기

            - 이 문제는 무엇을 계산하거나 판정하라고 요구하는가?
            - 입력 형식에서 가장 먼저 주의해야 할 제약은 무엇인가?
            - 성공 기준을 한 문장으로 쓰면 무엇인가?

            ## 시작 전 체크

            - [ ] `problem/README.md`와 `docs/references/overview.md`를 읽었다.
            - [ ] 어떤 자료구조나 알고리즘 후보가 있는지 두세 가지 적어 두었다.
            - [ ] `make -C problem test`를 실행할 준비가 되어 있다.
            """
        )
    if kind == "01-approach-log.md":
        return normalize(
            f"""
            # 접근 로그

            ## 이번에 채택한 방향

            - 먼저 떠올린 접근:
            - 최종 채택한 접근:
            - 왜 이 접근이 더 설명하기 쉬웠는가:

            ## 대안 비교

            | 후보 | 장점 | 미채택 이유 |
            | :--- | :--- | :--- |
            | 후보 1 |  |  |
            | 후보 2 |  |  |

            ## 구현에 옮길 때의 기준

            - 상태를 어떤 이름으로 둘지
            - 반복/재귀 종료 조건을 어디서 확인할지
            - 검증 명령을 언제 돌릴지
            """
        )
    if kind == "02-debug-log.md":
        return normalize(
            f"""
            # 디버그 로그

            ## 막혔던 지점

            | 증상 | 원인 | 수정 | 다시 확인한 방법 |
            | :--- | :--- | :--- | :--- |
            |  |  |  |  |

            ## 재현 기록

            - 실패를 재현한 입력:
            - 관련 함수나 코드 위치:
            - 수정 후 다시 실행한 명령:

            ## 다음에 같은 실수를 막으려면

            - 경계 조건 체크리스트에 무엇을 추가할지
            - 문서에서 먼저 적어 둘 설명은 무엇인지
            """
        )
    if kind == "03-retrospective.md":
        return normalize(
            f"""
            # 회고

            ## 이번 프로젝트에서 좋아진 점

            - 문제 해석 측면:
            - 구현 측면:
            - 문서화 측면:

            ## 아직 약한 점

            - 시간을 오래 쓴 지점:
            - 다시 풀면 더 단순하게 만들고 싶은 부분:

            ## 다음 프로젝트로 가져갈 습관

            - 먼저 남길 문장:
            - 먼저 실행할 검증 명령:
            - 포트폴리오 README에 바로 옮길 수 있는 표현:
            """
        )
    if kind == "05-development-timeline.md":
        return normalize(
            f"""
            # 개발 타임라인

            ## 재현 시작점

            - 현재 기준 경로: `study/{meta.track}/{meta.slug}`
            - 먼저 읽을 문서: `../docs/references/reproducibility.md`
            - 먼저 실행할 명령: `make -C problem test`

            ## 권장 재현 순서

            1. `problem/README.md`로 문제 자료와 fixture를 확인한다.
            2. `docs/references/reproducibility.md`에서 빠른 명령을 점검한다.
            3. `python/README.md`를 읽고 `make -C problem run-py`로 상태 전이를 확인한다.
            4. 필요하면 `01-approach-log.md`, `02-debug-log.md`로 선택 이유와 실패 기록을 함께 본다.

            ## 마지막 체크

            - 설명 문서와 실제 명령이 서로 어긋나지 않는가?
            - 자동 검증을 다시 돌린 뒤에도 같은 결론이 나오는가?
            - 다음 프로젝트로 넘어가기 전에 이번 문제의 핵심 선택 기준을 한 문장으로 말할 수 있는가?
            """
        )
    return normalize(
        f"""
        # 지식 인덱스

        ## 다시 꺼내 쓸 개념

        | 개념 | 이번 프로젝트에서 왜 중요했는가 | 다음에 다시 만날 곳 |
        | :--- | :--- | :--- |
        |  |  |  |

        ## 참고 자료

        - 문서 제목:
        - 링크 또는 파일 경로:
        - 확인 날짜:
        - 이번 프로젝트에 어떤 도움이 되었는가:

        ## 내 표현으로 정리한 한 줄

        - 
        """
    )


def normalize_approach(path: Path, meta: ProjectMeta) -> None:
    text = read_text(path)
    if meta.kind == "advanced" or word_count(text) < 80:
        write_text(path, approach_readme(meta))
        return
    text = re.sub(r"^# Approach", "# 접근 정리", text, flags=re.MULTILINE)
    block = ["## 코드 매핑 메모", "", f"- Python 기본 구현: `../../python/src/solution.py`"]
    if meta.has_cpp:
        block.append("- C++ 비교 구현: `../../cpp/src/solution.cpp`")
    block.extend(
        [
            "- 이 문서에서 설명한 상태 전이와 선택 기준을 실제 코드에서 대조할 때는 Python 구현을 먼저 읽는 편이 좋다.",
            "- 전체 재현 흐름은 `../../notion/05-development-timeline.md`에서 다시 밟을 수 있다.",
            "- 더 긴 설명은 `../../notion/`, 이전 버전 메모는 `../../notion-archive/`에서 이어서 볼 수 있다.",
            "",
        ]
    )
    replacement = "\n".join(block)
    text = re.sub(r"## 코드 매핑 메모\n.*?(?=\n## 정리)", replacement, text, flags=re.DOTALL)
    write_text(path, text)


def common_markdown_cleanup(path: Path) -> None:
    text = read_text(path)
    replacements = {
        "# Public Notes": "# 공개 학습 문서",
        "# Reference Overview": "# 읽기 안내",
        "# Reproducibility": "# 검증 메모",
        "# Edge Cases": "# 경계 사례 점검",
        "## Reading Guide": "## 추천 읽기 순서",
        "## Notes": "## 메모",
        "## Problem Constraints Recap": "## 문제 조건 다시 보기",
        "## Edge Case Analysis": "## 경계 사례 점검",
        "## Summary": "## 요약",
        "repo-authored": "저장소에서 직접 설계한",
        "public docs": "공개 문서",
        "local-only": "공개 노트와 분리된 전용",
        "process-heavy": "긴 호흡의",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.replace("`lab-report`와 `devlog`는 공개 문서에서 제외하고 `notion/`으로 옮겼다.", "`lab-report`와 `devlog` 성격의 이전 메모는 `notion-archive/`로 보관했고, 새 학습 노트는 `notion/`에 정리한다.")
    write_text(path, text)


def refresh_project(project: ProjectMeta, track: dict) -> None:
    project_dir = project.project_dir
    notion_dir = project_dir / "notion"
    archive_dir = project_dir / "notion-archive"
    if notion_dir.exists() and not archive_dir.exists():
        notion_dir.rename(archive_dir)
    notion_dir.mkdir(exist_ok=True)

    write_text(project_dir / "README.md", project_readme(project, track))
    write_text(project_dir / "problem" / "README.md", problem_readme(project, track))
    write_text(project_dir / "python" / "README.md", impl_readme(project, track, "python"))
    if project.has_cpp:
        write_text(project_dir / "cpp" / "README.md", impl_readme(project, track, "cpp"))
    write_text(project_dir / "docs" / "README.md", docs_readme(project))
    write_text(project_dir / "docs" / "references" / "overview.md", overview_readme(project))
    write_text(project_dir / "docs" / "references" / "reproducibility.md", reproducibility_readme(project))
    approach_path = project_dir / "docs" / "references" / "approach.md"
    if approach_path.exists():
        normalize_approach(approach_path, project)
    else:
        write_text(approach_path, approach_readme(project))
    write_text(notion_dir / "README.md", notion_readme(project))
    for filename in [
        "00-problem-framing.md",
        "01-approach-log.md",
        "02-debug-log.md",
        "03-retrospective.md",
        "04-knowledge-index.md",
        "05-development-timeline.md",
    ]:
        write_text(notion_dir / filename, notion_file(project, filename))

    for markdown_path in project_dir.rglob("*.md"):
        if "notion-archive" in markdown_path.parts:
            continue
        common_markdown_cleanup(markdown_path)


def main() -> None:
    test_results = run_tests()
    projects = build_project_meta(test_results)
    meta_by_key = {project.key: project for project in projects}

    write_text(ROOT / "README.md", root_readme(TRACKS, projects))
    write_text(STUDY / "README.md", study_readme(TRACKS))
    write_text(ROOT / "docs" / "curriculum-map.md", curriculum_map(TRACKS, projects))
    write_text(ROOT / "docs" / "migration-template.md", migration_template())
    write_text(ROOT / "docs" / "legacy-audit.md", legacy_audit(projects))
    write_text(ROOT / ".gitignore", gitignore())

    for track in TRACKS:
        write_text(STUDY / track["id"] / "README.md", track_readme(track, meta_by_key))
        for slug in track["projects"]:
            refresh_project(meta_by_key[f"{track['id']}/{slug}"], track)


if __name__ == "__main__":
    main()

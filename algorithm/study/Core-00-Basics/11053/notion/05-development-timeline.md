# 개발 타임라인

> 프로젝트: 가장 긴 증가하는 부분 수열
> 이 문서는 학습자가 현재 저장소 기준으로 구현과 검증 과정을 끝까지 다시 밟아 볼 수 있게 정리한 재현 문서다.

## 왜 이 문서가 중요한가

- `docs/references/reproducibility.md`는 빠른 실행 명령을 확인하는 문서이고, 여기서는 그 명령을 어떤 순서와 맥락에서 실행했는지까지 남긴다.
- 학습 레포에서 재현성은 '명령 하나를 안다'가 아니라 '어떤 문서를 읽고 어떤 확인을 거쳐 현재 구현에 도달하는지 따라갈 수 있다'는 뜻에 더 가깝다.

## 재현 시작점

- 현재 기준 경로: `study/Core-00-Basics/11053`
- 먼저 확인할 빠른 명령: `make -C problem test`
- 함께 읽을 빠른 문서: `../docs/references/reproducibility.md`, `01-approach-log.md`, `02-debug-log.md`

## 단계별 기록

아래 메모는 `notion-archive/05-development-timeline.md`의 실제 기록을 현재 공개 노트 기준으로 다듬고, 지금 다시 따라 할 때 필요한 설명을 덧붙인 버전이다.

### 단계 1: 프로젝트 초기화

#### 마이그레이션
provenance 메모: 이전 마이그레이션 기록상 원본 경로는 `legacy/core/00-basics/gold-11053`였다. 현재 읽을 기준 경로는 `study/Core-00-Basics/11053`이다.

생성된 디렉터리 구조:
```
study/Core-00-Basics/11053/
├── README.md
├── problem/
│   ├── Makefile
│   ├── code/        # starter.py, starter.cpp
│   ├── data/        # input/output fixtures
│   └── script/      # test.sh
├── python/
│   ├── src/         # solution.py
│   └── tests/
├── cpp/
│   └── src/         # solution.cpp
├── docs/
│   ├── concepts/    # lis-concept.md, edge-cases.md
│   └── references/  # approach.md, overview.md, reproducibility.md
└── notion/
```

#### C++ 구현 유지 결정
이 프로젝트는 Gold 난이도이고, Python/C++ 교차 검증이 학습에 도움이 된다고 판단하여 C++ 구현을 함께 유지하기로 했다.

### 단계 2: 문제 분석

#### 문제 원문 확인
BOJ 11053 페이지에서 입출력 형식과 제약 조건을 확인했다.
핵심 제약: $N \le 1\,000$, $A_i \le 1\,000$, **엄격 증가**.

#### 알고리즘 선택
$O(N^2)$ DP vs $O(N \log N)$ 이분탐색 중 DP를 선택.
이유: 학습 초기 단계에서 DP 패턴을 체화하는 것이 우선이고, $N=1\,000$에서 $O(N^2)$이 충분하기 때문.

#### 테스트 fixture 배치
공식 예제를 `problem/data/`에 배치:
- `input1.txt`: `6\n10 20 10 30 20 50` → `output1.txt`: `4`

### 단계 3: 솔루션 구현

#### Python 구현 (`python/src/solution.py`)
- `sys.stdin.readline` 입력 패턴
- `dp = [1] * n` 초기화
- 이중 루프로 전이 (`a[j] < a[i]` 조건)
- `print(max(dp))`로 답 출력

#### C++ 구현 (`cpp/src/solution.cpp`)
- `vector<int> dp(n, 1)` 초기화
- 동일한 이중 루프 구조
- `*max_element(dp.begin(), dp.end())`로 답 출력

#### C++ 빌드 명령
```bash
g++-14 -std=c++17 -O2 -Wall cpp/src/solution.cpp -o /tmp/sol_11053
```

### 단계 4: 검증

#### fixture 테스트
```bash
cd study/Core-00-Basics/11053/problem
make test
```
결과: `Results: 1/1 passed, 0 failed`

#### 수동 교차 검증
```bash
# Python
python3 ../python/src/solution.py <<'EOF'
8
10 20 10 30 20 50 40 60
EOF
# 출력: 5

# C++
g++-14 -std=c++17 -O2 ../cpp/src/solution.cpp -o /tmp/sol_11053
/tmp/sol_11053 <<'EOF'
8
10 20 10 30 20 50 40 60
EOF
# 출력: 5
```
Python/C++ 출력 일치 확인.

### 단계 5: 문서화

#### docs/ 작성
- `concepts/lis-concept.md`: LIS 정의, 두 가지 고전 접근법, CLRS 연결
- `concepts/edge-cases.md`: 단일 원소, 정렬/역정렬, 전부 같은 값, 지그재그 등
- `references/approach.md`: DP 전략과 정당성, 대안 비교
- `references/reproducibility.md`: 실행 환경, CLI 명령, 관측 출력

#### Cross-Track 메모
README에 "Core-08-DP 진입 전에 bridge 문제로 다시 읽는다"는 메모를 추가했다.

### 사용한 도구 및 환경

| 항목 | 상세 |
|------|------|
| OS | macOS (Darwin, ARM64) |
| Python | python3 |
| C++ | g++-14, -std=c++17 |
| Shell | zsh |
| 빌드 도구 | GNU Make |
| provenance | 이전 마이그레이션 기록 참고 |
| 버전 관리 | Git |

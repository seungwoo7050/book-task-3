# 개발 타임라인 — BOJ 11053 (가장 긴 증가하는 부분 수열)

> 이 문서는 소스코드만으로는 추적할 수 없는 개발 과정을 순차적으로 기록한다.

## Phase 1: 프로젝트 초기화

### 마이그레이션
legacy 구조(`legacy/core/00-basics/gold-11053`)에서 마이그레이션 도구를 통해 변환했다.

```bash
python3 tools/migrate_legacy_to_study.py
```

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

### C++ 구현 유지 결정
이 프로젝트는 Gold 난이도이고, Python/C++ 교차 검증이 학습에 도움이 된다고 판단하여 C++ 구현을 함께 유지하기로 했다.

## Phase 2: 문제 분석

### 문제 원문 확인
BOJ 11053 페이지에서 입출력 형식과 제약 조건을 확인했다.
핵심 제약: $N \le 1\,000$, $A_i \le 1\,000$, **엄격 증가**.

### 알고리즘 선택
$O(N^2)$ DP vs $O(N \log N)$ 이분탐색 중 DP를 선택.
이유: 학습 초기 단계에서 DP 패턴을 체화하는 것이 우선이고, $N=1\,000$에서 $O(N^2)$이 충분하기 때문.

### 테스트 fixture 배치
공식 예제를 `problem/data/`에 배치:
- `input1.txt`: `6\n10 20 10 30 20 50` → `output1.txt`: `4`

## Phase 3: 솔루션 구현

### Python 구현 (`python/src/solution.py`)
- `sys.stdin.readline` 입력 패턴
- `dp = [1] * n` 초기화
- 이중 루프로 전이 (`a[j] < a[i]` 조건)
- `print(max(dp))`로 답 출력

### C++ 구현 (`cpp/src/solution.cpp`)
- `vector<int> dp(n, 1)` 초기화
- 동일한 이중 루프 구조
- `*max_element(dp.begin(), dp.end())`로 답 출력

### C++ 빌드 명령
```bash
g++-14 -std=c++17 -O2 -Wall cpp/src/solution.cpp -o /tmp/sol_11053
```

## Phase 4: 검증

### fixture 테스트
```bash
cd study/Core-00-Basics/11053/problem
make test
```
결과: `Results: 1/1 passed, 0 failed`

### 수동 교차 검증
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

## Phase 5: 문서화

### docs/ 작성
- `concepts/lis-concept.md`: LIS 정의, 두 가지 고전 접근법, CLRS 연결
- `concepts/edge-cases.md`: 단일 원소, 정렬/역정렬, 전부 같은 값, 지그재그 등
- `references/approach.md`: DP 전략과 정당성, 대안 비교
- `references/reproducibility.md`: 실행 환경, CLI 명령, 관측 출력

### Cross-Track 메모
README에 "Core-08-DP 진입 전에 bridge 문제로 다시 읽는다"는 메모를 추가했다.

## 사용한 도구 및 환경

| 항목 | 상세 |
|------|------|
| OS | macOS (Darwin, ARM64) |
| Python | python3 |
| C++ | g++-14, -std=c++17 |
| Shell | zsh |
| 빌드 도구 | GNU Make |
| 마이그레이션 | `tools/migrate_legacy_to_study.py` |
| 버전 관리 | Git |

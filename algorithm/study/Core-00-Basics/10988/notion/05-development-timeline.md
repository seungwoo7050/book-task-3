# 개발 타임라인 — BOJ 10988 (회문 판별)

> 이 문서는 소스코드만으로는 추적할 수 없는 개발 과정을 순차적으로 기록한다.

## Phase 1: 프로젝트 초기화

### 디렉터리 구조 생성

이 프로젝트는 legacy 구조(`legacy/core/00-basics/bronze-10988`)에서 마이그레이션된 것이다.
마이그레이션 도구(`tools/migrate_legacy_to_study.py`)를 사용해 새 구조로 변환했다.

```bash
# 마이그레이션 실행
python3 tools/migrate_legacy_to_study.py
```

생성된 디렉터리 구조:
```
study/Core-00-Basics/10988/
├── README.md
├── problem/
│   ├── Makefile
│   ├── README.md
│   ├── code/        # starter.py, starter.cpp
│   ├── data/        # input1.txt, input2.txt, output1.txt, output2.txt
│   └── script/      # test.sh
├── python/
│   ├── README.md
│   ├── src/         # solution.py
│   └── tests/
├── docs/
│   ├── README.md
│   ├── concepts/    # palindrome-concept.md, edge-cases.md
│   └── references/  # approach.md, overview.md, reproducibility.md
└── notion/          # 이 문서가 위치한 곳
```

## Phase 2: 문제 분석 및 fixture 준비

### 문제 원문 확인
BOJ 10988 문제 페이지에서 입출력 형식을 확인했다.

### 테스트 fixture 작성
`problem/data/`에 공식 예제를 기반으로 fixture를 배치했다:
- `input1.txt`: `level` → `output1.txt`: `1`
- `input2.txt`: `baekjoon` → `output2.txt`: `0`

### 테스트 스크립트 작성
`problem/script/test.sh`를 작성했다.
이 스크립트는 `data/` 폴더의 모든 `input*.txt`를 순회하면서 대응하는 `output*.txt`와 비교한다.

### Makefile 설정
```bash
# Makefile 주요 타겟
make -C problem test     # 전체 fixture 테스트
make -C problem run-py   # input1.txt로 수동 실행
```

## Phase 3: 솔루션 구현

### Python 구현 (`python/src/solution.py`)
- `sys.stdin.readline`으로 입력을 읽는 패턴 적용
- `word == word[::-1]` 슬라이싱 방식으로 회문 판별
- 삼항 연산자로 1/0 출력

### starter 코드 배치
- `problem/code/starter.py`: `solve()` 함수 뼈대만 제공
- `problem/code/starter.cpp`: `main()` 함수 뼈대만 제공 (C++은 유지하지 않기로 결정)

## Phase 4: 검증

### fixture 테스트 실행
```bash
cd study/Core-00-Basics/10988/problem
make test
```
결과: `Results: 2/2 passed, 0 failed`

### 수동 edge case 검증
```bash
cd study/Core-00-Basics/10988/problem
python3 ../python/src/solution.py <<'EOF'
abba
EOF
```
출력: `1` (짝수 길이 회문 정상 처리 확인)

## Phase 5: 문서화

### docs/ 작성
- `concepts/palindrome-concept.md`: 회문의 수학적 정의, 홀수/짝수 길이 차이, CLRS 연결
- `concepts/edge-cases.md`: 단일 문자, 최대 길이, 거의 회문 등 경계 사례
- `references/approach.md`: 접근 전략과 정당성 증명
- `references/reproducibility.md`: 실행 환경, 명령어, 관측 결과 기록

### README.md 정리
프로젝트 스코프, 구조 설명, 검증 방법을 한 파일에 정리했다.

## 사용한 도구 및 환경

| 항목 | 상세 |
|------|------|
| OS | macOS (Darwin, ARM64) |
| Python | python3 |
| Shell | zsh |
| 빌드 도구 | GNU Make |
| 에디터 | VS Code |
| 마이그레이션 | `tools/migrate_legacy_to_study.py` |
| 버전 관리 | Git (`algorithm` 레포) |

# Reproducibility — BOJ 1753 (최단경로)

## 환경

- BOJ 1753 실행 시각: 2026-02-28 05:11:48
- BOJ 1753 OS: `Darwin macbook_air 25.3.0 Darwin Kernel Version 25.3.0: Wed Jan 28 20:53:01 PST 2026; root:xnu-12377.81.4~5/RELEASE_ARM64_T8103 arm64`
- BOJ 1753 Shell: `zsh`
- BOJ 1753 작업 경로: `core/0C-shortest-path/silver-1753/problem`

## 실행 명령

```bash
cd core/0C-shortest-path/silver-1753/problem
make test
```

## Observed Output(공식 테스트)

```text
Test 1: PASS

Results: 1/1 passed, 0 failed
```

## Observed Output(수동 케이스 1개)

수동 케이스 목적: 도달 불가 정점(INF)과 도달 가능 정점이 함께 있을 때 출력을 검증한다.

### 입력

```text
5 6
1
5 1 1
1 2 2
1 3 3
2 3 4
2 4 5
3 4 6
```

### 실행 명령 (Python)

```bash
cd core/0C-shortest-path/silver-1753/problem
python3 ../solve/solution/solution.py <<'EOF'
5 6
1
5 1 1
1 2 2
1 3 3
2 3 4
2 4 5
3 4 6
EOF
```

### 실행 명령 (C++)

```bash
cd core/0C-shortest-path/silver-1753/problem
g++-14 -std=c++17 -D_Alignof=alignof -O2 -Wall ../solve/solution/solution.cpp -o /tmp/clrs_0C_shortest_path__silver_1753
/tmp/clrs_0C_shortest_path__silver_1753 <<'EOF'
5 6
1
5 1 1
1 2 2
1 3 3
2 3 4
2 4 5
3 4 6
EOF
```

### 관측 출력 (Python)

```text
0
2
3
7
INF
```

### 관측 출력 (C++)

```text
0
2
3
7
INF
```

## 검증 메모

- BOJ 1753 공식 테스트 요약: `Results: 1/1 passed, 0 failed`
- BOJ 1753 수동 케이스 교차검증: BOJ 1753 수동 케이스에서 Python/C++ 출력이 완전히 일치한다.
- BOJ 1753 문서에서는 공식 로그와 수동 로그를 분리 저장해 회귀 시 원인 구간을 빠르게 좁힌다.
- 이번 수동 케이스는 "도달 불가 정점(INF)과 도달 가능 정점이 함께 있을 때 출력을 검증한다." 검증에 초점을 맞췄다.

## 재현 체크리스트

- [ ] BOJ 1753 기준으로 `make test`를 재실행했을 때 `Results: 1/1 passed, 0 failed` 패턴이 유지되는가?
- [ ] BOJ 1753 수동 케이스 입력을 재사용했을 때 Python/C++ 출력이 계속 일치하는가?
- [ ] BOJ 1753 기준으로 `approach.md`의 복잡도/정당성 설명이 관측 출력과 충돌하지 않는가?

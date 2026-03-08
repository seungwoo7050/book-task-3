# Reproducibility — BOJ 1197 (최소 스패닝 트리)

## 환경

- BOJ 1197 실행 시각: 2026-02-28 05:11:48
- BOJ 1197 OS: `Darwin macbook_air 25.3.0 Darwin Kernel Version 25.3.0: Wed Jan 28 20:53:01 PST 2026; root:xnu-12377.81.4~5/RELEASE_ARM64_T8103 arm64`
- BOJ 1197 Shell: `zsh`
- BOJ 1197 작업 경로: `core/0D-mst-topo/silver-1197/problem`

## 실행 명령

```bash
cd core/0D-mst-topo/silver-1197/problem
make test
```

## Observed Output(공식 테스트)

```text
Test 1: PASS

Results: 1/1 passed, 0 failed
```

## Observed Output(수동 케이스 1개)

수동 케이스 목적: 사이클을 만드는 간선을 건너뛰고 최소 가중치 합을 얻는지 검증한다.

### 입력

```text
4 5
1 2 1
1 3 4
2 3 2
2 4 7
3 4 3
```

### 실행 명령 (Python)

```bash
cd core/0D-mst-topo/silver-1197/problem
python3 ../solve/solution/solution.py <<'EOF'
4 5
1 2 1
1 3 4
2 3 2
2 4 7
3 4 3
EOF
```

### 실행 명령 (C++)

```bash
cd core/0D-mst-topo/silver-1197/problem
g++-14 -std=c++17 -D_Alignof=alignof -O2 -Wall ../solve/solution/solution.cpp -o /tmp/clrs_0D_mst_topo__silver_1197
/tmp/clrs_0D_mst_topo__silver_1197 <<'EOF'
4 5
1 2 1
1 3 4
2 3 2
2 4 7
3 4 3
EOF
```

### 관측 출력 (Python)

```text
6
```

### 관측 출력 (C++)

```text
6
```

## 검증 메모

- BOJ 1197 공식 테스트 요약: `Results: 1/1 passed, 0 failed`
- BOJ 1197 수동 케이스 교차검증: BOJ 1197 수동 케이스에서 Python/C++ 출력이 완전히 일치한다.
- BOJ 1197 문서에서는 공식 로그와 수동 로그를 분리 저장해 회귀 시 원인 구간을 빠르게 좁힌다.
- 이번 수동 케이스는 "사이클을 만드는 간선을 건너뛰고 최소 가중치 합을 얻는지 검증한다." 검증에 초점을 맞췄다.

## 재현 체크리스트

- [ ] BOJ 1197 재검증 관점에서 `make test`를 재실행했을 때 `Results: 1/1 passed, 0 failed` 패턴이 유지되는가?
- [ ] BOJ 1197 수동 케이스 입력을 재사용했을 때 Python/C++ 출력이 계속 일치하는가?
- [ ] `approach.md`의 복잡도/정당성 설명이 관측 출력과 충돌하지 않는가? (점검 기준: `간선 가중치 정렬 + 유니온파인드로 MST를 구성하는 Kruskal`)

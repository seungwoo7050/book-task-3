# Reproducibility — BOJ 1991 (트리 순회)

## 환경

- BOJ 1991 실행 시각: 2026-02-28 05:11:48
- BOJ 1991 OS: `Darwin macbook_air 25.3.0 Darwin Kernel Version 25.3.0: Wed Jan 28 20:53:01 PST 2026; root:xnu-12377.81.4~5/RELEASE_ARM64_T8103 arm64`
- BOJ 1991 Shell: `zsh`
- BOJ 1991 작업 경로: `core/0B-graph-tree/silver-1991/problem`

## 실행 명령

```bash
cd core/0B-graph-tree/silver-1991/problem
make test
```

## Observed Output(공식 테스트)

```text
Test 1: PASS

Results: 1/1 passed, 0 failed
```

## Observed Output(수동 케이스 1개)

수동 케이스 목적: 자식이 없는 노드(.) 처리와 3가지 순회 순서 출력을 동시에 검증한다.

### 입력

```text
7
A B C
B D.
C E F
E..
F. G
D..
G..
```

### 실행 명령 (Python)

```bash
cd core/0B-graph-tree/silver-1991/problem
python3 ../solve/solution/solution.py <<'EOF'
7
A B C
B D.
C E F
E..
F. G
D..
G..
EOF
```

### 실행 명령 (C++)

```bash
cd core/0B-graph-tree/silver-1991/problem
g++-14 -std=c++17 -D_Alignof=alignof -O2 -Wall ../solve/solution/solution.cpp -o /tmp/clrs_0B_graph_tree__silver_1991
/tmp/clrs_0B_graph_tree__silver_1991 <<'EOF'
7
A B C
B D.
C E F
E..
F. G
D..
G..
EOF
```

### 관측 출력 (Python)

```text
ABDCEFG
DBAECFG
DBEGFCA
```

### 관측 출력 (C++)

```text
ABDCEFG
DBAECFG
DBEGFCA
```

## 검증 메모

- BOJ 1991 공식 테스트 요약: `Results: 1/1 passed, 0 failed`
- BOJ 1991 수동 케이스 교차검증: BOJ 1991 수동 케이스에서 Python/C++ 출력이 완전히 일치한다.
- BOJ 1991 문서에서는 공식 로그와 수동 로그를 분리 저장해 회귀 시 원인 구간을 빠르게 좁힌다.
- 이번 수동 케이스는 "자식이 없는 노드(.) 처리와 3가지 순회 순서 출력을 동시에 검증한다." 검증에 초점을 맞췄다.

## 재현 체크리스트

- [ ] BOJ 1991 기준으로 `make test`를 재실행했을 때 `Results: 1/1 passed, 0 failed` 패턴이 유지되는가?
- [ ] BOJ 1991 수동 케이스 입력을 재사용했을 때 Python/C++ 출력이 계속 일치하는가?
- [ ] `approach.md`의 복잡도/정당성 설명이 관측 출력과 충돌하지 않는가? (점검 기준: `이진 트리 노드 맵을 구성하고 preorder/inorder/postor...`)

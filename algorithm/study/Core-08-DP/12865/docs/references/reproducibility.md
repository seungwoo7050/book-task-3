# Reproducibility — BOJ 12865 (Normal Knapsack (평범한 배낭))

## 환경

- BOJ 12865 실행 시각: 2026-02-28 05:11:48
- BOJ 12865 OS: `Darwin macbook_air 25.3.0 Darwin Kernel Version 25.3.0: Wed Jan 28 20:53:01 PST 2026; root:xnu-12377.81.4~5/RELEASE_ARM64_T8103 arm64`
- BOJ 12865 Shell: `zsh`
- BOJ 12865 작업 경로: `core/08-dp/gold-12865/problem`

## 실행 명령

```bash
cd core/08-dp/gold-12865/problem
make test
```

## Observed Output(공식 테스트)

```text
Test 1: PASS

Results: 1/1 passed, 0 failed
```

## Observed Output(수동 케이스 1개)

수동 케이스 목적: 담음/안담음 분기에서 가치 비교와 테이블 갱신을 검증한다.

### 입력

```text
4 7
6 13
4 8
3 6
5 12
```

### 실행 명령 (Python)

```bash
cd core/08-dp/gold-12865/problem
python3 ../solve/solution/solution.py <<'EOF'
4 7
6 13
4 8
3 6
5 12
EOF
```

### 실행 명령 (C++)

```bash
cd core/08-dp/gold-12865/problem
g++-14 -std=c++17 -D_Alignof=alignof -O2 -Wall ../solve/solution/solution.cpp -o /tmp/clrs_08_dp__gold_12865
/tmp/clrs_08_dp__gold_12865 <<'EOF'
4 7
6 13
4 8
3 6
5 12
EOF
```

### 관측 출력 (Python)

```text
14
```

### 관측 출력 (C++)

```text
14
```

## 검증 메모

- BOJ 12865 공식 테스트 요약: `Results: 1/1 passed, 0 failed`
- BOJ 12865 수동 케이스 교차검증: BOJ 12865 수동 케이스에서 Python/C++ 출력이 완전히 일치한다.
- BOJ 12865 문서에서는 공식 로그와 수동 로그를 분리 저장해 회귀 시 원인 구간을 빠르게 좁힌다.
- 이번 수동 케이스는 "담음/안담음 분기에서 가치 비교와 테이블 갱신을 검증한다." 검증에 초점을 맞췄다.

## 재현 체크리스트

- [ ] BOJ 12865 재검증 관점에서 `make test`를 재실행했을 때 `Results: 1/1 passed, 0 failed` 패턴이 유지되는가?
- [ ] BOJ 12865 수동 케이스 입력을 재사용했을 때 Python/C++ 출력이 계속 일치하는가?
- [ ] BOJ 12865 기준으로 `approach.md`의 복잡도/정당성 설명이 관측 출력과 충돌하지 않는가?

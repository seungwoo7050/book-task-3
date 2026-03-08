# Reproducibility — BOJ 11053 (Longest Increasing Subsequence)

## 환경

- BOJ 11053 실행 시각: 2026-02-28 05:11:48
- BOJ 11053 OS: `Darwin macbook_air 25.3.0 Darwin Kernel Version 25.3.0: Wed Jan 28 20:53:01 PST 2026; root:xnu-12377.81.4~5/RELEASE_ARM64_T8103 arm64`
- BOJ 11053 Shell: `zsh`
- BOJ 11053 작업 경로: `core/00-basics/gold-11053/problem`

## 실행 명령

```bash
cd core/00-basics/gold-11053/problem
make test
```

## Observed Output(공식 테스트)

```text
Test 1: PASS

Results: 1/1 passed, 0 failed
```

## Observed Output(수동 케이스 1개)

수동 케이스 목적: 증가/감소가 섞인 수열에서 이전 상태 참조(dp[j])가 정확히 누적되는지 확인한다.

### 입력

```text
8
10 20 10 30 20 50 40 60
```

### 실행 명령 (Python)

```bash
cd core/00-basics/gold-11053/problem
python3 ../solve/solution/solution.py <<'EOF'
8
10 20 10 30 20 50 40 60
EOF
```

### 실행 명령 (C++)

```bash
cd core/00-basics/gold-11053/problem
g++-14 -std=c++17 -D_Alignof=alignof -O2 -Wall ../solve/solution/solution.cpp -o /tmp/clrs_00_basics__gold_11053
/tmp/clrs_00_basics__gold_11053 <<'EOF'
8
10 20 10 30 20 50 40 60
EOF
```

### 관측 출력 (Python)

```text
5
```

### 관측 출력 (C++)

```text
5
```

## 검증 메모

- BOJ 11053 공식 테스트 요약: `Results: 1/1 passed, 0 failed`
- BOJ 11053 수동 케이스 교차검증: BOJ 11053 수동 케이스에서 Python/C++ 출력이 완전히 일치한다.
- BOJ 11053 문서에서는 공식 로그와 수동 로그를 분리 저장해 회귀 시 원인 구간을 빠르게 좁힌다.
- 이번 수동 케이스는 "증가/감소가 섞인 수열에서 이전 상태 참조(dp[j])가 정확히 누적되는지 확인한다." 검증에 초점을 맞췄다.

## 재현 체크리스트

- [ ] BOJ 11053 재검증 관점에서 `make test`를 재실행했을 때 `Results: 1/1 passed, 0 failed` 패턴이 유지되는가?
- [ ] BOJ 11053 수동 케이스 입력을 재사용했을 때 Python/C++ 출력이 계속 일치하는가?
- [ ] `approach.md`의 복잡도/정당성 설명이 관측 출력과 충돌하지 않는가? (핵심 기준: `1차원 DP로 각 위치에서 끝나는 LIS 길이를 누적 계산`)

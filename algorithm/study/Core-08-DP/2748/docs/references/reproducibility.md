# Reproducibility — BOJ 2748 (Fibonacci Number 2 (피보나치 수 2))

## 환경

- BOJ 2748 실행 시각: 2026-02-28 05:11:48
- BOJ 2748 OS: `Darwin macbook_air 25.3.0 Darwin Kernel Version 25.3.0: Wed Jan 28 20:53:01 PST 2026; root:xnu-12377.81.4~5/RELEASE_ARM64_T8103 arm64`
- BOJ 2748 Shell: `zsh`
- BOJ 2748 작업 경로: `core/08-dp/bronze-2748/problem`

## 실행 명령

```bash
cd core/08-dp/bronze-2748/problem
make test
```

## Observed Output(공식 테스트)

```text
Test 1: PASS

Results: 1/1 passed, 0 failed
```

## Observed Output(수동 케이스 1개)

수동 케이스 목적: 작은 N에서 초기값(F0,F1)과 점화식 적용 순서를 검증한다.

### 입력

```text
10
```

### 실행 명령 (Python)

```bash
cd core/08-dp/bronze-2748/problem
python3 ../solve/solution/solution.py <<'EOF'
10
EOF
```

### 실행 명령 (C++)

```bash
cd core/08-dp/bronze-2748/problem
g++-14 -std=c++17 -D_Alignof=alignof -O2 -Wall ../solve/solution/solution.cpp -o /tmp/clrs_08_dp__bronze_2748
/tmp/clrs_08_dp__bronze_2748 <<'EOF'
10
EOF
```

### 관측 출력 (Python)

```text
55
```

### 관측 출력 (C++)

```text
55
```

## 검증 메모

- BOJ 2748 공식 테스트 요약: `Results: 1/1 passed, 0 failed`
- BOJ 2748 수동 케이스 교차검증: BOJ 2748 수동 케이스에서 Python/C++ 출력이 완전히 일치한다.
- BOJ 2748 문서에서는 공식 로그와 수동 로그를 분리 저장해 회귀 시 원인 구간을 빠르게 좁힌다.
- 이번 수동 케이스는 "작은 N에서 초기값(F0,F1)과 점화식 적용 순서를 검증한다." 검증에 초점을 맞췄다.

## 재현 체크리스트

- [ ] BOJ 2748 기준으로 `make test`를 재실행했을 때 `Results: 1/1 passed, 0 failed` 패턴이 유지되는가?
- [ ] BOJ 2748 수동 케이스 입력을 재사용했을 때 Python/C++ 출력이 계속 일치하는가?
- [ ] BOJ 2748 기준으로 `approach.md`의 복잡도/정당성 설명이 관측 출력과 충돌하지 않는가?

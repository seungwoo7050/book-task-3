# Architecture Lab Y86 hand-in

## 이 디렉터리가 가르치는 것

이 디렉터리는 Architecture Lab의 실제 hand-in 성격 산출물을 모아 둡니다.
Part A 어셈블리, Part C `ncopy.ys`, Part B/C용 HCL patch logic가 여기에 있습니다.

## 누구를 위한 문서인가

- 공식 hand-in에 가까운 학습 산출물을 보고 싶은 학습자
- companion 모델과 별도로 실제 Y86 산출물을 확인하고 싶은 사람
- official verification과 연결되는 핵심 파일만 보고 싶은 사람

## 먼저 읽을 곳

1. [`../problem/README.md`](../problem/README.md)
2. [`../docs/README.md`](../docs/README.md)
3. `src/` 아래 Y86 파일과 `script/apply_hcl_patches.py`

## 디렉터리 구조

```text
y86/
  README.md
  src/
    sum.ys
    rsum.ys
    copy.ys
    ncopy.ys
  script/
    apply_hcl_patches.py
```

## 검증 방법

```bash
cd problem
make restore-official
make verify-official
```

최근 문서 기준 공식 Part C 결과:

- `Average CPE 9.16`
- `Score 26.8/60.0`

## 스포일러 경계

- 이 디렉터리에는 study-owned hand-in 산출물만 둡니다.
- 공식 simulator와 템플릿은 로컬 복원 경로로만 다룹니다.

## 포트폴리오로 확장하는 힌트

- 아키텍처 프로젝트는 "공식 hand-in 산출물"과 "학습용 companion 모델"을 나눠 보여 주면 훨씬 읽기 쉽습니다.

# Attack Lab 검증 기록

## 두 종류의 검증

이 프로젝트는 다음 둘을 나눠 검증합니다.

- 공개 self-study target 경계
- 저장소가 직접 작성한 companion verifier

## 공식 self-study target 검증

```bash
cd problem
make restore-official
make verify-official
```

2026-03-10 기준 기록:

- 공개 `target1` self-study handout에 대해 5개 phase가 통과한다
- 복원된 바이너리와 cookie 파일은 `problem/official/` 아래 로컬 전용 자산이다

## C companion 검증

```bash
cd c
make clean && make test
```

기록:

- phase 1~5의 payload 구조 검증 테스트 통과
- sample payload 파일 검증 통과

## C++ companion 검증

```bash
cd cpp
make clean && make test
```

기록:

- phase 1~5의 payload 구조 검증 테스트 통과
- sample payload 파일 검증 통과

## 현재 판단

공식 과제 경계와 공개 가능한 학습 산출물을 분리한 상태로,
두 검증 경로가 모두 유지되고 있습니다.

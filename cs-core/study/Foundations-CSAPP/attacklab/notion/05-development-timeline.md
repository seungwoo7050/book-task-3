# 05. 개발 타임라인

## 이 문서의 역할

이 문서는 `attacklab`을 새 환경에서 다시 세울 때 exploit dump 대신 어떤 순서로 공식 target과 companion verifier를 검증해야 하는지 보존하는 재현 문서입니다.
민감한 payload 내용보다 재현 가능한 작업 순서를 우선합니다.

## 권장 재현 순서

1. `problem/`에서 공개 self-study target과 verifier 도구를 복원한다.
2. 공식 `make verify-official`로 공개 target 경계를 먼저 확인한다.
3. `c/`, `cpp/` companion verifier를 차례대로 돌려 payload 구조 검증을 통과시킨다.
4. 마지막에 공개 정책을 다시 읽어 현재 문서에 민감한 값이 들어오지 않았는지 확인한다.

## 최소 명령

```bash
cd problem
make restore-official
make verify-official

cd ../c
make clean && make test

cd ../cpp
make clean && make test
```

## 성공 신호

- 공개 `target1` self-study handout 기준 5개 phase 검증이 통과한다.
- C/C++ companion verifier가 모두 sample payload와 phase별 구조 검증을 통과한다.
- `ctarget`, `rtarget`, `hex2raw`, `cookie`류 자산은 계속 `problem/official/` 아래 로컬 전용으로만 남는다.

## 재현이 어긋날 때 먼저 볼 곳

- `problem/README.md`: 공식 target 복원 경계
- `../docs/concepts/payload-models.md`: phase별 payload 모델
- `../docs/concepts/rop-and-relative-addressing.md`: 상대 주소 계산과 gadget 연결
- `../docs/references/publication-policy.md`: 공개 정책
- `../docs/references/verification.md`: 현재 검증 명령

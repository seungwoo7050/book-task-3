# 05. 개발 타임라인

## 이 문서의 역할

이 문서는 `bomblab`을 다시 분석할 때 어떤 순서로 공용 self-study target과 companion mini-bomb을 검증해야 하는지 압축해서 적어 둔 재현 문서입니다.
정답 덤프를 보관하는 문서가 아니라, 안전한 재현 경로를 보관하는 문서입니다.

## 권장 재현 순서

1. `problem/`에서 공개 self-study bomb 복원과 공식 검증 경로를 먼저 확인한다.
2. `c/` companion 구현을 테스트로 통과시킨다.
3. `cpp/` 구현도 같은 계약을 통과시키며 언어별 일관성을 맞춘다.
4. 마지막에 공개 범위가 흔들리지 않았는지 `publication-policy`를 다시 확인한다.

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

- 공개 self-study target 기준 공식 검증이 통과한다.
- C/C++ companion 테스트가 모두 통과한다.
- raw target-specific answer 파일을 현재 `notion/`이나 README에 추가하지 않는다.
- 필요하면 `../docs/references/verification.md`의 safe sample run 절차와 비교해 결과를 확인한다.

## 재현이 어긋날 때 먼저 볼 곳

- `problem/README.md`: 복원 자산과 공개 경계
- `../docs/concepts/reverse-engineering-workflow.md`: 브레이크포인트와 관찰 순서
- `../docs/references/publication-policy.md`: 공개 가능한 정보의 선
- `../docs/references/verification.md`: 현재 검증 명령

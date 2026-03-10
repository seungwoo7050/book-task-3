# 05. 개발 타임라인

## 이 문서의 역할

이 문서는 장문 회고가 아니라, 새 환경에서 `datalab`을 다시 끝까지 따라갈 때 필요한 순서와 성공 신호를 압축해서 적어 둔 재현 문서입니다.
2026-03-10 기준 작업본을 기준으로 정리했습니다.

## 권장 재현 순서

1. `problem/`에서 공식 handout을 복원하고 `dlc`와 `btest` 경로를 먼저 살린다.
2. `c/`에서 edge-case 테스트를 통과시킨다.
3. `cpp/`에서 같은 계약을 다시 검증해 언어별 일관성을 확인한다.
4. 마지막에 `docs/references/verification.md`와 현재 결과를 비교한다.

## 최소 명령

```bash
cd problem
make restore-official
make verify-official

cd ../c
make clean && make test

cd ../cpp/tests
g++ -std=c++20 -O1 -Wall -Werror -o test_bits_cpp test_bits.cpp ../src/bits.cpp
./test_bits_cpp
```

## 성공 신호

- 공식 `dlc`와 `btest -T 20`이 통과한다.
- C track에서 `55 / 55 edge-case tests passed`가 나온다.
- C++ track에서도 같은 edge-case 세트가 통과한다.
- 결과가 `../docs/references/verification.md`의 기록과 크게 어긋나지 않는다.

## 재현이 어긋날 때 먼저 볼 곳

- `problem/README.md`: 공식 handout 복원 경계
- `../docs/references/verification.md`: 현재 검증 명령과 기대 결과
- `c/tests/test_bits.c`, `cpp/tests/test_bits.cpp`: 경계값 테스트 기준점
- Docker/QEMU 환경 때문에 공식 검증이 느릴 수 있다는 점

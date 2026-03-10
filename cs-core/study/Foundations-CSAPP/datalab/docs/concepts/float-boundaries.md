# 부동소수점 퍼즐에서 먼저 분류해야 하는 경계

## 왜 정수 퍼즐과 따로 다뤄야 하는가

`floatScale2`, `floatFloat2Int`, `floatPower2`는 연산자 제한이 조금 풀리는 대신,
IEEE 754 비트 구조를 직접 해석해야 한다는 더 큰 요구를 줍니다.

여기서는 계산보다 분류가 먼저입니다.

## 가장 먼저 해야 할 일: 세 분류

모든 함수는 입력을 먼저 아래 셋 중 하나로 나눠 봐야 합니다.

- `exp == 0xFF`: NaN 또는 infinity
- `exp == 0`: zero 또는 denormalized
- 그 외: normalized

이 구분을 먼저 하지 않으면, 뒤 계산이 맞아도 특정 경계값에서 바로 틀립니다.

## `floatScale2`

핵심 질문은 "2배 했을 때 지수부를 바꿀지, fraction을 밀지"입니다.

- NaN, infinity: 그대로 반환
- denormalized: fraction을 왼쪽으로 한 칸 밀기
- normalized: exponent만 1 증가

이 함수는 수학 연산보다 상태 전이가 중요합니다.

## `floatFloat2Int`

핵심 질문은 "정수 범위를 벗어났는가"와 "유효 숫자를 어떻게 옮길 것인가"입니다.

- NaN, infinity, 범위 초과: `0x80000000u`
- 절댓값이 1보다 작음: `0`
- 그 외: 숨은 1을 복구한 뒤 exponent에 맞춰 shift

여기서는 부호 처리와 overflow 조기 판단이 가장 자주 실수나는 부분입니다.

## `floatPower2`

이 함수는 입력이 float 비트패턴이 아니라 정수 `x`라는 점이 다릅니다.
결국 `2.0^x`를 어떤 표현 영역으로 보낼지 판단해야 합니다.

- `x > 127`: infinity
- `-126 <= x <= 127`: normalized
- `-149 <= x < -126`: denormalized
- `x < -149`: underflow to zero

즉, exponent 범위를 먼저 잡고, 그다음 normalized/denormalized 표현을 분기하는 문제입니다.

## 꼭 기억할 값

- smallest denormal: `0x00000001`
- `1.0f`: `0x3F800000`
- `+inf`: `0x7F800000`
- quiet NaN 예시: `0x7FC00000`

이 값들은 디버깅할 때 가장 빨리 다시 보게 됩니다.

## 읽고 나서 바로 연결할 곳

- 정수 퍼즐 패턴: [`integer-patterns.md`](integer-patterns.md)
- 구현 경로: [`../../c/README.md`](../../c/README.md), [`../../cpp/README.md`](../../cpp/README.md)
- 실제 검증 결과: [`../references/verification.md`](../references/verification.md)

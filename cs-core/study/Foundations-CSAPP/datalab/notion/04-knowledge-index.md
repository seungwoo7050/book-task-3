# 04. 지식 인덱스

## 핵심 개념과 다시 볼 이유

- `INT_MIN`, `INT_MAX`, `-1`: overflow와 부호 전파를 가장 빨리 확인할 수 있는 기준점이다.
- 불리언을 전체 마스크로 바꾸는 패턴: `conditional`, `logicalNeg`, 범위 검사처럼 branchless 풀이가 필요한 곳에서 반복된다.
- `x + (~y + 1)`: 연산자 제약 안에서 뺄셈을 흉내 내는 기본 도구다.
- IEEE 754 분류: `floatScale2`, `floatFloat2Int`, `floatPower2`는 NaN, infinity, denormal 경계를 먼저 나누지 않으면 금방 흔들린다.
- 작은 상수로 넓은 마스크 조립: `0xAA`에서 `0xAAAAAAAA`를 만드는 감각은 operator budget 감각과 연결된다.

## 재현 중 막히면 먼저 확인할 것

- 정수 퍼즐 패턴: `../docs/concepts/integer-patterns.md`
- 부동소수점 경계: `../docs/concepts/float-boundaries.md`
- 실제 검증 명령: `../docs/references/verification.md`

## 이후 프로젝트와 연결되는 메모

- bit-level reasoning은 `bomblab`, `attacklab`, `archlab`에서도 그대로 이어진다.
- 경계값 테스트를 먼저 적어 두는 습관은 이후 모든 구현 README와 검증 문서 품질까지 끌어올린다.

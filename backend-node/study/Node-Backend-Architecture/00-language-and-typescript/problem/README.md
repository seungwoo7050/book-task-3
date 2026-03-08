# Problem

## 목표

백엔드 프레임워크에 들어가기 전에 TypeScript로 문제를 읽고,
함수와 타입을 설계하고, 비동기 코드와 에러 처리를 다룰 수 있어야 한다.

## 과제

1. 원시 문자열 태그 목록을 정규화해 중복 없는 slug 배열로 변환한다.
2. 불완전한 입력을 안전한 `NormalizedBook` 구조로 바꾼다.
3. 비동기 inventory client를 병렬 호출하되, 일부 실패가 전체 실패로 번지지 않게 처리한다.
4. CLI에서 받은 입력을 TypeScript 타입으로 검증해 사람이 읽기 좋은 카드 문자열로 출력한다.

## 제공 자료

- `problem/code/starter.ts`: 함수 시그니처와 타입 골격
- `problem/script/run-example.sh`: 예시 실행 명령

## 최소 성공 기준

- `normalizeTags`, `toNormalizedBook`, `fetchInventorySnapshot`, `formatBookCard`가 모두 동작한다.
- CLI가 필수 인자를 검증하고 정상 출력 또는 오류 코드를 반환한다.
- 테스트로 동기/비동기 경계를 모두 확인한다.

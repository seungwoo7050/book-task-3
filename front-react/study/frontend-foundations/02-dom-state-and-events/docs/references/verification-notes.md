# Verification Notes

## Unit Tests

- `parseQuery`와 `serializeQuery`가 URL 경계를 올바르게 유지하는지 확인한다.
- persisted state를 읽고 쓸 수 있는지 본다.
- query 때문에 보이지 않는 row가 생길 때 selection이 초기화되는지 확인한다.

## DOM Tests

- search와 filter 변경이 실제 URL에 반영되는지 확인한다.
- delegated click으로 selection과 inline edit가 수행되는지 본다.
- 편집 결과가 localStorage에 저장되는지 확인한다.

## E2E Tests

- URL query + persisted edit가 reload 뒤에도 살아 있는지 확인한다.
- keyboard-only로 row를 선택하고 제목을 수정한 뒤 Enter로 저장하는 흐름을 검증한다.

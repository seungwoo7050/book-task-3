# References

## 1. HTTP Semantics

- Title: HTTP Semantics
- URL: https://www.rfc-editor.org/rfc/rfc9110
- Checked date: 2026-03-07
- Why: 상태 코드와 method 의미를 다시 고정했다.
- Learned: 입문 단계에서도 `200`, `201`, `400`, `404`, `422`의 분리가 중요하다.
- Effect: 테스트 케이스를 상태 코드 구분 중심으로 작성했다.

## 2. `net/http` ServeMux Patterns

- Title: Routing Enhancements for Go 1.22
- URL: https://go.dev/blog/routing-enhancements
- Checked date: 2026-03-07
- Why: `GET /v1/tasks/{id}` 패턴 사용 근거를 확인했다.
- Learned: 표준 라이브러리만으로도 입문용 REST routing은 충분히 표현 가능하다.
- Effect: 외부 라우터 없이 `ServeMux` 패턴으로 구현했다.


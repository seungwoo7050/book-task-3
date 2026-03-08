# References

## 1. Prometheus Text Format

- Title: Exposition formats
- URL: https://prometheus.io/docs/instrumenting/exposition_formats/
- Checked date: 2026-03-07
- Why: `/metrics` 응답 형식을 단순하게 맞추기 위해 확인했다.
- Learned: 입문 단계에서는 full client library 없이도 핵심 개념을 보여줄 수 있다.
- Effect: plain text metrics endpoint를 직접 구현했다.

## 2. Slog Package

- Title: Package slog
- URL: https://pkg.go.dev/log/slog
- Checked date: 2026-03-07
- Why: structured logging 기본 인터페이스를 다시 확인했다.
- Learned: trace id 같은 운영 필드는 문자열 연결보다 필드로 남겨야 재사용성이 높다.
- Effect: 요청 로그에 `trace_id`, `method`, `path`를 남겼다.


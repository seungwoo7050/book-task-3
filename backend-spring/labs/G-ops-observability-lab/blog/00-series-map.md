# G-ops-observability-lab series map

이 시리즈는 `G-ops-observability-lab`을 "운영 기본기 다 갖춘 랩"으로 포장하지 않고, 실제로 존재하는 운영 표면과 문서상 주장 사이의 차이까지 같이 읽는다. JSON logging, trace header, Prometheus endpoint는 실제로 동작하지만, readiness는 custom endpoint와 actuator health가 서로 다른 의미를 갖고, CI는 workspace 안의 workflow 파일로 확인되지 않는다.

## 읽는 순서

1. [10-development-timeline.md](10-development-timeline.md)
   custom health, actuator health, ops summary, Prometheus scrape, compose/CI 근거를 순서대로 따라간다.

## 이 시리즈가 답하는 질문

- 현재 readiness는 무엇을 실제로 검사하고 무엇을 검사하지 않는가
- 운영 링크를 노출하는 것과 운영 상태를 증명하는 것은 어떻게 다른가
- 이 lab에서 진짜 코드 근거가 있는 운영 요소와 아직 문서 수준인 요소는 무엇인가

## 이번 보강에서 더 또렷하게 남긴 선

- 자동 테스트가 직접 잠그는 것은 custom `/health`의 `UP` 응답과 `/ops/summary`의 링크 문자열이다.
- `X-Trace-Id`, JSON log shape, `/actuator/health`와 custom ready의 의미 차이는 source와 manual boot run에서 더 강하게 확인된다.
- 그래서 이 랩의 observability 설명은 "전부 테스트됐다"가 아니라 "일부는 test-proven, 일부는 source/manual-proven"으로 읽는 편이 정확하다.

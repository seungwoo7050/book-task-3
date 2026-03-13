# G-ops-observability-lab Structure Outline

- 기존 blog 처리:
  - 기존 `blog/`가 없어 격리 대상이 없다.
- 시리즈 방향:
  - 운영성을 설정 모음이 아니라 앱이 노출하는 표면들의 묶음으로 복원한다.
- 작업 환경 반영:
  - macOS + VSCode 통합 터미널에서 `make test`, `make smoke`, Compose health 확인을 근거로 쓴다.
- 파일 계획:
  - `00-series-map.md`: 운영 랩의 범위와 근거를 고정한다.
  - `10-development-timeline.md`: scope 고정 -> health/trace/metrics/logging 구현 -> 테스트와 증명 범위 정리 순서로 쓴다.
- 반드시 강조할 것:
  - trace ID, JSON logging, Prometheus endpoint는 서로 연결된 운영 표면이다.
  - docs가 언급한 CI hooks와 현재 실제 파일 근거의 차이도 명시한다.

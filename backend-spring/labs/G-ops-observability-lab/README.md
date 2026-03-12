# G-ops-observability-lab

운영성을 capstone 부록이 아니라 백엔드 기본기로 다루는 랩입니다.

- 상태: `verified scaffold`
- 실행 진입점: [spring/README.md](spring/README.md)

## 문제 요약

- health, logging, metrics, CI는 구현이 끝난 뒤 붙는 장식이 아니라 백엔드가 스스로를 설명하는 방법입니다.
- 학습 레포에서도 "무엇을 관찰할 수 있는가"를 별도 주제로 남겨야 합니다.
- 상세 성공 기준과 제약은 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- health/readiness endpoint, JSON logging, trace ID propagation, Prometheus scrape target을 갖춘 랩을 만들었습니다.
- Compose와 GitHub Actions 수준의 운영 기본기를 코드와 문서로 남겼습니다.
- 다른 랩의 `global/` 코드가 왜 필요한지 설명하는 장소를 별도로 만들었습니다.

## 핵심 설계 선택

- full observability stack 과시보다 health/log/metrics/CI의 최소 세트를 먼저 고정했습니다.
- alert, dashboard, distributed tracing은 미완으로 남기고 현재 증명한 범위를 분명히 했습니다.
- 운영 문서를 capstone에 묻지 않고 독립 랩으로 분리했습니다.

## 검증

```bash
cd spring
make lint
make test
make smoke
docker compose up --build
```

마지막 기록된 실제 검증 결과는 [../../docs/verification-report.md](../../docs/verification-report.md)에 있습니다.

## 이번 단계에서 일부러 남긴 것

- alert rule과 dashboard 작성
- external log platform integration
- live AWS deployment or IaC

## 다음에 읽을 문서

- canonical problem statement: [problem/README.md](problem/README.md)
- 실행과 검증: [spring/README.md](spring/README.md)
- 현재 구현 범위와 단순화: [docs/README.md](docs/README.md)
- 학습 로그와 재현 기록: [notion/README.md](notion/README.md)

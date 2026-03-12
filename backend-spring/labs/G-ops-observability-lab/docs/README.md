# G-ops-observability-lab 설계 메모

이 문서는 운영 랩이 현재 어떤 기본기를 증명했고 어떤 운영 영역이 아직 비어 있는지 요약한다.

## 현재 구현 범위

- JSON logging과 trace ID header propagation
- health endpoint와 Prometheus scrape target
- Compose stack과 Prometheus 설정
- GitHub Actions validation workflow 개념 정리

## 의도적 단순화

- alert rule과 dashboard는 아직 없다
- 로그는 구조화되어 있지만 외부 플랫폼으로 보내지 않는다
- AWS 배포는 방향 문서이지 live infrastructure는 아니다

## 다음 개선 후보

- alert 예시와 dashboard 제안 추가
- AWS deployment asset 또는 IaC 작성
- `/actuator/prometheus`까지 확인하는 smoke 확장

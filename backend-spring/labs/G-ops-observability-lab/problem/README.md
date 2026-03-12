# G-ops-observability-lab 문제 정의

운영성을 capstone의 부록이 아니라 독립 학습 주제로 분리해, 백엔드가 스스로를 관찰 가능하게 만드는 최소 기준을 다룬다.

## 성공 기준

- health/readiness, JSON logging, trace ID, Prometheus scrape target이 존재한다.
- Compose와 CI가 "운영 기본기"로서 어떤 역할을 하는지 설명할 수 있다.
- 현재 증명한 범위와 아직 미완인 운영 영역이 문서에 분리되어 있다.

## 이번 단계에서 다루지 않는 것

- alert rule과 dashboard 작성
- 외부 log platform integration
- live AWS deployment와 IaC

이 디렉터리는 구현보다는 canonical problem statement와 범위 선언을 담당한다.

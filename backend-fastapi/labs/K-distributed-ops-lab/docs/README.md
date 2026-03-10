# K-distributed-ops-lab 문서 지도

이 문서는 “다중 서비스 구조도 운영 질문에 답할 수 있어야 한다”는 관점에서 K 랩을 읽게 하는 개념 지도다. 기능 추가보다 live/ready, JSON 로그, 최소 metrics, Compose health matrix, AWS target shape 문서가 먼저 등장하는 이유를 설명한다.

## 먼저 보면 좋은 질문

- 서비스별 readiness는 무엇을 확인해야 하는가
- request id와 metrics는 어떤 운영 질문에 답하는가
- target shape 문서는 어디까지 사실이고 어디부터 가정인가
- gateway health와 내부 서비스 health를 왜 같은 의미로 보면 안 되는가

## 이 문서에서 중심으로 보는 구조

- 모든 서비스는 `/health/live`, `/health/ready`를 가진다.
- gateway public health와 내부 서비스 ready는 다른 질문에 답한다.
- JSON 로그는 `service_name`, `request_id`를 중심으로 최소 correlation을 제공한다.
- AWS 문서는 “이렇게 배치할 수 있다”는 target shape이며, 실제 배포 완료 선언이 아니다.

## 읽고 나면 설명할 수 있어야 하는 것

- 분산 구조에서 health endpoint가 늘어나는 이유
- JSON 로그와 metrics의 최소 기준
- Compose health matrix와 AWS 문서의 역할
- 왜 운영성 문서도 학습 저장소의 핵심 산출물인지

## 함께 보면 좋은 문서

- [문제 정의](../problem/README.md)
- [FastAPI 실행 문서](../fastapi/README.md)
- [AWS target shape](aws-deployment.md)
- [학습 노트](../notion/README.md)

# G-ops-lab 설계 문서

이 폴더는 G-ops-lab의 설계 설명을 모아 둔 곳입니다. 실행 순서보다 왜 이런 경계를 택했고 무엇을 설명해야 하는지를 먼저 정리합니다.

## 이 문서에서 먼저 볼 질문

- liveness와 readiness는 왜 분리해야 하는가
- "최소 metrics"는 어떤 운영 질문에 답해야 하는가
- 배포 문서는 어디까지 사실이고 어디부터 가정인가

## 읽고 나면 설명할 수 있어야 하는 것

- health endpoint 설계 기준
- CI와 로컬 Compose 검증의 역할 차이
- AWS target shape 문서를 읽는 방법

## 역할이 다른 관련 문서

- [문제 정의](../problem/README.md)
- [FastAPI 실행 문서](../fastapi/README.md)
- [AWS 배포 문서](aws-deployment.md)
- [현재 학습 노트](../notion/README.md)

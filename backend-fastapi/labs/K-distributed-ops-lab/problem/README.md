# 문제 정의

## 문제

MSA 구조를 실행만 하는 것으로 끝내지 않고, 서비스별 health, JSON 로그, 최소 metrics, target shape 문서를 함께 설명해야 한다. 이 랩은 운영성을 별도 학습 주제로 분리한다.

## 성공 기준

- gateway와 내부 서비스가 각각 `/health/live`, `/health/ready`, `/ops/metrics`를 제공한다.
- request id가 로그 문맥과 응답 헤더에 남는다.
- AWS target shape 문서가 실제 배포 완료처럼 쓰이지 않는다.

## 제외 범위

- 실제 클라우드 배포 자동화
- trace backend
- log shipping

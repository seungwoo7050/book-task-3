# G-ops-lab

이 랩은 기능보다 운영 가능성을 설명하는 데 초점을 맞춥니다. health/readiness, metrics, CI, 배포 문서를 통해 "이 백엔드를 어떻게 믿고 실행할 것인가"를 최소 단위로 다룹니다.

## 이 랩에서 배우는 것

- liveness와 readiness의 구분
- 구조화 로그
- 최소 metrics endpoint
- Compose 기반 로컬 부팅 확인
- CI와 배포 문서의 역할

## 선수 지식

- FastAPI 애플리케이션 수명주기
- Docker Compose 기본
- 운영성 문서가 왜 코드만큼 중요한지에 대한 감각

## 구현 범위

- live / ready health endpoint
- request-count metrics surface
- JSON 로그
- GitHub Actions 기반 검증 흐름
- AWS target shape 문서

## 일부러 단순화한 점

- observability stack 전체를 붙이지 않고 최소 surface만 남깁니다.
- AWS는 실제 배포 자동화가 아니라 문서 수준 target shape로 설명합니다.

## 실행 방법

1. [problem/README.md](problem/README.md)로 운영성 범위를 읽습니다.
2. [fastapi/README.md](fastapi/README.md)에서 가장 작은 실행 경로를 확인합니다.
3. [docs/README.md](docs/README.md)와 [docs/aws-deployment.md](docs/aws-deployment.md)를 읽고 운영 문서의 역할을 정리합니다.

## 검증 방법

- `cd fastapi && make lint`
- `cd fastapi && make test`
- `cd fastapi && make smoke`
- `cd fastapi && docker compose up --build`

## 추천 학습 순서

1. health와 readiness를 왜 구분하는지 먼저 정리합니다.
2. metrics와 로그가 어떤 운영 질문에 답하는지 확인합니다.
3. 마지막으로 CI와 AWS 문서가 어디까지를 보장하지 않는지도 함께 읽습니다.

## 포트폴리오로 확장하려면

- Prometheus/Grafana, trace, structured log shipping으로 확장할 수 있습니다.
- IaC를 추가하더라도 "문서 수준 가정"과 "실제 검증 완료"를 구분해야 합니다.
- 포트폴리오 README에는 기능보다도 운영 기준과 실패 관찰 가능성을 먼저 적는 편이 좋습니다.

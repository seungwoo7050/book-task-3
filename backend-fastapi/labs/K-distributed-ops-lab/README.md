# K-distributed-ops-lab

MSA 구조를 실행만 하는 데서 끝내지 않고, 서비스별 health, metrics, JSON 로그, target shape 문서까지 설명하는 운영성 랩입니다.

## 이 랩에서 배우는 것

- 서비스별 live / ready
- request id가 포함된 JSON 로그
- 최소 metrics surface
- Compose health matrix와 AWS target shape

## 선수 지식

- [J-edge-gateway-lab](../J-edge-gateway-lab/README.md)
- 운영 문서가 코드만큼 중요한 이유

## 구현 범위

- 서비스별 health / metrics
- gateway 포함 Compose health matrix
- AWS target shape 문서

## 일부러 단순화한 점

- 실제 클라우드 배포 자동화와 IaC는 제외합니다.
- trace backend와 log shipping은 붙이지 않습니다.

## 실행 방법

1. [problem/README.md](problem/README.md)를 읽습니다.
2. [fastapi/README.md](fastapi/README.md)에서 전체 스택을 실행합니다.
3. [docs/README.md](docs/README.md)와 [notion/README.md](notion/README.md)로 운영 기준을 정리합니다.

## 검증 방법

- `cd fastapi && make lint`
- `cd fastapi && make test`
- `cd fastapi && make smoke`
- `cd fastapi && docker compose up --build`

## 추천 학습 순서

1. 먼저 live / ready 차이를 서비스별로 적습니다.
2. metrics와 request id가 어떤 운영 질문에 답하는지 봅니다.
3. 마지막으로 AWS 문서가 어디까지 사실이고 어디부터 가정인지 읽습니다.

## 포트폴리오로 확장하려면

- trace, log shipping, SLO 문서를 붙일 수 있습니다.
- target shape와 실제 검증 완료를 엄격히 분리해 적는 습관이 중요합니다.

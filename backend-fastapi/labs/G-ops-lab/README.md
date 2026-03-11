# G-ops-lab

이 랩은 기능보다 운영 가능성을 설명하는 데 초점을 맞춥니다. health/readiness, metrics, CI, 배포 문서를 통해 "이 백엔드를 어떻게 믿고 실행할 것인가"를 최소 단위로 다룹니다.

## 문제 요약

- 기능은 단순해도, 백엔드가 어떻게 살아 있는지 확인하고 어떻게 배포 가정을 설명할지 정리해야 합니다. health check, readiness, metrics, CI, 배포 문서는 개발용 API와 별개의 운영성 문제입니다.
- live / ready health endpoint가 구분되어야 합니다.
- 요청 수 같은 최소 metrics surface가 있어야 합니다.
- 상세 성공 기준과 제외 범위는 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- live / ready health endpoint
- request-count metrics surface
- JSON 로그
- GitHub Actions 기반 검증 흐름
- AWS target shape 문서

## 핵심 설계 선택

- liveness와 readiness의 구분
- 구조화 로그
- 최소 metrics endpoint
- observability stack 전체를 붙이지 않고 최소 surface만 남깁니다.
- AWS는 실제 배포 자동화가 아니라 문서 수준 target shape로 설명합니다.

## 검증

```bash
make lint
make test
make smoke
docker compose up --build
```

- 실행과 환경 설명은 [fastapi/README.md](fastapi/README.md)에서 다룹니다.
- 마지막 기록된 실제 검증 결과는 [../../docs/verification-report.md](../../docs/verification-report.md)에 있습니다.

## 제외 범위

- 풀 observability stack 구축
- IaC로 실제 인프라를 생성하는 자동화
- 장시간 부하 테스트와 장애 주입 실험

## 다음 랩 또는 비교 대상

- 다음 단계는 [workspace-backend](../../capstone/workspace-backend/README.md)입니다.
- 설계 설명은 [docs/README.md](docs/README.md), 학습 로그는 [notion/README.md](notion/README.md), 실행 진입점은 [fastapi/README.md](fastapi/README.md)에서 읽습니다.

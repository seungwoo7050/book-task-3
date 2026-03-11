# K-distributed-ops-lab

MSA 구조를 실행만 하는 데서 끝내지 않고, 서비스별 health, metrics, JSON 로그, target shape 문서까지 설명하는 운영성 랩입니다.

## 문제 요약

- MSA 구조를 실행만 하는 것으로 끝내지 않고, 서비스별 health, JSON 로그, 최소 metrics, target shape 문서를 함께 설명해야 한다. 이 랩은 운영성을 별도 학습 주제로 분리한다.
- gateway와 내부 서비스가 각각 `/health/live`, `/health/ready`, `/ops/metrics`를 제공한다.
- request id가 로그 문맥과 응답 헤더에 남는다.
- 상세 성공 기준과 제외 범위는 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- 서비스별 health / metrics
- gateway 포함 Compose health matrix
- AWS target shape 문서

## 핵심 설계 선택

- 서비스별 live / ready
- request id가 포함된 JSON 로그
- 최소 metrics surface
- 실제 클라우드 배포 자동화와 IaC는 제외합니다.
- trace backend와 log shipping은 붙이지 않습니다.

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

- 실제 클라우드 배포 자동화
- trace backend
- log shipping

## 다음 랩 또는 비교 대상

- 다음 단계는 [workspace-backend-v2-msa](../../capstone/workspace-backend-v2-msa/README.md)입니다.
- 설계 설명은 [docs/README.md](docs/README.md), 학습 로그는 [notion/README.md](notion/README.md), 실행 진입점은 [fastapi/README.md](fastapi/README.md)에서 읽습니다.

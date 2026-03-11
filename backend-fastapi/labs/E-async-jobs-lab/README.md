# E-async-jobs-lab

요청-응답 API 뒤에 숨어 있는 비동기 작업 경계를 따로 떼어 보는 랩입니다. Celery와 Redis를 붙여 백그라운드 작업을 실행하되, 핵심은 outbox와 idempotency를 통해 "안전하게 넘기는 법"을 설명하는 데 있습니다.

## 문제 요약

- 알림이나 후처리처럼 요청-응답 경로에서 바로 끝내기 어려운 작업을 안전하게 뒤로 넘겨야 합니다. 이때 중복 요청, 재시도, 작업 유실을 어떻게 다룰지 명시적인 경계가 필요합니다.
- 작업 enqueue 요청이 idempotency key를 받아야 합니다.
- outbox를 통해 저장과 전달 사이의 경계가 설명 가능해야 합니다.
- 상세 성공 기준과 제외 범위는 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- 알림 작업 enqueue API
- outbox 저장과 drain 흐름
- Celery worker 실행
- 재시도 가능한 상태 모델

## 핵심 설계 선택

- 비동기 enqueue와 실제 실행의 분리
- outbox handoff
- idempotency key
- 대규모 분산 메시징 대신 로컬 Redis + Celery 조합으로 제한합니다.
- 알림 도메인은 일반화된 예시로 유지합니다.

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

- 대규모 메시징 시스템 비교
- 고급 스케줄링과 운영 대시보드
- 실서비스 수준의 분산 장애 복구 실험

## 다음 랩 또는 비교 대상

- 다음 단계는 [F-realtime-lab](../F-realtime-lab/README.md)입니다.
- 설계 설명은 [docs/README.md](docs/README.md), 학습 로그는 [notion/README.md](notion/README.md), 실행 진입점은 [fastapi/README.md](fastapi/README.md)에서 읽습니다.

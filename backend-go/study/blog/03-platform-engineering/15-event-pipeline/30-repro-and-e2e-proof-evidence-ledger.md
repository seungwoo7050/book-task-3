# 15 Event Pipeline Evidence Ledger

## 30 repro-and-e2e-proof

- 시간 표지: 9단계: E2E 테스트 -> 10단계: 빌드 및 검증
- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/e2e/pipeline_flow_test.go`, `solution/go/Makefile`
- 처음 가설: consumer idempotency를 별도 책임으로 두어 relay와 downstream 처리의 경계를 선명하게 했다.
- 실제 조치: 전체 흐름: 구매 → outbox INSERT → relay 발행 → consumer 처리

CLI:

```bash
make e2e
# RUN_E2E=1 DATABASE_URL=... KAFKA_BROKERS=... go test ./e2e -v -count=1

make build
make test
make test-race
make smoke
```

- 검증 신호:
- make smoke
- 2026-03-08 기준 `make -C problem build`가 통과했다.
- 2026-03-08 기준 `make -C problem test`가 통과했다.
- 2026-03-08 기준 `cd solution/go && make repro`가 통과했다.
- 핵심 코드 앵커: `solution/go/e2e/pipeline_flow_test.go`
- 새로 배운 것: consumer는 at-least-once 환경을 가정하고 중복 처리를 견뎌야 한다.
- 다음: 선택 검증이나 운영 환경에서만 가능한 경계를 짧게 남긴다.

# 14 Cockroach TX Evidence Ledger

## 30 repro-and-e2e-proof

- 시간 표지: 10단계: E2E 테스트 -> 11단계: 빌드 및 검증
- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/e2e/purchase_flow_test.go`, `solution/go/Makefile`
- 처음 가설: HTTP handler, service, repo를 나눠 정합성 로직이 어디에 있어야 하는지 드러냈다.
- 실제 조치: `RUN_E2E=1` 환경변수로 게이트. CI에서는 DB가 있을 때만 실행.

CLI:

```bash
# CockroachDB 연동 통합 테스트
make e2e
# 내부: RUN_E2E=1 DATABASE_URL=... go test ./e2e -v -count=1

make build          # bin/server 바이너리 생성
make test           # 단위 테스트
make test-race      # -race 플래그
make smoke          # = make e2e
```

- 검증 신호:
- make smoke          # = make e2e
- 2026-03-08 기준 `make -C problem build`가 통과했다.
- 2026-03-08 기준 `make -C problem test`가 통과했다.
- 2026-03-08 기준 `cd solution/go && make repro`가 통과했다.
- 핵심 코드 앵커: `solution/go/e2e/purchase_flow_test.go`
- 새로 배운 것: Cockroach류 분산 SQL은 serialization failure를 애플리케이션 레벨에서 재시도하게 요구할 수 있다.
- 다음: 선택 검증이나 운영 환경에서만 가능한 경계를 짧게 남긴다.

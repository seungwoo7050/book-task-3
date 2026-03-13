# 18 Workspace SaaS API Evidence Ledger

## 50 repro-demo-and-portfolio-proof

- 시간 표지: Phase 12 — 전체 재현성 검증 -> Phase 13 — Demo Capture
- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `scripts/demo_capture.sh`
- 처음 가설: worker와 API를 바이너리 수준에서 분리해 async notification과 web request 경계를 명확히 했다.
- 실제 조치: 한 명령으로 전체 검증: `scripts/demo_capture.sh` — 프레젠테이션용 아티팩트 생성. 실제 API 호출의 요청/응답을 캡처하여 문서화에 활용.

CLI:

```bash
make repro

make up → make migrate → make seed → make test → make test-race → make e2e → make smoke
```

- 검증 신호:
- make up → make migrate → make seed → make test → make test-race → make e2e → make smoke
- `go test ./...` 통과
- `make e2e` 통과
- `make smoke` 통과
- [presentation-assets/demo-2026-03-07](presentation-assets/demo-2026-03-07)는
- 핵심 코드 앵커: `solution/go/scripts/smoke.sh`
- 새로 배운 것: 대표작의 검증 가치는 API 문서, e2e, smoke가 같이 돌아갈 때 생긴다.
- 다음: 선택 검증이나 운영 환경에서만 가능한 경계를 짧게 남긴다.

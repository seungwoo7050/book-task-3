# 18 Workspace SaaS API Structure

## 이 글이 답할 질문

- 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- worker와 API를 바이너리 수준에서 분리해 async notification과 web request 경계를 명확히 했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `05-portfolio-projects/18-workspace-saas-api` 안에서 `50-repro-demo-and-portfolio-proof.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: Phase 12 — 전체 재현성 검증 -> Phase 13 — Demo Capture
- 세션 본문: `scripts/demo_capture.sh` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/scripts/smoke.sh`
- 코드 앵커 2: `solution/go/e2e/workspace_flow_test.go`
- 코드 설명 초점: 이 테스트나 재현 스크립트는 프로젝트의 공개 표면을 말이 아니라 입력과 결과로 고정한다. 최종 글에서 이 증거를 빼면 구현은 보여도 완료 기준은 흐려진다.
- 개념 설명: 대표작의 검증 가치는 API 문서, e2e, smoke가 같이 돌아갈 때 생긴다.
- 마지막 단락: 선택 검증이나 운영 환경에서만 가능한 경계를 짧게 남긴다.

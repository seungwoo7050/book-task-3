# 17 Game Store Capstone Structure

## 이 글이 답할 질문

- 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- OAuth나 마이크로서비스는 제외하고 거래 일관성과 재현성에 집중했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `04-capstone/17-game-store-capstone` 안에서 `40-repro-and-e2e-hardening.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 12단계: E2E 테스트 -> 13단계: 전체 검증
- 세션 본문: `solution/go/e2e/purchase_flow_test.go, solution/go/Makefile` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/e2e/purchase_flow_test.go`
- 코드 앵커 2: `solution/go/Makefile`
- 코드 설명 초점: 이 테스트나 재현 스크립트는 프로젝트의 공개 표면을 말이 아니라 입력과 결과로 고정한다. 최종 글에서 이 증거를 빼면 구현은 보여도 완료 기준은 흐려진다.
- 개념 설명: e2e 테스트는 unit test가 놓치는 통합 문제를 빠르게 드러낸다.
- 마지막 단락: 선택 검증이나 운영 환경에서만 가능한 경계를 짧게 남긴다.

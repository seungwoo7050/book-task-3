# 14 Cockroach TX Structure

## 이 글이 답할 질문

- 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- HTTP handler, service, repo를 나눠 정합성 로직이 어디에 있어야 하는지 드러냈다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `03-platform-engineering/14-cockroach-tx` 안에서 `30-repro-and-e2e-proof.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 10단계: E2E 테스트 -> 11단계: 빌드 및 검증
- 세션 본문: `solution/go/e2e/purchase_flow_test.go, solution/go/Makefile` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/e2e/purchase_flow_test.go`
- 코드 앵커 2: `solution/go/Makefile`
- 코드 설명 초점: 이 테스트나 재현 스크립트는 프로젝트의 공개 표면을 말이 아니라 입력과 결과로 고정한다. 최종 글에서 이 증거를 빼면 구현은 보여도 완료 기준은 흐려진다.
- 개념 설명: Cockroach류 분산 SQL은 serialization failure를 애플리케이션 레벨에서 재시도하게 요구할 수 있다.
- 마지막 단락: 선택 검증이나 운영 환경에서만 가능한 경계를 짧게 남긴다.

# 05 HTTP REST Basics Structure

## 이 글이 답할 질문

- 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- idempotency는 완성형 분산 설계가 아니라 “왜 필요한가”를 보여 주는 최소 형태로 제한했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `01-backend-core/05-http-rest-basics` 안에서 `20-validation-pagination-and-idempotency.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: Phase 4: CLI 서버 -> Phase 5: 테스트 -> Phase 6: 문서 및 최종 검증
- 세션 본문: `solution/go/cmd/server/main.go, solution/go/internal/api/api_test.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/internal/api/api_test.go`
- 코드 앵커 2: `solution/go/internal/api/api.go`
- 코드 설명 초점: 이 테스트나 재현 스크립트는 프로젝트의 공개 표면을 말이 아니라 입력과 결과로 고정한다. 최종 글에서 이 증거를 빼면 구현은 보여도 완료 기준은 흐려진다.
- 개념 설명: 생성 성공은 `201`, 같은 idempotency key 재시도는 `200`으로 분리했다.
- 마지막 단락: persistence와 인증은 이 과제 범위에 포함하지 않았다.

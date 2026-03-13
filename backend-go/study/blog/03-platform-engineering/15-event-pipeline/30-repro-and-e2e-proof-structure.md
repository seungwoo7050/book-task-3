# 15 Event Pipeline Structure

## 이 글이 답할 질문

- 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- consumer idempotency를 별도 책임으로 두어 relay와 downstream 처리의 경계를 선명하게 했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `03-platform-engineering/15-event-pipeline` 안에서 `30-repro-and-e2e-proof.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 9단계: E2E 테스트 -> 10단계: 빌드 및 검증
- 세션 본문: `solution/go/e2e/pipeline_flow_test.go, solution/go/Makefile` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/e2e/pipeline_flow_test.go`
- 코드 앵커 2: `solution/go/Makefile`
- 코드 설명 초점: 이 블록은 병렬성과 보호 정책을 아이디어가 아니라 코드 invariant로 바꾼다. goroutine, channel, token을 어떤 경계로 묶었는지가 여기서 드러난다.
- 개념 설명: consumer는 at-least-once 환경을 가정하고 중복 처리를 견뎌야 한다.
- 마지막 단락: 선택 검증이나 운영 환경에서만 가능한 경계를 짧게 남긴다.

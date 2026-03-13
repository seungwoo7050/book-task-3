# 13 Distributed Log Core Structure

## 이 글이 답할 질문

- mmap index와 segment rotation을 테스트 및 benchmark와 함께 정리했다.
- 파일 포맷과 segment lifecycle을 먼저 구현해 분산 복제 이전의 로컬 불변식을 학습하게 했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `02-distributed-systems/13-distributed-log-core` 안에서 `20-log-abstraction-and-rotation.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 5단계: Log 구현 (다중 Segment 관리) -> 6단계: 에러 정의
- 세션 본문: `log/log.go, log/errors.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/log/log.go`
- 코드 앵커 2: `solution/go/log/index.go`
- 코드 설명 초점: 이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.
- 개념 설명: index는 logical offset을 물리 위치로 빠르게 찾기 위한 보조 구조다.
- 마지막 단락: 다음 글에서는 `30-tests-and-bench-evidence.md`에서 이어지는 경계를 다룬다.

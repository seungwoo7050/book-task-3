# 13 Distributed Log Core Structure

## 이 글이 답할 질문

- length-prefixed store와 fixed-width index를 직접 구현해야 한다.
- Kafka형 시스템을 한 번에 복제하지 않고 append-only log 핵심 구조만 분리했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `02-distributed-systems/13-distributed-log-core` 안에서 `10-store-index-and-segment-core.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 1단계: 프로젝트 초기화 -> 2단계: Store 구현 (append-only 파일) -> 3단계: Index 구현 (mmap 기반) -> 4단계: Segment 구현 (Store + Index 조합)
- 세션 본문: `log/store.go, log/index.go, log/segment.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/log/store.go`
- 코드 앵커 2: `solution/go/log/segment.go`
- 코드 설명 초점: 이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.
- 개념 설명: store는 레코드 바이트를 순차 append하는 역할이다.
- 마지막 단락: 다음 글에서는 `20-log-abstraction-and-rotation.md`에서 이어지는 경계를 다룬다.

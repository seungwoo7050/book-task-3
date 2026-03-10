# 01-rpc-framing — notion 폴더 가이드

이 폴더는 RPC Framing 프로젝트의 학습 과정과 설계 사고를 기록한 문서 모음입니다.

## 문서 구성

| 문서 | 내용 | 언제 읽으면 좋은가 |
|------|------|-------------------|
| [essay.md](essay.md) | TCP 바이트 스트림 위에 메시지 경계와 RPC를 쌓아 올리는 과정을 서사적으로 풀어낸 에세이 | 네트워크 프로토콜 계층화의 "왜"와 "어떻게"를 이해하고 싶을 때 |
| [timeline.md](timeline.md) | 프로젝트 개발의 전체 과정을 시간순으로 재현한 타임라인 | 동일한 프로젝트를 처음부터 따라 구현하고 싶을 때 |

## 프로젝트 한 줄 요약

4바이트 big-endian length prefix로 TCP 스트림에 메시지 경계를 복원하고, correlation ID 기반 pending call map으로 동시 RPC 요청을 처리하는 클라이언트-서버를 구현한다.

## 키워드

`TCP` · `length-prefix-framing` · `RPC` · `correlation-id` · `pending-call-map` · `concurrent-requests` · `timeout` · `split-chunk`

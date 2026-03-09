# 07-domain-events — 읽기 가이드

## 이 폴더의 구성

| 파일 | 설명 | 추천 독자 |
|------|------|-----------|
| **essay.md** | 도메인 이벤트로 side effect를 분리하는 과정, EventEmitter vs EventEmitter2 비교를 서사적으로 풀어낸 에세이 | 이벤트 기반 아키텍처의 동기와 설계 판단을 이해하고 싶은 독자 |
| **timeline.md** | EventBus 구현부터 이벤트 리스너 테스트까지의 개발 과정을 시간순 정리 | 직접 따라 만들거나, 이벤트 시스템의 배선 과정을 알고 싶은 독자 |

## 추천 읽기 순서

1. **essay.md** — 왜 Service에서 side effect를 분리해야 하는지, 두 레인(EventEmitter / @nestjs/event-emitter)의 접근법 차이를 먼저 파악한다.
2. **timeline.md** — EventBus 생성, 이벤트 타입 정의, 리스너 등록, 테스트 격리 등 소스 코드만으로는 보이지 않는 순서를 확인한다.
3. **소스 코드** — `events/` 디렉토리와 변경된 `book.service.ts`를 중심으로 읽는다.

## 관련 프로젝트

- **06-persistence-and-repositories**: 이전 프로젝트, 이벤트를 발행할 영속 계층의 기반
- **08-production-readiness**: 다음 프로젝트, 이벤트 로그를 포함한 운영 수준 로깅·모니터링

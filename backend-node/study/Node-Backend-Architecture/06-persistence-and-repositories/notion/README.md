# 06-persistence-and-repositories — 읽기 가이드

## 이 폴더의 구성

| 파일 | 설명 | 추천 독자 |
|------|------|-----------|
| **essay.md** | in-memory에서 SQLite로의 전환, raw SQL vs ORM 비교를 서사적으로 풀어낸 에세이 | 영속 계층 설계의 맥락과 판단 근거를 이해하고 싶은 독자 |
| **timeline.md** | 프로젝트 셋업부터 native 빌드, 테스트 격리까지의 개발 과정을 시간순으로 정리 | 직접 따라 만들거나, 소스 코드에 보이지 않는 CLI 작업을 알고 싶은 독자 |

## 추천 읽기 순서

1. **essay.md** — 왜 영속 계층이 필요한지, Express(raw SQL)와 NestJS(TypeORM) 두 경로가 같은 문제를 어떻게 다르게 해결하는지를 먼저 파악한다.
2. **timeline.md** — better-sqlite3 native 빌드 과정과 테스트 격리 전략 등 소스 코드만으로는 보이지 않는 개발 과정을 확인한다.
3. **소스 코드** — essay와 timeline에서 언급한 파일들을 직접 열어 구조를 확인한다.

## 관련 프로젝트

- **05-auth-and-authorization**: 이전 프로젝트, 인증·인가 후 데이터를 영속하는 자연스러운 다음 단계
- **07-domain-events**: 다음 프로젝트, 영속된 데이터 위에 도메인 이벤트를 발행하는 패턴
- **docs/native-sqlite-recovery.md**: better-sqlite3 native 빌드 실패 시 공통 복구 가이드

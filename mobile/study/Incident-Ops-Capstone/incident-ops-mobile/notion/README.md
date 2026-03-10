# Incident Ops Mobile (Contract Harness) — Notion 문서 안내

이 디렉터리는 **Incident Ops Mobile** 프로젝트의 학습 기록을 블로그형 에세이로 정리한 공간이다.
인시던트 관리 시스템의 공유 DTO 계약(contract)을 React Native 모바일 클라이언트에서 올바르게 해석하고,
역할 기반 워크플로우(ack → request-resolution → approve/reject)를 하네스로 검증하는 과정을 담고 있다.

이 프로젝트는 **시스템 경계(system boundary)에서 멈추는** contract harness다.
완성된 프로덕트 UX, 오프라인 지원, 포트폴리오 패키징은 별도 프로젝트인 `incident-ops-mobile-client`에서 다룬다.

---

## 읽는 순서

| 순서 | 파일 | 핵심 내용 |
|------|------|-----------|
| 1 | `00-problem-framing.md` | 왜 contract harness가 필요한지, 시스템 아키텍처 |
| 2 | `01-approach-log.md` | 계약 정의 → harness model → UI → 테스트 구현 과정 |
| 3 | `02-debug-log.md` | 역할 전환, 상태 전이, replay 디버깅 기록 |
| 4 | `03-retrospective.md` | contract-first 설계에서 얻은 교훈과 회고 |
| 5 | `04-knowledge-index.md` | 소스 파일 맵, 계약 타입, 워크플로우 참조 |
| 6 | `05-development-timeline.md` | CLI 명령, 서버 테스트, e2e demo 실행 기록 |

## 목적별 바로가기

- **"이 프로젝트가 뭘 하는 건지 빠르게 파악하고 싶다"** → `00-problem-framing.md`
- **"구현 흐름을 따라가며 배우고 싶다"** → `01-approach-log.md`
- **"특정 에러나 이슈 해결법을 찾고 싶다"** → `02-debug-log.md`
- **"설계 판단의 이유가 궁금하다"** → `03-retrospective.md`
- **"소스 파일 위치나 의존성을 빠르게 찾고 싶다"** → `04-knowledge-index.md`
- **"환경 세팅이나 CLI 명령 순서를 알고 싶다"** → `05-development-timeline.md`

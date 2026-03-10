# Navigation Patterns — Notion 문서 안내

이 디렉터리는 **Navigation Patterns** 프로젝트의 학습 기록을 블로그형 에세이로 정리한 공간이다.
React Navigation v7 기반으로 Stack, Tab, Drawer, Deep Linking 네 가지 네비게이션 패턴을 하나의 앱 안에 중첩 구성하고,
TypeScript 타입 안전성까지 확보하는 전 과정을 담고 있다.

---

## 읽는 순서

| 순서 | 파일 | 핵심 내용 |
|------|------|-----------|
| 1 | `00-problem-framing.md` | 왜 네비게이션 중첩 구조를 학습해야 하는지, 문제 정의와 설계 방향 |
| 2 | `01-approach-log.md` | Stack → Tab → Drawer → Deep Link 순서로 쌓아 올린 구현 과정 |
| 3 | `02-debug-log.md` | 중첩 navigator 간 dispatch, deep link state hydration 등 디버깅 기록 |
| 4 | `03-retrospective.md` | 네비게이션 아키텍처 설계에서 얻은 교훈과 회고 |
| 5 | `04-knowledge-index.md` | 소스 파일 맵, 의존성 목록, 타입 정의 빠른 참조 |
| 6 | `05-development-timeline.md` | CLI 명령, 패키지 설치, 시뮬레이터 테스트 등 코드 밖의 작업 기록 |

## 목적별 바로가기

- **"이 프로젝트가 뭘 하는 건지 빠르게 파악하고 싶다"** → `00-problem-framing.md`
- **"구현 흐름을 따라가며 배우고 싶다"** → `01-approach-log.md`
- **"특정 에러나 이슈 해결법을 찾고 싶다"** → `02-debug-log.md`
- **"설계 판단의 이유가 궁금하다"** → `03-retrospective.md`
- **"소스 파일 위치나 의존성을 빠르게 찾고 싶다"** → `04-knowledge-index.md`
- **"환경 세팅이나 CLI 명령 순서를 알고 싶다"** → `05-development-timeline.md`

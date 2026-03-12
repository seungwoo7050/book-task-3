# Native Modules — Notion 문서 안내

이 디렉터리는 **Native Modules** 프로젝트의 학습 기록을 블로그형 에세이로 정리한 공간이다.
Battery, Haptics, Sensor 세 가지 네이티브 모듈의 TypeScript spec을 정의하고,
codegen summary와 consumer app으로 JS/Native 경계를 설명하는 과정을 담고 있다.

---

## 읽는 순서

| 순서 | 파일 | 핵심 내용 |
|------|------|-----------|
| 1 | `00-problem-framing.md` | 왜 네이티브 모듈 spec을 TypeScript로 정의해야 하는지 |
| 2 | `01-approach-log.md` | spec 정의 → codegen summary → consumer UI 구현 과정 |
| 3 | `02-debug-log.md` | as const 타입, codegen 동기화 등 디버깅 기록 |
| 4 | `03-retrospective.md` | spec-first 설계에서 얻은 교훈과 회고 |
| 5 | `04-knowledge-index.md` | 소스 파일 맵, 모듈 spec, 의존성 빠른 참조 |
| 6 | `05-development-timeline.md` | CLI 명령, codegen 스크립트, 환경 설정 기록 |

## 목적별 바로가기

- **"이 프로젝트가 뭘 하는 건지 빠르게 파악하고 싶다"** → `00-problem-framing.md`
- **"구현 흐름을 따라가며 배우고 싶다"** → `01-approach-log.md`
- **"특정 에러나 이슈 해결법을 찾고 싶다"** → `02-debug-log.md`
- **"설계 판단의 이유가 궁금하다"** → `03-retrospective.md`
- **"소스 파일 위치나 의존성을 빠르게 찾고 싶다"** → `04-knowledge-index.md`
- **"환경 세팅이나 CLI 명령 순서를 알고 싶다"** → `05-development-timeline.md`

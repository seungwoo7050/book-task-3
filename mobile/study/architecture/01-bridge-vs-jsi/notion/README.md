# Bridge vs JSI Benchmark — Notion 문서 안내

이 디렉터리는 **Bridge vs JSI Benchmark** 프로젝트의 학습 기록을 블로그형 에세이로 정리한 공간이다.
React Native 0.84 기준에서 async serialized surface(Bridge 스타일)와 sync direct-call surface(JSI 스타일)의
성능 차이를 정량적으로 비교 분석한 과정을 담고 있다.

---

## 읽는 순서

| 순서 | 파일 | 핵심 내용 |
|------|------|-----------|
| 1 | `00-problem-framing.md` | 왜 Bridge와 JSI를 비교하는지, RN 0.84에서의 의미 |
| 2 | `01-approach-log.md` | 벤치마크 데이터 모델 → 통계 계산 → UI → export 구현 과정 |
| 3 | `02-debug-log.md` | 통계 계산, export 결과 동기화 등 디버깅 기록 |
| 4 | `03-retrospective.md` | 벤치마크 설계에서 얻은 교훈과 회고 |
| 5 | `04-knowledge-index.md` | 소스 파일 맵, 의존성, 벤치마크 수치 빠른 참조 |
| 6 | `05-development-timeline.md` | CLI 명령, export 스크립트, 환경 설정 기록 |

## 목적별 바로가기

- **"이 프로젝트가 뭘 하는 건지 빠르게 파악하고 싶다"** → `00-problem-framing.md`
- **"구현 흐름을 따라가며 배우고 싶다"** → `01-approach-log.md`
- **"특정 에러나 이슈 해결법을 찾고 싶다"** → `02-debug-log.md`
- **"설계 판단의 이유가 궁금하다"** → `03-retrospective.md`
- **"소스 파일 위치나 의존성을 빠르게 찾고 싶다"** → `04-knowledge-index.md`
- **"환경 세팅이나 CLI 명령 순서를 알고 싶다"** → `05-development-timeline.md`

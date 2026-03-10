# Virtualized List Performance — Notion 문서 안내

이 디렉터리는 **Virtualized List Performance** 프로젝트의 학습 기록을 블로그형 에세이로 정리한 공간이다.
10,000개 아이템 데이터셋을 FlatList와 FlashList v2로 각각 렌더링하면서
pagination, mount count, benchmark 지표를 비교 분석한 과정을 담고 있다.

---

## 읽는 순서

| 순서 | 파일 | 핵심 내용 |
|------|------|-----------|
| 1 | `00-problem-framing.md` | 왜 리스트 가상화 성능 비교가 필요한지, 문제 정의 |
| 2 | `01-approach-log.md` | 데이터 생성 → pagination → FlatList → FlashList → benchmark 구현 과정 |
| 3 | `02-debug-log.md` | estimatedItemSize, recycling, blank area 관련 디버깅 기록 |
| 4 | `03-retrospective.md` | FlatList vs FlashList 비교에서 얻은 교훈과 회고 |
| 5 | `04-knowledge-index.md` | 소스 파일 맵, 의존성, 벤치마크 지표 빠른 참조 |
| 6 | `05-development-timeline.md` | CLI 명령, 벤치마크 스크립트, 패키지 설치 등 코드 밖 작업 기록 |

## 목적별 바로가기

- **"이 프로젝트가 뭘 하는 건지 빠르게 파악하고 싶다"** → `00-problem-framing.md`
- **"구현 흐름을 따라가며 배우고 싶다"** → `01-approach-log.md`
- **"특정 에러나 이슈 해결법을 찾고 싶다"** → `02-debug-log.md`
- **"설계 판단의 이유가 궁금하다"** → `03-retrospective.md`
- **"소스 파일 위치나 의존성을 빠르게 찾고 싶다"** → `04-knowledge-index.md`
- **"환경 세팅이나 CLI 명령 순서를 알고 싶다"** → `05-development-timeline.md`

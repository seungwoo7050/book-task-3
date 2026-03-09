# 02 SSTable Format — Notion 문서 가이드

## 이 폴더는 무엇인가

이 `notion/` 폴더는 SSTable 바이너리 포맷 구현 프로젝트를 블로그형 에세이 스타일로 정리한 문서 세트다.
코드를 열기 전에 여기서부터 읽으면, 왜 이런 파일 포맷을 설계했는지, 어떤 과정을 거쳐 구현했는지 자연스럽게 파악할 수 있다.

## 문서 목록과 읽는 순서

| 순서 | 문서 | 목적 |
|------|------|------|
| 1 | [essay.md](essay.md) | SSTable 포맷의 설계 동기와 구현 과정을 서사적으로 풀어낸 에세이. **처음 읽을 문서.** |
| 2 | [timeline.md](timeline.md) | 개발 전 과정을 시간순으로 정리한 타임라인. CLI 명령, 의존성, 파일 작성 순서가 담겨 있다. |

## 목적별 바로가기

- **"이 프로젝트가 뭔지 빠르게 알고 싶다"** → [essay.md](essay.md)의 첫 두 섹션
- **"직접 재현하고 싶다"** → [timeline.md](timeline.md)를 처음부터 따라간다
- **"바이너리 레이아웃이 궁금하다"** → [essay.md](essay.md) "파일 하나의 해부학" 섹션 + `docs/concepts/sstable-layout.md`
- **"shared 패키지 의존성이 궁금하다"** → [timeline.md](timeline.md) Phase 0

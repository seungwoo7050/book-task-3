# 07 Buffer Pool — Notion 문서 가이드

## 이 폴더는 무엇인가

이 `notion/` 폴더는 Buffer Pool Manager 프로젝트를 블로그형 에세이와 타임라인으로 정리한 문서 세트다.

## 문서 목록과 읽는 순서

| 순서 | 문서 | 목적 |
|------|------|------|
| 1 | [essay.md](essay.md) | LRU 캐시, pin/unpin, dirty write-back의 동기와 구현. |
| 2 | [timeline.md](timeline.md) | 개발 타임라인. LRU → BufferPool → 테스트 순서. |

## 목적별 바로가기

- **"Buffer Pool이 왜 필요한지"** → [essay.md](essay.md) 첫 섹션
- **"LRU 캐시 구현"** → [essay.md](essay.md) "LRU 캐시" 섹션
- **"pin/unpin과 dirty 추적"** → [essay.md](essay.md) "페이지 관리" 섹션
- **"처음부터 재현"** → [timeline.md](timeline.md)

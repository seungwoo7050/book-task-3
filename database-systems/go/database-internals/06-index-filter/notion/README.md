# 06 Index Filter — Notion 문서 가이드

## 이 폴더는 무엇인가

이 `notion/` 폴더는 Bloom Filter + Sparse Index를 붙인 SSTable 조회 최적화 프로젝트를 블로그형 에세이와 타임라인으로 정리한 문서 세트다.

## 문서 목록과 읽는 순서

| 순서 | 문서 | 목적 |
|------|------|------|
| 1 | [essay.md](essay.md) | Bloom filter, sparse index, 확장된 SSTable 포맷의 동기와 동작 원리. |
| 2 | [timeline.md](timeline.md) | 개발 타임라인. bloom → sparse index → SSTable 통합 순서. |

## 목적별 바로가기

- **"왜 filter가 필요한지"** → [essay.md](essay.md) 첫 섹션
- **"Bloom filter 구현 상세"** → [essay.md](essay.md) "Bloom filter" 섹션
- **"sparse index와 block scan"** → [essay.md](essay.md) "Sparse index" 섹션
- **"처음부터 재현"** → [timeline.md](timeline.md)

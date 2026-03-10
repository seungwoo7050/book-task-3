# 05 Leveled Compaction — Notion 문서 가이드

## 이 폴더는 무엇인가

이 `notion/` 폴더는 Leveled Compaction 프로젝트를 블로그형 에세이와 재현 타임라인으로 정리한 문서 세트다.

## 문서 목록과 읽는 순서

| 순서 | 문서 | 목적 |
|------|------|------|
| 1 | [essay.md](essay.md) | SSTable이 쌓이는 문제, k-way merge, tombstone 제거 정책, manifest를 서사적으로 설명. |
| 2 | [timeline.md](timeline.md) | 개발 타임라인. merge 구현 → Manager → manifest → 테스트 순서. |

## 목적별 바로가기

- **"compaction이 왜 필요한지"** → [essay.md](essay.md) 첫 섹션  
- **"merge 알고리즘 상세"** → [essay.md](essay.md) "k-way merge" 섹션
- **"tombstone은 언제 지워도 되는지"** → [essay.md](essay.md) "tombstone 제거" 섹션
- **"manifest 원자성"** → [essay.md](essay.md) "메타데이터" 섹션 + `docs/concepts/manifest-atomicity.md`
- **"처음부터 재현"** → [timeline.md](timeline.md)

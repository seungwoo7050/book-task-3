# 04 WAL Recovery — Notion 문서 가이드

## 이 폴더는 무엇인가

이 `notion/` 폴더는 WAL(Write-Ahead Log) 구현과 crash recovery 프로젝트를 블로그형 에세이 + 재현 타임라인으로 정리한 문서 세트다.

## 문서 목록과 읽는 순서

| 순서 | 문서 | 목적 |
|------|------|------|
| 1 | [essay.md](essay.md) | WAL의 필요성, 레코드 포맷, recovery 정책, flush 후 rotation을 서사적으로 설명. |
| 2 | [timeline.md](timeline.md) | 개발 타임라인. WAL 구현 → DurableStore 통합 → 테스트 순서. |

## 목적별 바로가기

- **"왜 WAL이 필요한지"** → [essay.md](essay.md) 첫 섹션
- **"레코드 포맷 상세"** → [essay.md](essay.md) "레코드 포맷" 섹션 + `docs/concepts/wal-record-format.md`
- **"recovery가 어떤 정책을 쓰는지"** → [essay.md](essay.md) "복구" 섹션
- **"처음부터 재현하고 싶다"** → [timeline.md](timeline.md)

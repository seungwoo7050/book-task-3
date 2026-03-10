# 02-wal-recovery — notion 폴더 가이드

이 폴더는 Python 트랙 WAL Recovery 프로젝트의 학습 과정과 설계 사고를 기록한 문서 모음입니다.

## 문서 구성

| 문서 | 내용 | 언제 읽으면 좋은가 |
|------|------|-------------------|
| [essay.md](essay.md) | 바이너리 WAL과 CRC32 기반 복구를 Python으로 구현한 과정의 에세이 | append-before-apply와 stop-on-corruption의 의미를 이해하고 싶을 때 |
| [timeline.md](timeline.md) | 프로젝트 개발의 전체 과정을 시간순으로 재현한 타임라인 | 동일한 프로젝트를 처음부터 따라 구현하고 싶을 때 |

## 프로젝트 한 줄 요약

CRC32 검증 바이너리 WAL로 append-before-apply 원칙을 구현하고, stop-on-corruption 복구, DurableStore 통합, flush 후 WAL rotation을 구현한다.

## 키워드

`WAL` · `CRC32` · `append-before-apply` · `stop-on-corruption` · `binary-record` · `recovery` · `rotation` · `DurableStore` · `Python` · `struct`

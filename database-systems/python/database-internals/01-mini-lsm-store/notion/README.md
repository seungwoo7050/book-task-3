# 01-mini-lsm-store — notion 폴더 가이드

이 폴더는 Python 트랙 Mini LSM Store 프로젝트의 학습 과정과 설계 사고를 기록한 문서 모음입니다.

## 문서 구성

| 문서 | 내용 | 언제 읽으면 좋은가 |
|------|------|-------------------|
| [essay.md](essay.md) | MemTable, SSTable, LSM 읽기 경로를 하나로 합친 Python 구현의 에세이 | Go 트랙 01~03의 핵심을 Python 한 파일로 压축한 과정을 이해하고 싶을 때 |
| [timeline.md](timeline.md) | 프로젝트 개발의 전체 과정을 시간순으로 재현한 타임라인 | 동일한 프로젝트를 처음부터 따라 구현하고 싶을 때 |

## 프로젝트 한 줄 요약

Python dict 기반 active memtable, JSON Lines SSTable, newest-first 읽기 경로, tombstone, threshold 기반 자동 flush, close/reopen 영속성을 하나의 `MiniLSMStore`에 구현한다.

## 키워드

`LSM-tree` · `memtable` · `SSTable` · `flush` · `tombstone` · `read-path` · `persistence` · `Python` · `JSON-Lines`

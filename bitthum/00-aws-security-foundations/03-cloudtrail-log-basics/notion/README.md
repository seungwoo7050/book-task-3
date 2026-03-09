# 03 CloudTrail Log Basics — Notion 문서 안내

## 이 폴더의 목적

이 `notion/` 폴더는 프로젝트 03-cloudtrail-log-basics의 전체 개발 과정과 학습 내용을
Notion으로 옮길 수 있는 형태로 정리한 문서 세트입니다.

## 문서 목록과 읽기 순서

| 순서 | 문서 | 목적 | 추천 독자 |
|------|------|------|-----------|
| 1 | [essay.md](essay.md) | 로그를 "정규화된 이벤트"로 바꾸는 사고의 전환을 서사적으로 풀어낸 에세이 | 이 프로젝트를 처음 접하는 사람, Security Lake 과제 진입 전 예습 |
| 2 | [dev-timeline.md](dev-timeline.md) | DuckDB 설치부터 Parquet 적재까지 전체 개발 과정을 순차적으로 기록한 타임라인 | 프로젝트를 재현하려는 사람, DuckDB가 처음인 사람 |

## 언제 어떤 문서를 읽을까

- **"CloudTrail 로그 정규화가 왜 필요한지 알고 싶다"** → `essay.md`
- **"DuckDB와 Parquet를 직접 써 보고 싶다"** → `dev-timeline.md`
- **"과제 07 (Security Lake Mini)을 시작하기 전에 기반을 잡고 싶다"** → `essay.md` + `dev-timeline.md` 순서대로
- **"ETL 파이프라인의 구조를 빠르게 파악하고 싶다"** → `essay.md`의 설계 섹션

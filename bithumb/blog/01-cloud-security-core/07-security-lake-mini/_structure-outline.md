# 07 Security Lake Mini 구조 메모

이 문서는 최종 글을 쓰기 전에 서사 배치를 점검하는 메모다. 독자에게 무엇을 먼저 설명하고 어디서 코드와 CLI를 꺼내 올지 한눈에 보이도록 정리한다.

## 이번 문서가 맡는 일
- foundation의 log normalization을 local lake 적재와 preset detection query로 확장하는 흐름을 보여 준다.
- 글은 `lake 적재 -> SQL alert taxonomy -> CLI/test 재현성` 순서로 배치한다.

## 먼저 붙들 소스 묶음
- [`../../../01-cloud-security-core/07-security-lake-mini/README.md`](../../../01-cloud-security-core/07-security-lake-mini/README.md)
- [`../../../01-cloud-security-core/07-security-lake-mini/problem/README.md`](../../../01-cloud-security-core/07-security-lake-mini/problem/README.md)
- [`../../../01-cloud-security-core/07-security-lake-mini/docs/concepts/lake-thinking.md`](../../../01-cloud-security-core/07-security-lake-mini/docs/concepts/lake-thinking.md)
- [`../../../01-cloud-security-core/07-security-lake-mini/python/README.md`](../../../01-cloud-security-core/07-security-lake-mini/python/README.md)
- [`../../../01-cloud-security-core/07-security-lake-mini/python/src/security_lake_mini/lake.py`](../../../01-cloud-security-core/07-security-lake-mini/python/src/security_lake_mini/lake.py)
- [`../../../01-cloud-security-core/07-security-lake-mini/python/src/security_lake_mini/cli.py`](../../../01-cloud-security-core/07-security-lake-mini/python/src/security_lake_mini/cli.py)
- [`../../../01-cloud-security-core/07-security-lake-mini/python/tests/test_lake.py`](../../../01-cloud-security-core/07-security-lake-mini/python/tests/test_lake.py)
- [`../../../01-cloud-security-core/07-security-lake-mini/python/tests/test_cli.py`](../../../01-cloud-security-core/07-security-lake-mini/python/tests/test_cli.py)

## 본문을 배치하는 순서

- `00-series-map.md`
  - ingestion과 detection query를 같은 프로젝트 안에서 읽는 이유를 먼저 설명한다.
- `10-development-timeline.md`
  - 도입: raw log를 적재만 해서는 lake가 아니고, detection query가 반복 실행돼야 한다는 문제의식을 세운다.
  - Phase 1. CloudTrail fixture를 local lake로 적재했다.
  - Phase 2. SQL query를 alert taxonomy로 썼다.
  - Phase 3. CLI와 테스트로 alert 순서를 잠갔다.
  - 마무리: control plane이 이 lake alert를 어떻게 ingest하는지 질문을 넘긴다.

## 강조할 코드와 CLI
- 코드 앵커: lake bootstrap, preset SQL registry, `LAKE-*` findings mapping, CLI output order assertions
- CLI 앵커: `python -m security_lake_mini.cli ingest ...`, `python -m security_lake_mini.cli detect ...`, `pytest 01-cloud-security-core/07-security-lake-mini/python/tests`
- 개념 훅: lake에서 중요한 것은 저장 위치보다 “같은 SQL을 반복 실행해 같은 alert taxonomy를 얻는 능력”이라는 점

## 리라이트 기준
- chronology는 실제 commit timestamp보다 source, test, CLI가 묶이는 순서를 기준으로 읽는다.
- 이 문서는 메타 기록보다 서사 배치와 강조점에 집중한다.

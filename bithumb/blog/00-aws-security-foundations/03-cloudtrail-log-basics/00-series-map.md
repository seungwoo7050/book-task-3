# 03 CloudTrail Log Basics 읽기 지도

원본 로그를 그대로 쌓는 대신, query와 detection이 가능한 공통 이벤트 구조로 바꾸는 가장 작은 ETL 단계다.

이 문서는 본문으로 바로 들어가기 전에 무엇을 붙들고 읽어야 하는지 정리해 두는 입구다. 먼저 질문과 흐름을 잡고 내려가면 phase 사이 점프가 훨씬 덜 갑작스럽다.

## 먼저 붙들 질문
- 서로 다른 로그 포맷을 어떤 공통 필드로 눌러야 이후 query가 단순해지는가?
- 왜 메모리 배열이 아니라 DuckDB + Parquet를 함께 남겼는가?
- ETL 성공을 파일 생성이 아니라 질의 결과로 검증하려면 무엇을 잠가야 하는가?

## 이 글은 이렇게 흘러간다
1. 시작점: 문제 정의와 이 프로젝트가 고정하려는 입력/출력 경계
2. Phase 1. 두 로그를 같은 EventRecord로 눌렀다: CloudTrail과 VPC Flow Logs를 하나의 분석 코드가 읽을 수 있는 공통 구조로 만든다.
3. Phase 2. DuckDB와 Parquet를 동시에 남겼다: 정규화 결과를 로컬에서 즉시 질의 가능하고, 다음 프로젝트에도 넘길 수 있는 저장 구조로 만든다.
4. Phase 3. 집계 쿼리와 time range를 테스트로 잠갔다: 적재 결과가 정말 queryable한지 확인한다.
5. 마무리: 다음 프로젝트로 이어지는 질문과 남은 한계

## 특히 눈여겨볼 장면
- 로그를 raw payload가 아니라 공통 레코드로 바꾸는 장면을 첫 분기점으로 둔다.
- DuckDB + Parquet를 남기는 이유가 저장이 아니라 다음 query 단계 연결이라는 점을 보여 준다.
- 집계와 time range 테스트로 ETL의 효용을 증명하는 흐름으로 닫는다.

## 먼저 열 문서
- [10-development-timeline.md](10-development-timeline.md): raw log를 queryable event로 바꾸는 ETL

## 근거로 삼은 파일
- `README.md`
- `problem/README.md`
- `python/README.md`
- `docs/concepts/log-normalization.md`
- `python/src/cloudtrail_log_basics/etl.py`
- `python/tests/test_etl.py`

# 문제 프레이밍

## 이 프로젝트가 답하려는 질문

CloudTrail JSON을 눈으로 읽는 것만으로는 운영 질문에 답하기 어렵습니다. 이 프로젝트는 두 종류의 로그를 공통
이벤트 스키마로 정규화한 뒤, DuckDB와 Parquet에 적재해 질의 가능한 상태로 만드는 것이 목표입니다.

## 실제 입력과 출력

입력:
- `problem/data/cloudtrail_events.json`
- `problem/data/vpc_flow_logs.json`

출력:
- 정규화된 `EventRecord` 목록
- DuckDB 테이블
- Parquet 파일
- 이벤트 이름/actor/시간 범위 기준 요약 결과

## 강한 제약

- 원본 스키마의 모든 필드를 보존하지 않습니다.
- VPC Flow Logs는 실제 텍스트 포맷이 아니라 JSON fixture로 단순화합니다.
- 이상 탐지 알고리즘은 넣지 않고, 정규화와 요약 질의까지만 다룹니다.

## 완료로 보는 기준

- 두 종류의 로그를 하나의 스키마로 설명할 수 있어야 합니다.
- Parquet 파일이 생성되고, DuckDB에서 요약 쿼리가 동작해야 합니다.
- 테스트에서 event count, actor summary, 시간 범위 집계를 재현해야 합니다.

## 확인에 쓰는 근거

- 문제 설명: [../problem/README.md](../problem/README.md)
- 핵심 테스트: [../python/tests/test_etl.py](../python/tests/test_etl.py)
- 이전 배경 설명: [../notion-archive/essay.md](../notion-archive/essay.md)

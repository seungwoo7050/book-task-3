# 지식 인덱스

## 이번 프로젝트에서 굳혀야 할 개념

- 정규화는 원본 로그를 지우는 과정이 아니라, 분석 질문에 맞는 공통 좌표계로 옮기는 과정입니다.
- DuckDB는 로컬 학습 환경에서 보안 로그 ETL과 집계 쿼리를 재현하기에 충분히 강력합니다.
- Parquet는 이후 lake 구조, 재처리, 샘플 공유에 유리한 중간 산출물입니다.
- 집계와 시간 범위 필터를 함께 확인해야 ETL이 실제 탐지 흐름의 기반이 됩니다.

## 로컬 근거 파일

- 개념 요약: [../docs/concepts/log-normalization.md](../docs/concepts/log-normalization.md)
- 문제 범위: [../problem/README.md](../problem/README.md)
- ETL 구현: [../python/src/cloudtrail_log_basics/etl.py](../python/src/cloudtrail_log_basics/etl.py)
- 검증 코드: [../python/tests/test_etl.py](../python/tests/test_etl.py)
- 입력 fixture: [../problem/data/](../problem/data/)

## 재현 체크포인트

- Parquet 파일이 실제로 생성되는지와 별개로, `summarize_by_event_name`가 네 개 이벤트를 올바르게 집계하는지 확인합니다.
- `within_time_range`가 2를 반환해야 특정 시간대 필터가 정상이라는 뜻입니다.
- `CreateAccessKey`와 `PutBucketAcl`이 같은 테이블에서 다뤄지는 이유를 설명할 수 있어야 합니다.

## 다음 프로젝트로 이어지는 질문

- `07-security-lake-mini`는 이 정규화 사고방식 위에 detection query를 얹습니다.
- `10-cloud-security-control-plane`에서는 같은 로그 적재 흐름이 ingestion API로 들어갑니다.

## 참고 자료

- 공식 링크 정리: [../docs/references/README.md](../docs/references/README.md)
- 이전 서술형 기록: [../notion-archive/essay.md](../notion-archive/essay.md)
- 이전 작업 로그: [../notion-archive/dev-timeline.md](../notion-archive/dev-timeline.md)

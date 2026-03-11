# 07 Security Lake Mini

## 풀려는 문제

로그를 모으는 것만으로는 탐지 체계가 되지 않습니다.
이 프로젝트는 CloudTrail fixture를 local lake에 적재하고, preset detection query를 반복 실행해 alert를 만드는 최소 흐름을 구현합니다.

## 내가 낸 답

- CloudTrail fixture를 DuckDB table과 Parquet 파일로 적재합니다.
- 미리 정한 detection query를 실행해 `LAKE-*` alert를 생성합니다.
- 적재와 탐지를 하나의 CLI 흐름으로 묶어 로컬에서도 반복 검증되게 합니다.
- 03번의 정규화 감각을 이어받아 detection engineering 입문 문제로 확장합니다.

## 입력과 출력

- 입력: `problem/data/cloudtrail_suspicious.json`, lake DB 경로, Parquet 경로
- 출력: local lake 산출물과 detection alert 목록

## 검증 방법

```bash
make venv
mkdir -p .artifacts/security-lake-mini
PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m security_lake_mini.cli 01-cloud-security-core/07-security-lake-mini/problem/data/cloudtrail_suspicious.json .artifacts/security-lake-mini/lake.duckdb .artifacts/security-lake-mini/events.parquet
PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m pytest 01-cloud-security-core/07-security-lake-mini/python/tests
```

## 현재 상태

- `verified`
- local lake 적재와 detection query 실행을 fixture 기반으로 재현할 수 있습니다.
- 10번 캡스톤의 CloudTrail ingestion 흐름과 alert성 finding 설계에 연결됩니다.

## 한계와 다음 단계

- VPC Flow Logs join과 다중 테이블 detection은 캡스톤에서 확장합니다.
- 분산 저장소나 대용량 처리 최적화는 다루지 않고, local lake 개념 재현에 집중합니다.

## 더 깊게 읽을 문서

- [problem/README.md](problem/README.md)
- [python/README.md](python/README.md)
- [docs/README.md](docs/README.md)
- [notion/README.md](notion/README.md)

# 07 Security Lake Mini

## 프로젝트 한줄 소개

보안 로그를 적재하고 detection query를 돌리는 작은 local security lake입니다.

## 왜 배우는가

로그를 모으는 것만으로는 탐지 체계가 되지 않습니다. 이 프로젝트는 CloudTrail fixture를 로컬 lake에 적재하고 preset query를 반복 실행하는 흐름을 통해 detection engineering 입문 감각을 만듭니다.

## 현재 구현 범위

- CloudTrail fixture를 DuckDB와 Parquet에 적재합니다.
- preset detection query를 실행해 alert를 생성합니다.
- 로컬에서 security lake 개념을 축소 재현합니다.

## 빠른 시작

아래 명령은 레포 루트 기준입니다.

```bash
make venv
mkdir -p .artifacts/security-lake-mini
PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m security_lake_mini.cli 01-cloud-security-core/07-security-lake-mini/problem/data/cloudtrail_suspicious.json .artifacts/security-lake-mini/lake.duckdb .artifacts/security-lake-mini/events.parquet
```

## 검증 명령

```bash
PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m pytest 01-cloud-security-core/07-security-lake-mini/python/tests
```

## 먼저 읽을 파일

- [problem/README.md](problem/README.md)
- [docs/README.md](docs/README.md)
- [python/README.md](python/README.md)
- [notion/README.md](notion/README.md)

## 포트폴리오 확장 힌트

“lake를 만들었다”는 말보다, 어떤 탐지 질문을 어떤 query preset으로 증명했는지 보여 주는 편이 훨씬 강합니다.

## 알려진 한계

- VPC Flow Logs와 multi-table join은 캡스톤에서 확장합니다.
- 분산 저장소나 대용량 처리 최적화는 다루지 않습니다.

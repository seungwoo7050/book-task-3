# 03 CloudTrail Log Basics

## 프로젝트 한줄 소개

원본 보안 로그를 질의 가능한 이벤트 구조로 바꾸는 입문 프로젝트입니다.

## 왜 배우는가

로그 파일을 저장하는 것과 탐지 가능한 형태로 적재하는 것은 다릅니다. 이 프로젝트는 CloudTrail과 VPC Flow Logs를 정규화해, 이후 security lake와 detection query의 기반을 만듭니다.

## 현재 구현 범위

- CloudTrail과 VPC Flow Logs fixture를 읽습니다.
- 공통 필드 중심의 이벤트 구조로 정규화합니다.
- DuckDB와 Parquet로 로컬 적재 흐름을 재현합니다.

## 빠른 시작

아래 명령은 레포 루트 기준입니다.

```bash
make venv
PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src .venv/bin/python -m cloudtrail_log_basics.etl 00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/cloudtrail_events.json 00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/vpc_flow_logs.json
```

## 검증 명령

```bash
PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src .venv/bin/python -m pytest 00-aws-security-foundations/03-cloudtrail-log-basics/python/tests
```

## 먼저 읽을 파일

- [problem/README.md](problem/README.md)
- [docs/README.md](docs/README.md)
- [python/README.md](python/README.md)
- [notion/README.md](notion/README.md)

## 포트폴리오 확장 힌트

로그를 많이 모았다는 설명보다, 어떤 공통 필드로 정규화했고 왜 그 구조가 이후 탐지에 유리한지 보여 주는 편이 더 좋습니다.

## 알려진 한계

- 실제 CloudTrail 스키마의 모든 필드를 보존하지는 않습니다.
- 운영 규모의 대용량 파이프라인 대신 로컬 fixture 중심으로 제한합니다.

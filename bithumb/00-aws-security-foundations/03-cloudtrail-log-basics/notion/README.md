# 03 CloudTrail Log Basics notion 기록

## 이 문서 묶음이 하는 일

이 `notion/`은 로그를 수집하는 단계와 질의 가능한 구조로 정규화하는 단계를 분리해서 이해하도록 돕는 기록입니다.
현재 버전은 ETL 코드, DuckDB/Parquet 산출물, 테스트가 실제로 검증하는 질의 결과를 기준으로 다시 쓰였습니다.

## 이 문서를 읽을 때 잡아야 할 질문

- 왜 CloudTrail과 VPC Flow Logs를 같은 테이블에 넣으려 했는가?
- 공통 `EventRecord` 스키마를 두면 어떤 질문이 쉬워지는가?
- Parquet까지 남기는 이유가 단순 저장이 아니라 다음 프로젝트 연결이라는 점을 어떻게 보여 줄 수 있는가?

## 추천 읽기 순서

학습자가 가장 빨리 손에 잡히는 재현 경로를 보려면 `05-reproduction-guide.md`를 초반에 읽는 편이 좋습니다.

1. [00-problem-framing.md](00-problem-framing.md): 문제와 경계를 먼저 확인합니다.
2. [05-reproduction-guide.md](05-reproduction-guide.md): 가장 짧은 재현 경로와 기대 결과를 확인합니다.
3. [01-approach-log.md](01-approach-log.md): 현재 구현 방향을 왜 택했는지 읽습니다.
4. [02-debug-log.md](02-debug-log.md): 어디서 자주 막히는지와 어떤 테스트가 근거인지 확인합니다.
5. [03-retrospective.md](03-retrospective.md): 지금 구현이 무엇을 증명했고 무엇을 의도적으로 비워 두었는지 읽습니다.
6. [04-knowledge-index.md](04-knowledge-index.md): 다음 프로젝트로 이어지는 개념과 근거 파일을 모아 봅니다.

## 이 버전의 근거

- 현재 문제 설명: [../problem/README.md](../problem/README.md)
- 현재 구현 안내: [../python/README.md](../python/README.md)
- ETL 구현: [../python/src/cloudtrail_log_basics/etl.py](../python/src/cloudtrail_log_basics/etl.py)
- 검증 코드: [../python/tests/test_etl.py](../python/tests/test_etl.py)
- 이전 장문 기록: [../notion-archive/essay.md](../notion-archive/essay.md)
- 이전 작업 로그: [../notion-archive/dev-timeline.md](../notion-archive/dev-timeline.md)

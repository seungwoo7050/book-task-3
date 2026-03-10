# 문제 프레이밍

## 이 프로젝트가 답하려는 질문

로그를 적재한 뒤 실제로 의심스러운 행위를 자동으로 찾을 수 있는가? 이 프로젝트는 CloudTrail fixture 하나를 lake에 넣고,
여기서 `CreateAccessKey`, `PutBucketAcl`, `AuthorizeSecurityGroupIngress`, `DeleteTrail`, `Root ConsoleLogin` 다섯 가지 패턴을 alert로 뽑아내는 것이 목표입니다.

## 실제 입력과 출력

입력:
- `problem/data/cloudtrail_suspicious.json`
- 출력용 DuckDB 경로
- 출력용 Parquet 경로

출력:
- 적재된 lake 파일
- detection query 결과 alert 목록
- `LAKE-001` ~ `LAKE-005` control_id

## 강한 제약

- VPC Flow Logs와 multi-table join은 이 단계에서 제외합니다.
- detection query는 코드에 하드코딩되어 있습니다.
- 이상 탐지 모델 대신 규칙 기반 query만 다룹니다.

## 완료로 보는 기준

- suspicious fixture를 넣었을 때 alert control_id 순서가 고정돼야 합니다.
- Parquet 파일이 실제로 생성돼야 합니다.
- root 로그인처럼 조건이 섬세한 규칙도 설명할 수 있어야 합니다.

## 확인에 쓰는 근거

- 문제 설명: [../problem/README.md](../problem/README.md)
- 핵심 테스트: [../python/tests/test_lake.py](../python/tests/test_lake.py)
- 이전 배경 설명: [../notion-archive/essay.md](../notion-archive/essay.md)

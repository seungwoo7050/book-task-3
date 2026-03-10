# 지식 인덱스

## 이번 프로젝트에서 굳혀야 할 개념

- security lake의 핵심은 저장 그 자체가 아니라 detection 가능한 구조입니다.
- alert는 행위 기반 결과이며, 정적 설정에서 나오는 finding과 다른 속성을 가집니다.
- Parquet 출력은 재처리와 샘플 공유에 유리합니다.
- CloudTrail suspicious event는 detection rule 입문용으로 좋은 fixture입니다.

## 로컬 근거 파일

- 개념 요약: [../docs/concepts/lake-thinking.md](../docs/concepts/lake-thinking.md)
- 구현 진입점: [../python/src/security_lake_mini/lake.py](../python/src/security_lake_mini/lake.py)
- CLI 진입점: [../python/src/security_lake_mini/cli.py](../python/src/security_lake_mini/cli.py)
- 검증 코드: [../python/tests/test_lake.py](../python/tests/test_lake.py)
- 입력 fixture: [../problem/data/cloudtrail_suspicious.json](../problem/data/cloudtrail_suspicious.json)

## 재현 체크포인트

- alert 목록의 control_id 순서가 `LAKE-001`부터 `LAKE-005`까지 일관되게 나오는지 확인합니다.
- Parquet 파일이 생성돼야 이후 재처리나 공유가 가능합니다.
- 정규화 기반 적재 없이 detection query만 별도로 돌리면 왜 같은 결과가 안 나오는지 설명할 수 있어야 합니다.

## 다음 프로젝트로 이어지는 질문

- `10-cloud-security-control-plane`은 같은 CloudTrail ingestion과 detection 흐름을 API 뒤에 둡니다.
- `03-cloudtrail-log-basics`는 이 프로젝트가 기대는 정규화 기반입니다.

## 참고 자료

- 공식 링크 정리: [../docs/references/README.md](../docs/references/README.md)
- 이전 서술형 기록: [../notion-archive/essay.md](../notion-archive/essay.md)
- 이전 작업 로그: [../notion-archive/dev-timeline.md](../notion-archive/dev-timeline.md)

# 디버그 로그

## 실제로 자주 막히는 지점

- `Root ConsoleLogin`은 event 이름만으로는 부족하고 actor 패턴까지 봐야 합니다.
- 다섯 가지 detection을 따로 구현하면 관리가 쉬워 보이지만, 현재 범위에서는 하나의 분류 쿼리가 더 단순합니다.
- 적재만 성공하고 탐지가 비어 있는 상황을 막으려면 alert control_id 결과를 고정된 리스트로 검증해야 합니다.

## 이미 확인된 테스트 시나리오

- `test_security_lake_generates_expected_alerts`: suspicious fixture를 적재한 뒤 `LAKE-001`부터 `LAKE-005`까지 순서대로 나오는지 확인합니다.
- 같은 테스트에서 Parquet 파일 생성 여부까지 함께 확인합니다.

## 다시 검증할 명령

```bash
PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m pytest 01-cloud-security-core/07-security-lake-mini/python/tests
```

## 실패하면 먼저 볼 곳

- 테스트 코드: [../python/tests/test_lake.py](../python/tests/test_lake.py)
- 구현 진입점: [../python/src/security_lake_mini/lake.py](../python/src/security_lake_mini/lake.py)
- 이전 설명: [../notion-archive/essay.md](../notion-archive/essay.md)

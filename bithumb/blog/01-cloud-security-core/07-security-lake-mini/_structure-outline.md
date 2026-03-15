# 07 Security Lake Mini 구조 메모

## 이번 문서의 중심
- 이 lab을 "로컬 저장소 만들기"가 아니라 "반복 가능한 detection lake 만들기"로 설명한다.
- 서사는 `정규화/적재 -> SQL taxonomy -> CLI와 테스트 재현성` 순서로 고정한다.
- 이전 lab의 append 성격과 달리, 이번 lab은 resettable lake라는 점을 분명히 드러낸다.

## 먼저 붙들 소스
- `../../../01-cloud-security-core/07-security-lake-mini/README.md`
- `../../../01-cloud-security-core/07-security-lake-mini/problem/README.md`
- `../../../01-cloud-security-core/07-security-lake-mini/python/README.md`
- `../../../01-cloud-security-core/07-security-lake-mini/docs/concepts/lake-thinking.md`
- `../../../01-cloud-security-core/07-security-lake-mini/problem/data/cloudtrail_suspicious.json`
- `../../../01-cloud-security-core/07-security-lake-mini/python/src/security_lake_mini/lake.py`
- `../../../01-cloud-security-core/07-security-lake-mini/python/src/security_lake_mini/cli.py`
- `../../../01-cloud-security-core/07-security-lake-mini/python/tests/test_lake.py`
- `../../../01-cloud-security-core/07-security-lake-mini/python/tests/test_cli.py`

## 본문 배치
- 도입
  - lake의 핵심을 저장이 아니라 반복 실행 가능한 detection으로 잡는다.
- Phase 1
  - `_normalize`, `ingest_cloudtrail`, `DELETE FROM lake_events`를 중심으로 resettable 적재를 설명한다.
- Phase 2
  - SQL `CASE`가 taxonomy라는 점, `source`는 저장되지만 rule에선 쓰이지 않는 점을 보여 준다.
  - `INFO` branch가 현재는 사실상 도달 불가라는 source-based inference를 남긴다.
- Phase 3
  - CLI와 pytest가 같은 alert 순서를 잠그는 구조를 설명한다.
- 마무리
  - correlation, suppression, multi-table join은 아직 없다는 한계를 정리한다.

## 꼭 남길 검증 신호
- CLI JSON alert 5개 출력
- DuckDB `lake_events` row count = `5`
- control 순서 `LAKE-001` -> `LAKE-005`
- pytest `2 passed in 0.07s`

## 탈락 기준
- Parquet 생성 사실만 강조하고 detection query 의미를 놓치면 안 된다.
- SQL taxonomy를 문서 밖의 숨은 규칙처럼 쓰면 안 된다.
- rerun determinism을 빼먹으면 이전 append형 lab과 차이가 흐려진다.

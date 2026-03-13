# D-data-api-lab 시리즈 지도

이 시리즈는 CRUD보다 오래 남는 데이터 API의 결정 지점, 즉 목록 질의, 소프트 삭제, 버전 충돌을 실제 소스와 테스트 기준으로 다시 읽습니다.

## 이 시리즈가 보는 문제

- 프로젝트, 태스크, 댓글 API가 단순 생성/조회 예제로 끝나지 않고, 정렬과 삭제 정책을 설명할 수 있어야 합니다.
- 동시에 수정 충돌을 낙관적 락으로 드러내는 최소 경로가 있어야 합니다.

## 실제 구현 표면

- `/api/v1/data/projects`, `/tasks`, `/comments`
- `status`, `sort`, `page`, `page_size`, `include_deleted` query parameter
- `version` 필드 기반 업데이트 충돌 감지
- soft delete 후 목록 필터링

## 대표 검증 엔트리

- `pytest tests/integration/test_data_api.py -q`
- `make smoke`

## 읽는 순서

1. [프로젝트 README](../../../labs/D-data-api-lab/README.md)
2. [문제 정의](../../../labs/D-data-api-lab/problem/README.md)
3. [실행 진입점](../../../labs/D-data-api-lab/fastapi/README.md)
4. [대표 통합 테스트](../../../labs/D-data-api-lab/fastapi/tests/integration/test_data_api.py)
5. [핵심 구현](../../../labs/D-data-api-lab/fastapi/app/domain/services/data_api.py)
6. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../labs/D-data-api-lab/README.md)
- [problem/README.md](../../../labs/D-data-api-lab/problem/README.md)
- [fastapi/README.md](../../../labs/D-data-api-lab/fastapi/README.md)
- [tests/integration/test_data_api.py](../../../labs/D-data-api-lab/fastapi/tests/integration/test_data_api.py)
- [app/domain/services/data_api.py](../../../labs/D-data-api-lab/fastapi/app/domain/services/data_api.py)
- [docs/verification-report.md](../../../docs/verification-report.md)

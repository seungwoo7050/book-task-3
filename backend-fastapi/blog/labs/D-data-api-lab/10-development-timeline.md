# D-data-api-lab: CRUD를 만들되, 목록 조건과 충돌 제어를 먼저 드러내기

이 글은 `labs/D-data-api-lab/README.md`, `problem/README.md`, `docs/README.md`, `labs/D-data-api-lab/fastapi/app/api/v1/routes/data_api.py::update_project`, `labs/D-data-api-lab/fastapi/tests/integration/test_data_api.py::test_optimistic_locking_and_task_comment_creation`, `backend-fastapi/docs/verification-report.md`를 바탕으로 실제 구현 순서를 다시 복원한다.

D 랩은 겉보기에는 가장 평범한 CRUD 프로젝트처럼 보인다. 그런데 problem/README.md를 보면 생성/조회/수정/삭제보다 필터링, 정렬, 페이지네이션, 소프트 삭제, 낙관적 락이 더 먼저 나온다. 즉 이 프로젝트는 엔터티 수를 늘리는 실습이 아니라, 데이터 API가 어떤 조회 의미와 충돌 규칙을 가져야 하는지 정리하는 실습이다.

## 1. 데이터 API를 단순 CRUD보다 넓은 문제로 잡기
처음부터 질문이 달랐다. README.md는 projects/tasks/comments CRUD를 말하지만, docs/README.md는 엔터티 관계를 어디까지 API에 그대로 드러낼지, 소프트 삭제가 목록 조회에서 어떤 의미를 가지는지, optimistic locking이 어떤 충돌을 막아 주는지부터 묻는다. 이 덕분에 timeline도 자연스럽게 목록 semantics 중심으로 재배열된다.

## 2. 목록 조건과 버전 필드를 route surface에 올리기
코드에서 가장 중요한 건 update_project다. 이 함수는 payload에서 version을 직접 받는다. 즉 클라이언트는 최신 버전을 알고 있어야 수정할 수 있고, stale update는 애초에 contract 위반으로 취급된다. 낙관적 락을 storage 내부 구현으로 숨기지 않고 API surface로 끌어낸 셈이다.

```python
def update_project(
    project_id: str,
    payload: ProjectUpdateRequest,
    service: Annotated[DataApiService, Depends(get_data_service)],
) -> ProjectResponse:
    project = service.update_project(
        project_id=project_id,
        title=payload.title,
        status=payload.status,
        version=payload.version,
    )
    return ProjectResponse.model_validate(project)
```

핵심은 버전 필드가 optimistic locking을 API 계약 안으로 끌어올린다는 데 있다.

## 3. 충돌과 소프트 삭제를 테스트로 굳히기
테스트는 목록과 충돌 의미를 더 구체적으로 만든다. 첫 번째 테스트는 active 프로젝트만 필터링하고, 소프트 삭제 뒤에는 목록에서 사라지며, include_deleted=true를 주면 다시 보인다는 사실을 고정한다. 두 번째 테스트는 version 1로 stale patch를 보냈을 때 409가 나는지 확인한다. 이 조합 덕분에 글도 CRUD 설명이 아니라 '조회 semantics와 충돌 제어가 어떻게 함께 움직이는가'를 중심으로 쓸 수 있다.

```python
def test_optimistic_locking_and_task_comment_creation(client) -> None:
    project = client.post(
        "/api/v1/data/projects",
        json={"title": "Roadmap", "status": "active"},
    ).json()

    update = client.patch(
        f"/api/v1/data/projects/{project['id']}",
        json={"version": project["version"], "title": "Roadmap v2"},
    )
    assert update.status_code == 200
    assert update.json()["version"] == 2
```

테스트는 버전 충돌과 하위 task/comment 생성이 한 데이터 흐름에 묶여 있음을 보여 준다.

## 4. 2026-03-09 재검증으로 Compose surface까지 닫기
재검증은 2026-03-09 기준으로 compile, lint, test, smoke, Compose probe까지 닫혀 있다. 보고서가 로컬 스키마 자동 초기화까지 분리해 적어 둔 것도 좋다. 덕분에 이 프로젝트는 단순 예제 코드가 아니라, 문서와 실행 진입점까지 같이 따라갈 수 있는 독립 워크스페이스로 남는다.

```bash
python3 -m compileall app tests
make lint
make test
make smoke
./tools/compose_probe.sh labs/D-data-api-lab/fastapi 8002
```

2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 통과했고, 로컬 학습 실행을 위해 앱 시작 시 스키마 자동 초기화를 두었다. 이 랩의 핵심 CLI는 테스트보다도 query parameter와 version 충돌을 반복 호출해 보는 데 있다.

## 정리
D 랩에서 남는 것은 CRUD endpoint 수가 아니라 데이터 contract의 무게다. 목록 조건, 삭제 정책, 버전 충돌을 surface로 끌어올렸기 때문에, 다음 E 랩에서 요청-응답 밖으로 작업을 밀어낼 때도 어떤 데이터가 어디까지 확정됐는지를 더 또렷하게 설명할 수 있다.

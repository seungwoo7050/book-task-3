# D-data-api-lab 개발 타임라인

## 2026-03-09
### Session 1

- 목표: 데이터 API를 만들라는 요구를 처음 봤을 때 "CRUD 네 줄이면 끝 아닌가?"라고 생각했다. `problem/README.md`를 먼저 읽어 실제 범위를 확인한다.
- 진행: 성공 기준에 필터링, 정렬, 페이지네이션, 소프트 삭제, 낙관적 락이 들어 있다. 이건 CRUD가 아니라 데이터 API의 "계약을 어떻게 설계하는가" 문제다.
- 판단: 인증과 인가를 일부러 빼고 데이터 경계에만 집중하는 게 이 랩의 핵심이다. 먼저 project → task → comment 계층을 만들되, 삭제와 충돌 제어를 후순위가 아니라 초기 설계에 넣기로 했다.

CLI:

```bash
$ cd labs/D-data-api-lab/fastapi
$ python3 -m venv .venv
$ source .venv/bin/activate
$ make install
```

### Session 2

- 목표: project 생성과 목록 조회를 먼저 구현한다.
- 진행: 처음엔 `list_projects`를 단순히 전체 조회로 만들었다. 그런데 테스트를 작성하면서 "active인 것만 보고 싶다", "title 순서로 보고 싶다", "페이지당 1개만 보고 싶다"를 동시에 요구하니, 쿼리 파라미터 조합이 필요했다.
- 이슈: `sort` 파라미터를 어떻게 설계할까? 처음엔 `sort_by`와 `sort_order`를 따로 받으려 했는데, `-title`처럼 prefix로 방향을 표현하는 게 query string이 간결해진다.
- 판단: 페이지네이션은 cursor vs page-based 중 고민했다. 이 랩은 대규모 데이터를 다루는 것이 아니므로 page-based로 충분하다.
- 검증: `status=active, sort=title, page=1, page_size=1`로 요청하면 Alpha만 나오고 total은 2인 것을 확인했다.

```python
filtered = client.get(
    "/api/v1/data/projects",
    params={"status": "active", "sort": "title", "page": 1, "page_size": 1},
)
assert payload["total"] == 2
assert len(payload["items"]) == 1
assert payload["items"][0]["title"] == "Alpha"
```

### Session 3

- 목표: 소프트 삭제를 구현한다. 처음엔 "그냥 DELETE에서 row를 지우면 되는 거 아닌가?"라고 생각했다.
- 이슈: hard delete를 하면 되돌릴 수 없다. 관리자가 실수로 삭제한 프로젝트를 복구할 방법이 없다. 또, 삭제된 프로젝트를 감사 목적으로 조회해야 하는 경우도 있다.
- 조치: `deleted_at` timestamp를 찍고, 기본 목록에서는 제외하되, `include_deleted=true`로 요청하면 다시 보이게 했다.

```python
project.deleted_at = datetime.now(UTC)
project.version += 1
self.session.commit()
```

여기서 중요한 건 삭제할 때도 `version`을 올린다는 점이다. 처음엔 삭제 시 version 증가를 빼먹었는데, 나중에 보니 삭제도 "상태 변경"이므로 version이 올라가야 다른 클라이언트가 stale 상태를 감지할 수 있다.

- 검증: 삭제 후 기본 목록에서 빠지고, `include_deleted=true`에서는 보이는 것을 확인했다.

CLI:

```bash
$ pytest tests/integration/test_data_api.py::test_filter_sort_pagination_and_soft_delete -q
```

```
1 passed
```

### Session 4

- 목표: 낙관적 락(optimistic locking)을 구현한다.
- 진행: 두 명이 같은 프로젝트를 동시에 수정하면 어떻게 되나? 처음엔 "마지막 쓰기가 이긴다(last write wins)"로 넘어가려 했는데, 그러면 첫 번째 사람의 수정이 조용히 사라진다.
- 이슈: 해결책은 호출자가 자기가 마지막으로 본 `version`을 함께 보내고, 서버가 현재 version과 비교하는 것. 안 맞으면 409를 돌려보낸다.

```python
if project.version != version:
    raise AppError(
        code="VERSION_CONFLICT",
        message="Project version conflict.",
        status_code=409,
    )
```

처음엔 낙관적 락의 "낙관적"이 무슨 뜻인지 확실하지 않았다. 대부분의 경우 충돌이 안 나는 것을 낙관적으로 가정하고, 충돌이 실제로 나면 그때 거부한다는 뜻이었다. 비관적 락(DB lock)과 달리 읽기에서 성능 손실이 없다.

- 검증: version 1로 update하면 성공(version이 2로 올라감), 같은 version 1로 다시 update하면 409.

```python
update = client.patch(
    f"/api/v1/data/projects/{project['id']}",
    json={"version": project["version"], "title": "Roadmap v2"},
)
assert update.status_code == 200
assert update.json()["version"] == 2

stale = client.patch(
    f"/api/v1/data/projects/{project['id']}",
    json={"version": 1, "status": "archived"},
)
assert stale.status_code == 409
```

나중에 보니 이 두 요청이 이 랩의 핵심을 가장 압축해서 보여 준다. API 호출자가 stale 상태를 가지고 있으면 서버가 명시적으로 거부한다.

### Session 5

- 목표: task, comment 하위 리소스를 추가하고 전체 검증 루프를 돈다.
- 진행: project 아래 task, task 아래 comment를 만드는 계층 구조를 구현했다. 삭제된 project에 task를 만들려고 하면 404를 돌려보낸다.
- 이슈: 스키마 초기화에서 로컬 학습 환경 문제가 있었다. C-authorization-lab과 같은 이유로 앱 시작 시 `create_all`을 호출하는 자동 초기화를 반영했다.
- 검증: compile, lint, 두 테스트 모두 통과, smoke, Compose live/ready probe 통과.
- 다음: 이 랩은 데이터 저장 경계까지만 잡고, 비동기 전달(outbox, idempotency)은 E-async-jobs-lab으로 넘긴다.

CLI:

```bash
$ python3 -m compileall app tests
$ make lint
$ make test
```

```
2 passed
```

```bash
$ make smoke
$ docker compose up --build
```

# c-authorization-lab-fastapi 문제지

## 왜 중요한가

워크스페이스 기반 협업 서비스에서 "누가 무엇을 할 수 있는가"를 명확히 해야 합니다. 초대, 역할 변경, 소유권, 읽기/쓰기 가능 범위를 코드로 표현하고, 인증 자체와는 분리해서 설명 가능한 구조를 만들어야 합니다.

## 목표

시작 위치의 구현을 완성해 워크스페이스 생성과 초대 흐름이 분리된 규칙으로 정리되어야 합니다, 역할별로 가능한 작업이 문서와 코드에서 일관되게 드러나야 합니다, owner와 일반 member의 차이가 실제 리소스 접근에 반영되어야 합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../labs/C-authorization-lab/fastapi/app/__init__.py`
- `../labs/C-authorization-lab/fastapi/app/api/__init__.py`
- `../labs/C-authorization-lab/fastapi/app/api/deps.py`
- `../labs/C-authorization-lab/fastapi/app/api/v1/__init__.py`
- `../labs/C-authorization-lab/fastapi/tests/conftest.py`
- `../labs/C-authorization-lab/fastapi/tests/integration/test_authorization_flows.py`
- `../labs/C-authorization-lab/fastapi/compose.yaml`
- `../labs/C-authorization-lab/fastapi/Makefile`

## starter code / 입력 계약

- `../labs/C-authorization-lab/fastapi/app/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 워크스페이스 생성과 초대 흐름이 분리된 규칙으로 정리되어야 합니다.
- 역할별로 가능한 작업이 문서와 코드에서 일관되게 드러나야 합니다.
- owner와 일반 member의 차이가 실제 리소스 접근에 반영되어야 합니다.
- 인가 규칙을 서비스 계층에서 테스트할 수 있어야 합니다.

## 제외 범위

- 실제 로그인 시스템과 세션 관리
- 정책 엔진 같은 고급 외부 권한 시스템
- 조직 간 멀티테넌시 전체 설계

## 성공 체크리스트

- 핵심 흐름은 `get_authorization_service`와 `get_actor_id`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `app_env`와 `client`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../labs/C-authorization-lab/fastapi/compose.yaml` fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi && PYTHONPATH=. python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi && PYTHONPATH=. python3 -m pytest
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi test
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi && python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`c-authorization-lab-fastapi_answer.md`](c-authorization-lab-fastapi_answer.md)에서 확인한다.

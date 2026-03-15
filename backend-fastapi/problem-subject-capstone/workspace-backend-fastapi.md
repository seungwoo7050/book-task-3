# workspace-backend-fastapi 문제지

## 왜 중요한가

개별 랩으로 연습한 인증, 인가, 데이터 API, 비동기 알림, 실시간 전달을 하나의 협업형 SaaS 백엔드로 다시 조합합니다. 목표는 기능을 많이 붙이는 것이 아니라, 여러 경계를 함께 설명할 수 있는 통합 구조를 만드는 것입니다.

## 목표

시작 위치의 구현을 완성해 로컬 로그인과 외부 로그인 흐름이 같은 사용자 모델 안에서 설명 가능해야 합니다, 워크스페이스 멤버십과 역할이 프로젝트/태스크/댓글 API와 연결되어야 합니다, 알림 생성이 큐와 실시간 전달로 이어지는 흐름이 보여야 합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../capstone/workspace-backend/fastapi/app/__init__.py`
- `../capstone/workspace-backend/fastapi/app/api/__init__.py`
- `../capstone/workspace-backend/fastapi/app/api/deps.py`
- `../capstone/workspace-backend/fastapi/app/api/v1/__init__.py`
- `../capstone/workspace-backend/fastapi/tests/conftest.py`
- `../capstone/workspace-backend/fastapi/tests/integration/test_capstone.py`
- `../capstone/workspace-backend/fastapi/compose.yaml`
- `../capstone/workspace-backend/fastapi/Makefile`

## starter code / 입력 계약

- `../capstone/workspace-backend/fastapi/app/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 로컬 로그인과 외부 로그인 흐름이 같은 사용자 모델 안에서 설명 가능해야 합니다.
- 워크스페이스 멤버십과 역할이 프로젝트/태스크/댓글 API와 연결되어야 합니다.
- 알림 생성이 큐와 실시간 전달로 이어지는 흐름이 보여야 합니다.
- 개별 랩의 개념이 capstone에서 어떻게 다시 조합되었는지 문서로 설명할 수 있어야 합니다.

## 제외 범위

- 프런트엔드 렌더링과 정적 자산 제공
- 실제 클라우드 배포 자동화
- 랩 코드를 공용 패키지로 묶는 리팩터링

## 성공 체크리스트

- 핵심 흐름은 `get_auth_service`와 `get_mailbox`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `app_env`와 `app_client`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../capstone/workspace-backend/fastapi/compose.yaml` fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/backend-fastapi/capstone/workspace-backend/fastapi && PYTHONPATH=. python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/capstone/workspace-backend/fastapi && PYTHONPATH=. python3 -m pytest
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/capstone/workspace-backend/fastapi test
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/capstone/workspace-backend/fastapi && python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`workspace-backend-fastapi_answer.md`](workspace-backend-fastapi_answer.md)에서 확인한다.

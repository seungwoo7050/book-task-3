# b-federation-security-lab-fastapi 문제지

## 왜 중요한가

이미 로컬 인증이 있는 서비스에 외부 로그인과 보안 강화 기능을 붙여야 한다고 가정합니다. 사용자는 Google 스타일 로그인으로 진입할 수 있어야 하고, 필요하면 2단계 인증과 recovery code를 사용할 수 있어야 합니다. 동시에 로그인 시도는 남용에 대비해 제한하고, 중요한 인증 이벤트는 기록해야 합니다.

## 목표

시작 위치의 구현을 완성해 외부 인증 공급자와 내부 사용자 계정의 연결 관계가 설명 가능해야 합니다, TOTP 등록과 검증 흐름이 독립된 단계로 구현되어야 합니다, recovery code 재생성 및 소진 규칙이 있어야 합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../labs/B-federation-security-lab/fastapi/app/__init__.py`
- `../labs/B-federation-security-lab/fastapi/app/api/__init__.py`
- `../labs/B-federation-security-lab/fastapi/app/api/deps.py`
- `../labs/B-federation-security-lab/fastapi/app/api/v1/__init__.py`
- `../labs/B-federation-security-lab/fastapi/tests/conftest.py`
- `../labs/B-federation-security-lab/fastapi/tests/integration/test_google_callback.py`
- `../labs/B-federation-security-lab/fastapi/compose.yaml`
- `../labs/B-federation-security-lab/fastapi/Makefile`

## starter code / 입력 계약

- `../labs/B-federation-security-lab/fastapi/app/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 외부 인증 공급자와 내부 사용자 계정의 연결 관계가 설명 가능해야 합니다.
- TOTP 등록과 검증 흐름이 독립된 단계로 구현되어야 합니다.
- recovery code 재생성 및 소진 규칙이 있어야 합니다.
- 로그인 throttling과 audit log가 최소 수준으로라도 동작해야 합니다.

## 제외 범위

- 실제 Google 서비스와의 end-to-end 통신 검증
- 제품 도메인별 권한과 리소스 모델
- 복수 공급자에 대한 공통 추상화 완성

## 성공 체크리스트

- 핵심 흐름은 `get_auth_service`와 `get_google_oidc_service`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `app_env`와 `client`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../labs/B-federation-security-lab/fastapi/compose.yaml` fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi && PYTHONPATH=. python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi && PYTHONPATH=. python3 -m pytest
```

```bash
make -C /Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi test
```

```bash
cd /Users/woopinbell/work/book-task-3/backend-fastapi/labs/B-federation-security-lab/fastapi && python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`b-federation-security-lab-fastapi_answer.md`](b-federation-security-lab-fastapi_answer.md)에서 확인한다.

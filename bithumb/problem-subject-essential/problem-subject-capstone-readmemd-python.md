# problem-subject-capstone-readmemd-python 문제지

## 왜 중요한가

최종 목표는 AWS-first local security control plane을 만드는 것입니다. 여러 입력을 받아 finding, exception, remediation plan, markdown report, audit event까지 한 흐름으로 연결해야 합니다.

## 목표

시작 위치의 구현을 완성해 실제 AWS 계정과 연동하지 않습니다와 외부 큐 시스템, 운영용 인증, 멀티테넌시는 다루지 않습니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/__init__.py`
- `../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/app.py`
- `../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/cli.py`
- `../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/db.py`
- `../02-capstone/10-cloud-security-control-plane/python/tests/test_api.py`
- `../02-capstone/10-cloud-security-control-plane/problem/data/broad_admin_policy.json`
- `../02-capstone/10-cloud-security-control-plane/problem/data/cloudtrail_suspicious.json`
- `../02-capstone/10-cloud-security-control-plane/problem/data/insecure_k8s.yaml`

## starter code / 입력 계약

- `../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 실제 AWS 계정과 연동하지 않습니다.
- 외부 큐 시스템, 운영용 인증, 멀티테넌시는 다루지 않습니다.

## 제외 범위

- `../02-capstone/10-cloud-security-control-plane/problem/data/broad_admin_policy.json` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `create_app`와 `_database_url`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `_data`와 `test_control_plane_end_to_end`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../02-capstone/10-cloud-security-control-plane/problem/data/broad_admin_policy.json` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/bithumb/02-capstone/10-cloud-security-control-plane/python && PYTHONPATH=src python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/bithumb/02-capstone/10-cloud-security-control-plane/python && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`problem-subject-capstone-readmemd-python_answer.md`](problem-subject-capstone-readmemd-python_answer.md)에서 확인한다.

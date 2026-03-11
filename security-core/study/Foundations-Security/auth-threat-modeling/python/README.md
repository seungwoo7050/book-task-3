# Python 구현

아래 명령은 모두 `security-core` 레포 루트 기준입니다.

## 다루는 범위

- auth scenario manifest 읽기
- control 누락을 `AUTH-001`~`AUTH-008` finding으로 변환
- `check-scenarios` summary 출력
- `demo` single-profile 출력

## 실행 예시

```bash
make venv
PYTHONPATH=study/Foundations-Security/auth-threat-modeling/python/src \
  .venv/bin/python -m auth_threat_modeling.cli check-scenarios \
  study/Foundations-Security/auth-threat-modeling/problem/data/scenario_bundle.json
```

## 테스트

```bash
make test-unit
```

## 상태

`verified`

## 구현 메모

이 프로젝트는 실제 login server가 아니라 auth design evaluator입니다. provider API, database, JWT library를 붙이지 않고도
control gap을 설명 가능한 finding으로 바꾸는 데 집중합니다.


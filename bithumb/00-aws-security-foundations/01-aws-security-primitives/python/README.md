# Python 구현

아래 내용은 모두 레포 루트 기준입니다.

## 구현한 답의 범위

- policy JSON과 request JSON을 입력으로 받습니다.
- statement별 매칭 결과와 최종 허용/거부 결정을 설명합니다.
- wildcard action/resource matching과 explicit deny 우선순위를 다룹니다.

## 핵심 엔트리포인트

- `python/src/aws_security_primitives/engine.py`
- `python/src/aws_security_primitives/cli.py`

## 실행

```bash
make venv
PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m aws_security_primitives.cli 00-aws-security-foundations/01-aws-security-primitives/problem/data/policy_allow_read.json 00-aws-security-foundations/01-aws-security-primitives/problem/data/request_read.json
```

## 테스트

```bash
PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m pytest 00-aws-security-foundations/01-aws-security-primitives/python/tests
```

## 대표 출력 예시

```json
{
  "allowed": true,
  "reason": "at least one allow matched",
  "matches": [
    {
      "sid": "AllowRead",
      "effect": "Allow",
      "matched": true,
      "reason": "action/resource matched"
    }
  ]
}
```

## 구현 메모

엔진은 외부 상태 없이 동작하는 순수 함수 형태라 테스트와 재사용이 쉽습니다.

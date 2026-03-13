# 10 Development Timeline

이 문서는 `AWS Security Primitives`를 현재 소스와 테스트만으로 다시 읽기 위해 chronology를 재구성한 기록입니다.

## Day 1
### Session 1

- 목표: 이 프로젝트가 단순 allow/deny 예제가 아니라, 왜 그런 결론이 나오는지 statement 단위 증거를 남기는 엔진인지 확인한다.
- 진행: `README.md`, `problem/README.md`, `python/README.md`, `test_engine.py`, `engine.py`를 순서대로 대조했다.
- 이슈: 처음엔 `allowed` boolean만 맞으면 충분한 연습이라고 생각했는데, 테스트와 CLI 표면을 같이 보니 이 프로젝트의 핵심은 `matches[]`에 어떤 statement가 왜 맞았는지 남기는 데 있었다.
- 판단: 이후 04번 analyzer가 이 감각 위에서 finding을 만들기 때문에, v1부터 statement별 이유를 JSON으로 설명하는 구조가 필요했다.

CLI:

```bash
$ sed -n '1,120p' 00-aws-security-foundations/01-aws-security-primitives/README.md
$ sed -n '1,120p' 00-aws-security-foundations/01-aws-security-primitives/problem/README.md
$ sed -n '1,200p' 00-aws-security-foundations/01-aws-security-primitives/python/tests/test_engine.py
$ sed -n '1,220p' 00-aws-security-foundations/01-aws-security-primitives/python/src/aws_security_primitives/engine.py
```

이 시점의 핵심 코드는 최종 우선순위를 정하는 이 짧은 분기였다.

```python
    if deny_match:
        return Decision(allowed=False, reason="explicit deny matched", matches=results)
    if allow_match:
        return Decision(allowed=True, reason="at least one allow matched", matches=results)
    return Decision(allowed=False, reason="no allow statement matched", matches=results)
```

처음엔 wildcard 매칭 함수 `_matches()`가 중심이라고 생각했지만, 실제로는 `deny_match`와 `allow_match`를 어떻게 모아서 설명 가능한 `Decision`으로 끝내느냐가 더 중요했다. 이 분기 때문에 같은 request라도 `implicit deny`와 `explicit deny`를 다른 이유 문자열로 구분해 줄 수 있다.

### Session 2

- 진행: 실제 CLI와 테스트를 다시 돌려 README의 대표 출력과 테스트 계약이 현재 코드와 맞는지 확인했다.
- 검증: allow 케이스 CLI는 `allowed: true`와 `at least one allow matched`를 출력했고, pytest는 3개 시나리오를 모두 통과했다.
- 판단: 처음 가설은 deny 케이스만 확인하면 된다는 쪽이었지만, `test_request_denied_when_no_allow_statement_matches`가 있어야 `no match`와 `explicit deny`를 같은 실패로 뭉개지지 않는다.
- 다음: 이 프로젝트는 여기서 멈추고, 04번에서 broad permission과 `iam:PassRole`을 위험 finding으로 확장한다.

CLI:

```bash
$ make venv
$ PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m aws_security_primitives.cli 00-aws-security-foundations/01-aws-security-primitives/problem/data/policy_allow_read.json 00-aws-security-foundations/01-aws-security-primitives/problem/data/request_read.json
$ PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m pytest 00-aws-security-foundations/01-aws-security-primitives/python/tests
```

출력:

```text
"reason": "at least one allow matched"
3 passed in 0.01s
```

# 개발 타임라인

## 1. 환경 준비

```bash
cd security-core
make venv
```

## 2. 시나리오 검증

```bash
make test-unit
```

성공 신호:

- `auth-threat-modeling` 시나리오 테스트와 CLI smoke test가 통과합니다.

## 3. demo 출력 확인

```bash
make demo-auth
```

성공 신호:

- control gap이 pretty JSON finding 목록으로 출력됩니다.


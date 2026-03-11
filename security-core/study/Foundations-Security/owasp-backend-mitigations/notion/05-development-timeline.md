# 개발 타임라인

## 1. 환경 준비

```bash
cd security-core
make venv
```

## 2. case 검증

```bash
make test-unit
```

## 3. demo 출력

```bash
make demo-owasp
```

성공 신호:

- secure baseline이 0 finding으로 유지되고, demo route는 deterministic finding 목록을 출력합니다.


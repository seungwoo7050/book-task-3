# 개발 타임라인

## 1. 환경 준비

```bash
cd security-core
make venv
make doctor
```

성공 신호:

- `.venv`가 준비됩니다.
- `doctor ok`가 출력됩니다.

## 2. capstone 테스트

```bash
make test-capstone
```

성공 신호:

- crypto/auth/backend/dependency evaluator 재구성 테스트가 통과합니다.
- CLI가 review JSON shape와 artifact 파일 생성 규칙을 검증합니다.

## 3. foundations 회귀 확인

```bash
make test-unit
```

성공 신호:

- foundations 4개 프로젝트의 기존 테스트가 그대로 통과합니다.

## 4. demo artifact 생성

```bash
make demo-capstone
sed -n '1,120p' .artifacts/capstone/demo/07-report.md
```

성공 신호:

- `.artifacts/capstone/demo/` 아래에 `01`~`07` 파일이 생성됩니다.
- `07-report.md`에 summary, category findings, remediation board 섹션이 모두 들어 있습니다.

## 5. 문서 표면 갱신

- 루트 `README.md`, `docs/roadmap.md`, `docs/project-catalog.md`, `study/README.md`를 capstone `verified` 상태에 맞춰 갱신합니다.
- `CURRICULUM_EXPANSION_PLAN.md`에서 `security-capstone` 행과 `security-core/study/90-capstone-collab-saas-security-review/` 상태를 올립니다.

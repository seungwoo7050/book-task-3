# demo walkthrough

`make demo-capstone`은 `.artifacts/capstone/demo/` 아래에 일곱 개 파일을 만듭니다.

## 재현 순서

```bash
cd security-core
make venv
make demo-capstone
sed -n '1,120p' .artifacts/capstone/demo/07-report.md
```

성공 신호:

- `demo assets written to .artifacts/capstone/demo`가 출력됩니다.
- `07-report.md`에 여섯 개 섹션 제목이 순서대로 들어 있습니다.

## 생성 순서

1. `01-service-profile.json`: 서비스 프로필과 summary
2. `02-crypto-findings.json`: crypto finding 목록
3. `03-auth-findings.json`: auth finding 목록
4. `04-backend-findings.json`: backend finding 목록
5. `05-dependency-items.json`: dependency triage 결과
6. `06-remediation-board.json`: 우선순위 정렬된 통합 조치 목록
7. `07-report.md`: 사람이 읽는 markdown 보고서

## 확인 포인트

- `07-report.md`의 섹션 제목이 `Service Summary`, `Crypto Findings`, `Auth Findings`, `Backend Findings`, `Dependency Queue`, `Remediation Board` 순서인지 확인합니다.
- `06-remediation-board.json`에서 `P1` 항목이 앞에 모여 있는지 확인합니다.
- `02`~`05`의 개별 결과가 foundations 프로젝트 vocabulary와 같은 control ID와 priority를 사용하는지 확인합니다.

## 발표용 읽기 순서

1. `01-service-profile.json`으로 서비스 가정과 finding 개수를 설명합니다.
2. `06-remediation-board.json`으로 어떤 항목을 먼저 고치는지 설명합니다.
3. 필요할 때만 `02`~`05`에서 각 category 근거를 보여 줍니다.
4. `07-report.md`는 review 결과를 글로 공유할 때 사용합니다.

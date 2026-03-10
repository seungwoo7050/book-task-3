# 지식 인덱스

## 이번 프로젝트에서 굳혀야 할 개념

- CSPM은 설정이 안전한지 자동으로 묻는 규칙 체계이며, 좋은 rule은 secure 입력에서 조용히 통과해야 합니다.
- shift-left 보안 관점에서 plan JSON은 매우 강한 입력입니다.
- 운영 snapshot을 함께 읽어야 정적 설정 분석이 놓치는 회전 키, 오래된 credential 같은 문제를 메울 수 있습니다.
- `control_id`가 있어야 remediation, exception, report 계층과 안정적으로 연결됩니다.

## 로컬 근거 파일

- 개념 요약: [../docs/concepts/rule-design.md](../docs/concepts/rule-design.md)
- 구현 진입점: [../python/src/cspm_rule_engine/scanner.py](../python/src/cspm_rule_engine/scanner.py)
- CLI 진입점: [../python/src/cspm_rule_engine/cli.py](../python/src/cspm_rule_engine/cli.py)
- 검증 코드: [../python/tests/test_scanner.py](../python/tests/test_scanner.py)
- 입력 fixture: [../problem/data/](../problem/data/)

## 재현 체크포인트

- `insecure_plan.json`과 `access_keys_snapshot.json`을 함께 넣었을 때 `CSPM-001`부터 `CSPM-004`까지 네 control이 모두 보이는지 확인합니다.
- `secure_plan.json`은 반드시 0건이어야 하며, 이 기준이 깨지면 rule precision 설명이 무너집니다.
- plan 기반 finding과 access key 기반 finding이 같은 출력 구조를 갖는지 확인합니다.
- 결과 JSON에서 `control_id`, `severity`, `resource_id`, `title`이 모두 있는지 봅니다.

## 다음 프로젝트로 이어지는 질문

- `06-remediation-pack-runner`는 이 finding을 받아 dry-run remediation plan으로 바꿉니다.
- `10-cloud-security-control-plane`은 같은 scan 결과를 API 요청, DB 저장, report export로 통합합니다.

## 참고 자료

- 공식 링크 정리: [../docs/references/README.md](../docs/references/README.md)
- 이전 서술형 기록: [../notion-archive/essay.md](../notion-archive/essay.md)
- 이전 작업 로그: [../notion-archive/dev-timeline.md](../notion-archive/dev-timeline.md)

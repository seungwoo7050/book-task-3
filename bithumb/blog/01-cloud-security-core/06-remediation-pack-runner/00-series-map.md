# 06 Remediation Pack Runner 읽기 지도

이 lab은 finding을 "곧바로 실행할 수정 작업"으로 보지 않고, 사람이 검토할 수 있는 remediation plan으로 먼저 바꾸는 단계다. 그래서 읽을 때도 patch 자체보다 `finding -> plan -> approval 상태`라는 계약이 어떻게 고정됐는지를 먼저 붙드는 편이 낫다.

## 먼저 붙들 질문
- 왜 첫 산출물을 실행 결과가 아니라 `RemediationPlan` 데이터로 잡았는가?
- 어떤 control은 자동 패치 후보이고, 어떤 control은 승인이나 수동 검토 대상으로 남는가?
- approval은 실제로 무엇을 바꾸고, 무엇은 아직 바꾸지 않는가?

## 이 글은 이렇게 읽으면 된다
1. 입력과 출력 경계를 먼저 본다. `sample_finding.json` 하나가 어떤 plan shape로 바뀌는지 확인한다.
2. 그다음 `control_id` 분기를 본다. `CSPM-001`, `CSPM-002`, 나머지 fallback이 각각 다른 운영 모드로 바뀐다.
3. 마지막으로 `approve()`를 본다. 이 함수가 진짜 승인 워크플로를 구현하는지, 아니면 상태 표지 정도만 담당하는지 확인한다.

## 특히 눈여겨볼 장면
- `RemediationPlan`이 summary, commands, status를 같이 들고 있어서 "실행 전 제안"을 데이터로 남긴다.
- `CSPM-001`은 Terraform patch 초안을, `CSPM-002`는 승인 전제 CLI 명령을, 나머지는 일반 운영 절차 문구를 돌려준다.
- approval 이후 바뀌는 것은 `status`와 summary 문자열뿐이라서, 실제 apply/rollback orchestration은 아직 바깥 책임으로 남아 있다.
- README의 설명과 달리 실제 CLI는 `dry-run` 서브커맨드 없이 `python -m remediation_pack_runner.cli <finding_path>` 형태로 호출된다.

## 먼저 열 문서
- [10-development-timeline.md](10-development-timeline.md)

## 이번 문서의 근거
- `README.md`
- `problem/README.md`
- `python/README.md`
- `docs/concepts/dry-run-remediation.md`
- `python/src/remediation_pack_runner/runner.py`
- `python/src/remediation_pack_runner/cli.py`
- `python/tests/test_runner.py`
- `problem/data/sample_finding.json`

# 06 Remediation Pack Runner notion 기록

## 이 문서 묶음이 하는 일

이 `notion/`은 finding 이후 단계에서 “무조건 자동 수정”이 아니라 “검토 가능한 dry-run 조치안”을 먼저 만드는 설계를 정리합니다.
현재 버전은 `runner.py`, sample finding, 테스트가 증명하는 승인 전/후 상태 전이를 기준으로 다시 썼습니다.

## 이 문서를 읽을 때 잡아야 할 질문

- 왜 모든 finding을 곧바로 patch하지 않았는가?
- `auto_patch_available`, `manual_approval_required`, `manual_review`는 어떤 운영 판단 차이를 반영하는가?
- remediation 결과가 단순 문자열이 아니라 상태 전이 모델이 되어야 하는 이유는 무엇인가?

## 추천 읽기 순서

학습자가 가장 빨리 손에 잡히는 재현 경로를 보려면 `05-reproduction-guide.md`를 초반에 읽는 편이 좋습니다.

1. [00-problem-framing.md](00-problem-framing.md): 문제와 경계를 먼저 확인합니다.
2. [05-reproduction-guide.md](05-reproduction-guide.md): 가장 짧은 재현 경로와 기대 결과를 확인합니다.
3. [01-approach-log.md](01-approach-log.md): 현재 구현 방향을 왜 택했는지 읽습니다.
4. [02-debug-log.md](02-debug-log.md): 어디서 자주 막히는지와 어떤 테스트가 근거인지 확인합니다.
5. [03-retrospective.md](03-retrospective.md): 지금 구현이 무엇을 증명했고 무엇을 의도적으로 비워 두었는지 읽습니다.
6. [04-knowledge-index.md](04-knowledge-index.md): 다음 프로젝트로 이어지는 개념과 근거 파일을 모아 봅니다.

## 이 버전의 근거

- 현재 문제 설명: [../problem/README.md](../problem/README.md)
- 현재 구현 안내: [../python/README.md](../python/README.md)
- 구현 진입점: [../python/src/remediation_pack_runner/runner.py](../python/src/remediation_pack_runner/runner.py)
- CLI 진입점: [../python/src/remediation_pack_runner/cli.py](../python/src/remediation_pack_runner/cli.py)
- 검증 코드: [../python/tests/test_runner.py](../python/tests/test_runner.py)
- 샘플 finding: [../problem/data/sample_finding.json](../problem/data/sample_finding.json)
- 이전 장문 기록: [../notion-archive/essay.md](../notion-archive/essay.md)

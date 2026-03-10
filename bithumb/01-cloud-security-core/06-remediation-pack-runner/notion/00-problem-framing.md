# 문제 프레이밍

## 이 프로젝트가 답하려는 질문

finding을 많이 만드는 것만으로는 운영자가 움직이지 않습니다. 이 프로젝트는 finding을 받아 실제 변경은 하지 않되,
사람이 검토하고 승인할 수 있는 조치 계획(`RemediationPlan`)으로 바꾸는 것이 목표입니다.

## 실제 입력과 출력

입력:
- `problem/data/sample_finding.json`

출력:
- remediation plan
- mode (`auto_patch_available`, `manual_approval_required`, `manual_review`)
- status (`pending_approval`, `approved`)
- patch 또는 command 제안 목록

## 강한 제약

- 실제 apply는 하지 않습니다.
- rollback orchestration과 change-management 도구 연동은 다루지 않습니다.
- 그러나 승인 전/후 상태와 조치안 성격은 분명하게 드러나야 합니다.

## 완료로 보는 기준

- `CSPM-001` finding에서 자동 패치 후보 plan이 생성되어야 합니다.
- approve 이후 status가 바뀌고 승인자 정보가 반영되어야 합니다.
- control_id에 따라 조치안의 성격이 달라짐을 설명할 수 있어야 합니다.

## 확인에 쓰는 근거

- 문제 설명: [../problem/README.md](../problem/README.md)
- 핵심 테스트: [../python/tests/test_runner.py](../python/tests/test_runner.py)
- 이전 배경 설명: [../notion-archive/essay.md](../notion-archive/essay.md)

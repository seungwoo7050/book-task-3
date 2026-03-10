# 접근 기록

## 핵심 선택

- remediation을 실행 결과가 아니라 plan 데이터로 정의했습니다.
- `control_id`에 따라 모드를 나누었습니다. `CSPM-001`은 auto patch 후보, `CSPM-002`는 manual approval, 나머지는 manual review입니다.
- 승인 시 기존 객체를 수정하지 않고 새 plan을 반환하도록 해 승인 전/후 상태를 분리했습니다.

## 버린 대안

- finding을 즉시 자동 적용하는 흐름은 배제했습니다. 네트워크와 IAM 변경은 사고로 이어질 수 있습니다.
- 구조화된 patch AST 대신 문자열 리스트를 남겼습니다. 현재 범위에서는 사람이 읽고 실행할 수 있는 텍스트가 더 실용적입니다.
- 모든 finding에 동일한 remediation 템플릿을 적용하는 방식은 포기했습니다. control별 성격이 다릅니다.

## 다음 프로젝트와의 연결

이 프로젝트가 있어야 finding이 운영 조치와 연결됩니다. `10-cloud-security-control-plane`의 remediation worker도
같은 `build_dry_run` 패턴을 사용하므로, 지금 단계에서 mode와 status 전이가 명확해야 합니다.

## 다시 써도 유지할 기준

- 실행보다 검토 가능성이 우선입니다.
- 승인 전/후 상태가 데이터로 남아야 합니다.
- command와 patch는 사람이 읽고 바로 판단할 수 있어야 합니다.

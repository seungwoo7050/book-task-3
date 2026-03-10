# 지식 인덱스

## 이번 프로젝트에서 굳혀야 할 개념

- `explicit deny > allow > implicit deny`는 순서를 암기하는 규칙이 아니라 테스트로 고정해야 하는 평가 규칙입니다.
- statement 적용은 `Action`과 `Resource`의 동시 매칭이 있어야 하므로, 부분 일치만 확인하면 오판이 생깁니다.
- policy evaluation 결과를 설명 가능한 레코드로 남겨야 뒤 단계에서 finding, exception, audit로 확장할 수 있습니다.
- 작은 엔진일수록 CLI 출력과 테스트 어휘가 같은지 확인하는 것이 중요합니다.

## 로컬 근거 파일

- 개념 요약: [../docs/concepts/iam-basics.md](../docs/concepts/iam-basics.md)
- 문제 범위: [../problem/README.md](../problem/README.md)
- 구현 진입점: [../python/src/aws_security_primitives/engine.py](../python/src/aws_security_primitives/engine.py)
- CLI 진입점: [../python/src/aws_security_primitives/cli.py](../python/src/aws_security_primitives/cli.py)
- 검증 코드: [../python/tests/test_engine.py](../python/tests/test_engine.py)

## 재현 체크포인트

- CLI 출력에서 `allowed`만 보지 말고 `reason`과 `matches` 배열까지 같이 확인합니다.
- secret prefix 요청은 allow가 먼저 있어도 deny가 마지막 결론을 뒤집는지 확인합니다.
- 요청 액션을 `s3:PutObject`로 바꾸면 implicit deny가 아니라 `no allow statement matched`라는 설명이 남는지 봅니다.

## 다음 프로젝트로 이어지는 질문

- `04-iam-policy-analyzer`는 같은 policy 입력을 받아 “허용 여부”가 아니라 “위험 finding”으로 바꾸는 층을 추가합니다.
- `10-cloud-security-control-plane`에서는 이 판단 결과가 API, DB, report 흐름 안으로 들어갑니다.

## 참고 자료

- 공식 링크 정리: [../docs/references/README.md](../docs/references/README.md)
- 이전 서술형 기록: [../notion-archive/essay.md](../notion-archive/essay.md)
- 이전 작업 로그: [../notion-archive/dev-timeline.md](../notion-archive/dev-timeline.md)

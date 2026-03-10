# 문제 프레이밍

## 이 프로젝트가 답하려는 질문

IAM 정책을 읽을 줄 안다는 것과, 특정 요청이 왜 허용되거나 거부되었는지 설명할 수 있다는 것은 다릅니다.
이 프로젝트는 그 간극을 줄이기 위해 `Effect`, `Action`, `Resource`, `explicit deny` 네 가지 규칙만 남긴 작은
평가 엔진을 만듭니다.

## 실제 입력과 출력

입력:
- policy JSON 1개
- request JSON 1개

출력:
- 최종 허용/거부 결정
- 어떤 statement가 매칭되었고 어떤 것은 왜 무시됐는지에 대한 설명

## 범위를 의도적으로 잘라낸 이유

- Condition keys, Principal evaluation, Policy variables를 한 번에 넣으면 “평가 흐름의 뼈대”가 흐려집니다.
- 실제 AWS API를 호출하는 순간, 학습 초점이 권한 평가 논리보다 환경 구성으로 이동합니다.
- 뒤 프로젝트에서 이 엔진을 재사용해야 하므로, 외부 상태 없는 순수 함수 구조가 더 중요합니다.

## 완료로 보는 기준

- 허용 케이스, explicit deny override, allow 부재 케이스를 모두 설명할 수 있어야 합니다.
- 단순히 `True/False`가 아니라 statement 단위 이유를 남길 수 있어야 합니다.
- 이후 `04-iam-policy-analyzer`에서 정책 위험도를 설명하는 기반으로 쓸 수 있어야 합니다.

## 확인에 쓰는 근거

- 문제 설명: [../problem/README.md](../problem/README.md)
- 핵심 테스트: [../python/tests/test_engine.py](../python/tests/test_engine.py)
- 이전 배경 설명: [../notion-archive/essay.md](../notion-archive/essay.md)

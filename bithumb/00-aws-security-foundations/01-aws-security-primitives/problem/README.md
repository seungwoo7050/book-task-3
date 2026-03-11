# 문제 정리

## 원래 문제

AWS IAM 전체를 구현하는 것이 아니라, 가장 자주 혼동되는 평가 규칙 몇 가지를 코드로 설명하는 것이 목표입니다.
특히 `Effect`, `Action`, `Resource`, `explicit deny`가 최종 decision에 어떤 순서로 반영되는지 보여 줘야 합니다.

## 제공된 자료

- `problem/data/policy_allow_read.json`
- `problem/data/request_read.json`
- policy/request 쌍을 읽는 가장 작은 CLI 흐름

## 제약

- 실제 AWS API나 계정 상태를 조회하지 않습니다.
- 학습 범위는 statement 단위 match와 우선순위 설명까지로 제한합니다.

## 통과 기준

- CLI가 allow/deny 결과와 `reason`, `matches[]`를 JSON으로 출력해야 합니다.
- 테스트가 `explicit deny`, wildcard match, no-match 시나리오를 보장해야 합니다.

## 이번 프로젝트에서 일부러 제외한 것

- condition key
- principal evaluation
- policy variable

# 01 AWS Security Primitives series map

이 시리즈는 `01-aws-security-primitives`를 "AWS IAM 전체 구현"이 아니라, 이후 analyzer와 control plane이 공통으로 기대는 가장 작은 판단 문법으로 읽는다. 실제 구현은 `Action`/`Resource` wildcard match, `explicit deny > allow > implicit deny`, 그리고 `matches[]`가 포함된 설명 가능한 JSON 출력까지다. 반대로 `Condition`, `Principal`, `NotAction`, malformed policy 방어는 현재 범위 밖이다.

## 읽는 순서

1. [10-development-timeline.md](10-development-timeline.md)
   statement match를 어떻게 근거로 남기고, 그 근거를 최종 decision과 CLI 출력으로 어떻게 닫았는지 순서대로 따라간다.

## 이 시리즈가 답하는 질문

- 왜 "allow/deny 여부"보다 먼저 statement match를 분리해서 남겨야 했는가
- deny precedence를 테스트로 잠가 두는 일이 왜 이후 IAM analyzer의 바닥이 되는가
- 이 엔진이 어디까지는 설명 가능하고, 어디부터는 아직 의도적으로 다루지 않는가

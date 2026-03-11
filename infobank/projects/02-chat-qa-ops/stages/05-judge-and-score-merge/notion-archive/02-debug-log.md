> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Judge & Score Merge — 디버깅 기록: resolution과 communication 구분 문제

## Case: 짧은 응답도 무조건 높은 resolution 점수를 받음

### 증상

"네"라는 한 글자 응답에도 resolution 점수가 높게 나왔다.
실제 상담에서 "네"만 답하면 고객 문제가 해결된 게 아니라, 그냥 수긍한 것뿐이다.
그런데 점수는 "문제를 해결했다"로 해석될 수 있는 수준이었다.

### 원인

초기 구현에서 resolution과 communication을 **같은 기준**(특정 표현의 존재 여부)으로 판단하고 있었다.
"안내"라는 단어가 있으면 resolution도 높고 communication도 높았다.

문제는 resolution은 "문제 해결 방향을 제시했느냐"이고, communication은 "표현이 명확하고 친절하냐"인데, 이 둘이 구분되지 않았다는 것이다.

### 해결

두 축을 서로 다른 기준으로 분리했다:
- **resolution**: 응답 **길이**가 10자 초과인지 확인 — 충분한 안내를 제공했을 가능성
- **communication**: "안내" 또는 "확인" **표현 유무** — 안내성 표현이 있는지

여전히 조잡하지만, 적어도 **두 축이 독립적으로 움직인다**.

### 검증

`judge_response` 구현이 길이와 표현 여부를 다른 축으로 평가한다.
`test_judge_and_score_merge`에서 "환불 정책을 확인해 안내드리겠습니다."(충분한 길이 + 안내 표현)가 높은 점수를 받는지 확인한다.

## 이 경험에서 배운 것

평가 축이 다르면 **판단 기준도 달라야** 한다.
같은 신호를 여러 축에 재사용하면, 축을 나눈 의미가 사라진다.
heuristic이 조잡하더라도, 축 간 독립성은 유지하는 게 낫다.

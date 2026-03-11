> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Golden Set & Regression — 회고

## 잘 된 것

### 메커니즘이 극단적으로 단순하다

evaluate_case()는 사실상 "집합 교집합이 비어있지 않은지" 확인하는 함수다.
이 단순함 덕분에 버그 가능성이 거의 없고, 새 팀원이 코드를 읽는 데 30초면 충분하다.

### reason code 패턴의 일관성

stage 03의 failure_types, stage 05의 judge output, stage 06의 reason_codes가 모두 같은 패턴("문자열 상수 리스트")을 따른다.
나중에 로그 분석이나 대시보드 필터링에서 이 일관성이 큰 도움이 된다.

## 아쉬운 것

### golden case 수가 너무 적다

현재 2개(gs-001, gs-002)로는 regression 탐지의 신뢰도를 주장하기 어렵다.
stage 수준에서는 메커니즘 증명이 목적이므로 의도적인 선택이지만, capstone에서는 최소 20개 이상으로 확장해야 한다.

### 점수 기반 regression은 이 stage에서 다루지 않는다

현재는 "근거 문서 포함 여부"만 확인한다.
"평균 점수가 떨어졌는가?"는 stage 07의 version compare에서 처리하지만, 이 stage에 통합되어 있으면 더 자연스러웠을 수 있다.

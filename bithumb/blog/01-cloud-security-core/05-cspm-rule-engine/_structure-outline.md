# 05 CSPM Rule Engine structure outline

## 중심 질문

- 이 engine이 왜 plan scanner를 넘어서 multi-source triage engine으로 읽혀야 하는지
- secure plan 0건과 combined CLI output이 왜 다른 층위의 진술인지

## 글 흐름

1. root module resource dispatch로 시작한다.
2. access key snapshot을 같은 finding shape로 합치는 장면을 두 번째 축으로 둔다.
3. secure plan 0건과 combined CLI 차이를 세 번째 축으로 둔다.
4. root module 한정 등 현재 입력 범위의 좁음을 마지막에 남긴다.

## 반드시 남길 증거

- `_resources()`, `scan_plan()`, `scan_access_keys()`
- insecure CLI의 `CSPM-001` ~ `CSPM-004`
- pytest `3 passed in 0.01s`
- secure plan 0건은 `scan_plan()` 기준이라는 점
- root module만 읽는 현재 구조

## 반드시 피할 서술

- secure fixture 0건을 combined CLI 전체 0건으로 오해하게 만드는 문장
- nested module까지 이미 다룬다고 보이게 하는 표현
- snapshot rule을 부가 기능처럼 축소해 쓰는 설명
- `CSPM-004`를 secure plan의 false positive처럼 묘사하는 오독

## 톤 체크

- chronology는 `plan rules -> snapshot rule -> secure 기준선 -> 현재 범위` 순서로 살아 있어야 한다.
- 홍보문보다 "같은 finding 언어로 묶인 입력들"과 "무엇이 아직 제외됐는가"가 함께 읽히는 탐색형 톤을 유지한다.

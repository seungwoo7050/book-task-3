# Debug Log

## Current recorded issue

이 랩의 현재 위험은 런타임 크래시보다 “Querydsl까지 적혀 있는데 실제로는 scaffold 수준”이라는 오해다.

- failing command or request:
  - none recorded as a blocking defect in the current pass
- exact symptom:
  - 설치된 기술 키워드가 구현 깊이보다 더 커 보일 수 있다
- first incorrect assumption:
  - dependency를 추가한 것만으로도 학습 목표를 충분히 달성했다고 보기 쉽다
- evidence collected:
  - docs는 Querydsl이 installed but not exercised deeply yet라고 분명히 적는다

## Root cause

JPA 랩은 특히 keyword inflation이 일어나기 쉽다. 실제 query complexity와 entity boundary가 기술 이름보다 더 중요하다.

## Fix and verification

- code or config change made:
  - tracked docs에서 current implementation과 next improvements를 분리했다
- why that change addresses the cause:
  - 독자가 현재 증명된 범위만 읽을 수 있다
- command, test, or log line that proved the fix:
  - `make test`
  - `make smoke`

## Follow-up debt

- Querydsl real query 예시를 추가해야 한다
- N+1 regression test와 soft delete까지 연결해야 한다


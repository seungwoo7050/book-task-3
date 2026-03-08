# 포지셔닝

`Ops Triage Console`은 “React internals를 공부한 사람”이 아니라 “제품형 프론트 업무를 맡길 수 있는 사람”이라는 신호를 주기 위해 설계했다.

## 왜 이 도메인인가

- B2B 운영 콘솔은 테이블, 필터, 상태 전이, 정보 밀도, 오류 복구를 한 번에 보여 주기 좋다.
- 소비자 앱보다 데이터 해석과 업무 흐름 설계 능력을 더 직접적으로 보여 줄 수 있다.
- 한 화면에서 여러 종류의 품질 문제를 다루게 되므로 우선순위 판단과 UX 구조화가 중요해진다.

## 이 앱이 보여 주는 역량

- query/filter/sort/pagination 모델링
- async 상태와 retry 설계
- optimistic update와 rollback 처리
- 저장된 뷰와 bulk action
- dense but calm한 UI 톤 조절


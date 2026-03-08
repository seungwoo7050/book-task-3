# Query Navigation

이 explorer는 `search`, `category`, `item`을 URL에 반영한다.

- `search`
  - 현재 결과 집합을 재현하기 위한 최소 입력
- `category`
  - 결과 범위를 제한하는 공유 가능한 필터
- `item`
  - detail pane에서 어떤 문서를 보고 있는지 나타내는 선택 상태

URL에 넣지 않은 것은 `simulateFailureNext` 같은 디버그성 상태다. 이런 값은 공유 링크보다 로컬 실험 문맥에 가깝기 때문이다.

이 경계는 다음 포트폴리오 프로젝트에서도 그대로 재사용할 수 있다. 공유 가능한 view state와 로컬 실험 상태를 나누는 감각이 생기기 때문이다.

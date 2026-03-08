# State And URL Boundaries

이 프로젝트는 브라우저 상태를 세 층으로 나눈다.

- URL state
  - search, status, sort처럼 공유 가능한 query만 넣는다.
- local persisted state
  - items, selected row처럼 새로고침 뒤에도 유지할 문맥을 저장한다.
- ephemeral UI state
  - 현재 editing row처럼 잠깐만 필요한 상태는 메모리에서만 둔다.

이 경계를 분리하면 "무엇이 링크로 공유되는가"와 "무엇이 개인 작업 문맥인가"를 설명하기 쉬워진다.

이 프로젝트에서 URL이 localStorage보다 우선하는 이유도 여기 있다. 공유 링크는 현재 view를 강제해야 하고, 그 외 개인 문맥은 저장값에서 복원하면 된다.

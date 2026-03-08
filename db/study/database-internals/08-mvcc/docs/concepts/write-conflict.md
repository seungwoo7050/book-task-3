# Write Conflict

- 이 프로젝트는 first-committer-wins 규칙을 사용한다.
- 내 snapshot 이후에 다른 committed transaction이 같은 key를 썼다면 commit은 실패한다.
- abort는 해당 tx가 쓴 version만 version chain에서 제거한다.


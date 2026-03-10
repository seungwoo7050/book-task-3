# 01. 접근 기록

## 실제로 택한 접근

이 프로젝트는 기능을 한 번에 넣지 않았다.

1. sequential forwarding 먼저 완료
2. detached thread 추가
3. 마지막에 cache 추가

각 단계가 끝날 때마다 local origin harness로 다시 검증했다.

## 왜 이 순서를 택했는가

- URI parsing과 header rewrite가 틀리면 뒤의 동시성 검증도 의미가 없다
- concurrency bug와 cache bug를 동시에 잡으려 하면 원인 분리가 안 된다
- 단계별로 테스트를 붙이면 문서도 자연스럽게 마일스톤 구조가 된다

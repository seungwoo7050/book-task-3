# OSS 포지셔닝

## 의도한 사용처

`v3-oss-hardening`은 “추천 시스템 데모”가 아니라, 한 팀이 self-hosted로 MCP catalog와 release gate를 운영해 보는 reference implementation이다.

이 프로젝트가 특히 유용한 경우:

- MCP 추천 시스템을 어떻게 운영형 구조로 바꾸는지 배우고 싶을 때
- baseline -> rerank -> gate -> artifact 흐름을 작은 팀 도구로 보고 싶을 때
- 바로 SaaS를 만들 생각은 없지만 self-hosted starter가 필요할 때

## 이 문서가 다루지 않는 것

- multi-tenant SaaS
- managed cloud service
- external integration-heavy production product
- zero-config enterprise platform

## 왜 v3가 필요한가

`v2`는 capstone으로 끝났다. 하지만 “그래서 남이 설치해서 쓸 수 있나?”라는 질문에는 아직 답이 약했다. `v3`는 그 질문에 답하기 위해 auth, roles, jobs, audit, compose를 추가했다.

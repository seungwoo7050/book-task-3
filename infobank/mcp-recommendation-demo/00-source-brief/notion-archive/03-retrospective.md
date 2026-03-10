# Source Brief — 회고

## 잘 된 것

### catalog seed가 다양한 테스트 시나리오를 커버한다

10+ 도구를 의도적으로 선정한 덕분에, 이후 stage에서:
- keyword 매칭 (baseline selector)
- category 필터링 (reranker)
- semver 호환성 (compatibility gate)
- deprecation 체크 (release gate)
를 모두 테스트할 수 있었다.

### reference spine이 짧아서 팀원이 빠르게 이해한다

문서 2개로 프로젝트 범위를 설명할 수 있다.
각 stage별 상세는 해당 stage의 docs/에 있으므로, 중복이 없다.

## 아쉬운 것

### 실제 MCP 서버와의 연동 부재

seed 데이터로만 동작하므로, 실제 도구의 응답 시간이나 안정성을 반영하지 못한다.
v3에서 Docker Compose로 일부 도구를 실제 실행할 수 있지만, 여전히 시뮬레이션 수준이다.

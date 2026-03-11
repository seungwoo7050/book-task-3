> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Registry Catalog & Manifest Schema — 회고

## 잘 된 것

### schema-first 접근이 전체 프로젝트를 안정화시킨다

Zod manifest schema를 확정한 뒤, 모든 stage가 이 schema에 의존한다.
recommendation service, eval service, compatibility gate, release gate 모두
catalog entry가 이 schema를 따른다는 가정 위에 구현되었다.

schema를 먼저 고정하면, 생각보다 많은 설계 결정이 자동으로 따라온다.

### seed 데이터가 모든 stage의 기반이 된다

catalog.ts의 seed 데이터를 바꾸면 eval 결과, 추천 결과, compatibility 체크 결과가 모두 바뀐다.
이건 seed 데이터가 "테스트 데이터"가 아니라 "시스템의 상태"라는 뜻이다.

## 아쉬운 것

### 실제 MCP 도구의 manifest를 자동으로 가져오는 기능이 없다

현재는 수동으로 catalog.ts에 추가해야 한다.
실제 운영에서는 MCP 서버에서 manifest를 자동 수집하는 connectors가 필요하다.
v3 non-goals에 명시적으로 제외되어 있다.

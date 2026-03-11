> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Registry Catalog & Manifest Schema — 문제 정의

## 풀어야 하는 문제

추천 시스템이 "무엇을" 추천하는지를 정의해야 한다.
MCP 도구는 각각 이름, 버전, 카테고리, 입출력 규격을 가진다.
이걸 자유 형식으로 관리하면 추천 로직이 불안정해진다.

## manifest schema라는 접근

모든 MCP 도구가 따라야 하는 **단일 스키마**를 Zod로 정의한다.
스키마를 통과하지 못하는 도구는 catalog에 등록할 수 없다.

이걸 "manifest validation"이라고 부른다.
API 레벨에서 manifest 검증 엔드포인트를 제공하면,
새 도구를 등록하기 전에 스키마 적합성을 확인할 수 있다.

## seed catalog

개발과 테스트를 위해 미리 정의된 도구 목록이 필요하다.
catalog.ts에 10+ MCP 도구를 하드코딩하고, `pnpm seed` 스크립트로 DB에 삽입한다.

seed가 중요한 이유:
1. offline eval이 seed 데이터를 기반으로 동작한다
2. 대시보드에서 보여줄 데이터가 있어야 한다
3. 추천 알고리즘의 동작을 검증할 수 있다

## 제약

- 실시간 도구 등록/삭제 API는 v1 capstone에서 추가된다
- seed 데이터는 deterministic이어야 한다 (매번 같은 결과)

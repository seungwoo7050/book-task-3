> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Registry Catalog & Manifest Schema — 지식 인덱스

## 핵심 개념

| 개념 | 설명 | 관련 파일 |
|------|------|-----------|
| manifest schema | MCP 도구 메타데이터의 Zod 스키마. name, version, category, inputs, outputs 등 | `shared/src/contracts.ts` |
| catalog entry | manifest + status + exposure를 포함한 catalog 등록 항목 | `shared/src/catalog.ts` |
| seed catalog | 개발/테스트용으로 미리 정의된 도구 목록 (10+) | `shared/src/catalog.ts` |
| seed script | catalog.ts의 도구를 DB에 upsert하는 스크립트 | `node/src/scripts/seed.ts` |
| manifest validation | manifest JSON이 Zod schema를 통과하는지 검증하는 API | `POST /api/manifests/validate` |
| upsert | 이미 있으면 업데이트, 없으면 삽입. seed 반복 실행 안전성 보장 | `seed.ts → onConflictDoUpdate` |

## 구현 위치

| 기능 | capstone 버전 | 파일 |
|------|--------------|------|
| Zod manifest schema | v0 | `shared/src/contracts.ts` |
| seed catalog | v0 | `shared/src/catalog.ts` |
| seed script | v0 | `node/src/scripts/seed.ts` |
| manifest validation test | v0 | `node/tests/manifest-validation.test.ts` |
| catalog CRUD API | v1 | `node/src/repositories/catalog-repository.ts` |

## 다음 단계 연결

- **stage 03**: catalog entry에 한국어 노출 필드(tagline, description, differentiator) 설계
- **stage 04**: catalog의 도구에 대해 baseline selector가 추천을 실행

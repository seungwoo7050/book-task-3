> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Selection Rubric & Eval Contract — 개발 타임라인

## 1단계: contracts.ts에 eval schema 추가

```bash
cd shared/src
# contracts.ts에 offlineEvalCaseSchema 추가
```

기존 mcpManifestSchema, catalogEntrySchema 아래에 eval 관련 schema를 추가했다.
eval case의 expected 배열에 rank 필드를 포함시키는 것이 핵심 결정이었다.

## 2단계: eval.ts에 eval case 작성

```bash
# eval.ts에 실제 eval case 추가
```

작성한 eval case 시나리오:
- 릴리즈 체크 요청 → release-check-bot 기대
- semver 호환성 확인 → compatibility checker 기대
- 한국어 문서 검색 → korean-docs-search 기대
- 스키마 분석 → postgres-schema-mapper 기대

## 3단계: eval-service.ts 구현

```bash
cd 08-capstone-submission/v0-initial-demo/node/src/services
touch eval-service.ts
```

구현 흐름:
1. eval case를 shared에서 import
2. each case에 대해 recommendation-service.recommend() 호출
3. 반환된 추천 목록과 expected를 비교
4. rubric 축별 점수 계산
5. 결과 객체 반환

## 4단계: integration test 작성

```bash
cd 08-capstone-submission/v0-initial-demo/node/tests
touch routes.integration.test.ts
```

```bash
pnpm test
```

테스트 내용:
- eval endpoint가 200 반환
- 결과에 caseId, passed, scores가 포함
- scores에 relevance, rankAccuracy 키가 존재

## 5단계: pnpm eval 스크립트 추가

```bash
# package.json에 eval 스크립트 추가
```

```json
{
  "scripts": {
    "eval": "tsx src/scripts/run-eval.ts"
  }
}
```

```bash
pnpm eval
# 전체 eval case 실행 + 결과 요약 출력
```

## 비고

- 이 stage의 실제 구현은 v0 capstone에 있다. stage 01 폴더는 문서만 포함한다.
- threshold 값은 v0 baseline 결과를 확인한 후 설정했다.
- `pnpm eval`은 DB가 seed된 상태에서만 동작한다 (`pnpm seed` 필요).

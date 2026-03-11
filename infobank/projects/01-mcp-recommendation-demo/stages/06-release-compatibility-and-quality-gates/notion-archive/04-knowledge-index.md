> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Release Compatibility & Quality Gates — 지식 인덱스

## 핵심 개념

| 개념 | 설명 | 관련 파일 |
|------|------|-----------|
| release candidate (RC) | 배포 준비가 된 도구 버전. gate를 통과하면 실제 배포로 승격 | `release-gate-service.ts` |
| compatibility gate | semver 분석으로 호환성 판정. major=breaking, minor=feature, patch=fix | `compatibility-service.ts` |
| release gate | 여러 검사(compatibility, eval, deprecated)를 종합하여 PASS/FAIL 판정 | `release-gate-service.ts` |
| artifact export | gate 실행 결과를 JSON으로 내보내는 기능. 감사 추적 용도 | `artifact-service.ts` |
| semver diff | 두 버전의 major/minor/patch 차이 분석 | `compatibility-service.ts` |
| breaking change | major 버전 변경으로 인한 하위 호환성 미보장 | compatibility report |
| dry-run | DB에 기록하지 않고 결과만 반환하는 실행 모드 | service options |

## CLI 명령어

| 명령어 | 설명 |
|--------|------|
| `pnpm compatibility <rc-id>` | compatibility gate 실행 |
| `pnpm release:gate <rc-id>` | release gate 실행 |
| `pnpm artifact:export <rc-id>` | artifact JSON 내보내기 |

## 구현 위치

| 기능 | capstone 버전 | 파일 |
|------|--------------|------|
| compatibility service | v2 | `node/src/services/compatibility-service.ts` |
| release gate service | v2 | `node/src/services/release-gate-service.ts` |
| artifact service | v2 | `node/src/services/artifact-service.ts` |
| compatibility test | v2 | `node/tests/compatibility-service.test.ts` |
| release gate test | v2 | `node/tests/release-gate-service.test.ts` |

## 다음 단계 연결

- **stage 07**: gate 결과를 대시보드에서 RC 단위로 시각화
- **capstone v3**: gate 실행을 background job으로 처리, audit log 기록

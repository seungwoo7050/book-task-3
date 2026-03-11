> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Release Compatibility & Quality Gates — 디버그 기록

## semver 파싱 엣지 케이스

### 상황

"1.0.0-beta.1" 같은 pre-release 버전을 파싱할 때,
단순 split('.')으로는 "0-beta" 부분이 숫자로 변환되지 않았다.

### 해결

semver 라이브러리를 사용하지 않고, 직접 파싱했다:

```typescript
const [major, minor, patchStr] = version.split('.');
const patch = parseInt(patchStr.split('-')[0], 10);
const prerelease = patchStr.includes('-') ? patchStr.split('-').slice(1).join('-') : null;
```

pre-release 버전은 같은 major.minor.patch보다 항상 이전 버전으로 취급한다.

## gate FAIL인데 artifact export가 되는 문제

### 상황

release gate가 FAIL인 RC에 대해 artifact:export를 실행하면
FAIL 결과가 담긴 artifact가 생성되었다.
이게 의도된 동작인지 혼란이 있었다.

### 해결

의도된 동작이다.
FAIL artifact도 "왜 이 버전을 배포하면 안 되는지"의 증거이므로 보존 가치가 있다.
artifact에 `overallStatus: "FAIL"` 필드가 명시적으로 포함되어 있어서
실수로 FAIL artifact를 PASS로 오인할 위험은 없다.

## dry-run pipeline과 실제 실행의 차이

### 상황

v2에서 dry-run 모드를 추가했는데,
dry-run에서는 DB에 기록하지 않고 결과만 반환해야 한다.

### 해결

각 service에 `dryRun: boolean` 옵션을 추가했다:

```typescript
async function runReleaseGate(rcId: string, options?: { dryRun?: boolean }) {
  // ... gate 실행
  if (!options?.dryRun) {
    await saveGateResult(result);
  }
  return result;
}
```

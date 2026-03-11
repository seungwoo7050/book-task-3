> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Monitoring Dashboard — 디버그 기록

## version compare 드롭다운 초기값 문제

### 상황

Overview 페이지에서 version compare 섹션을 구현할 때,
baseline과 candidate를 드롭다운으로 선택하게 했다.

초기값을 useState로 "v1.0"/"v1.1"로 하드코딩했는데,
overview API에서 `run_labels` 배열이 내려오면 그걸 기반으로 초기값을 설정해야 했다.

문제: useEffect에서 overview 데이터를 받아온 뒤 setBaseline/setCandidate를 호출하면,
이미 사용자가 드롭다운을 변경한 경우 값이 덮어씌워진다.

### 해결

setState에 함수형 업데이트를 사용했다:

```typescript
setBaseline((current) => current || overview.run_labels[0] || "v1.0");
```

`current`가 이미 있으면(사용자가 변경했으면) 유지하고,
없을 때만 API에서 받은 값으로 채운다.

## CORS 처리

### 상황

React 개발 서버(localhost:5173)에서 FastAPI 서버(localhost:8000)로 요청을 보내면 CORS 에러가 발생한다.

### 해결

Vite의 proxy 설정으로 처리했다:

```typescript
// vite.config.ts
server: {
  proxy: {
    '/api': 'http://localhost:8000'
  }
}
```

프로덕션에서는 같은 도메인에서 서빙하므로 CORS 문제가 없다.

## 테스트에서 API 모킹

### 상황

Overview.test.tsx에서 실제 API를 호출할 수 없으므로,
apiGet/apiPost를 모킹해야 한다.

### 해결

`testUtils.ts`에 공통 모킹 유틸리티를 만들고,
각 테스트에서 `vi.mock('../api/client')`로 모듈 단위 모킹을 적용했다.

SNAPSHOT 데이터를 그대로 모킹 반환값으로 사용하면,
프론트엔드가 실제 API 응답을 정확히 렌더링하는지 검증할 수 있다.

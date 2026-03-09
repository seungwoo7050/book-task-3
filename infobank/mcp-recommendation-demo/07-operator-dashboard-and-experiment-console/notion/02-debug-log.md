# 02 — 디버그 기록: 대시보드 구축 과정에서 만난 문제들

## 문제 1: Next.js fetch 캐시로 인한 stale 상태

### 증상

Catalog를 수정한 뒤 "저장" 버튼을 눌러도 목록이 갱신되지 않는다.  
새로고침하면 반영되어 있다.

### 원인

Next.js 13+ App Router는 `fetch()`에 기본적으로 `force-cache`를 적용한다.  
클라이언트 컴포넌트(`"use client"`)에서도 이 동작이 간섭할 수 있다.

### 해결

`apiFetch` 유틸에 `cache: "no-store"`를 일괄 적용했다:

```typescript
const response = await fetch(`${apiBaseUrl}${path}`, {
  ...init,
  cache: "no-store"
});
```

대시보드는 매번 "지금 서버의 최신 상태"를 보여줘야 하기 때문에 캐시를 완전히 끈 것이 맞다.  
일반 사용자 앱이었다면 SWR이나 React Query의 `staleTime` 전략을 쓰겠지만, 운영 콘솔에서는 과잉이다.

## 문제 2: loadAll() 에러 한 개가 전체를 가린다

### 증상

5개(v1) 또는 9개(v2) API를 `Promise.all`로 병렬 호출하는데, 하나라도 실패하면 전부 catch에 잡힌다.  
서버가 부분적으로만 올라왔을 때(예: catalog는 되는데 eval은 아직 안 됨) 빈 화면이 나온다.

### 원인

`Promise.all`은 하나라도 reject되면 즉시 전체를 reject한다.

### 해결 — 의도적으로 유지

`Promise.allSettled`로 바꾸면 부분 성공을 처리할 수 있지만, 이 프로젝트에서는 의도적으로 `Promise.all`을 유지했다.  
이유: 운영 콘솔이 부분적으로 로드된 상태에서 운영자가 작업하면 더 큰 혼란을 야기한다.  
대신 `useEffect` catch에서 에러 메시지를 명확히 표시한다:

```typescript
void loadAll().catch((loadError) => {
  setError(loadError instanceof Error ? loadError.message : "초기 데이터를 불러오지 못했습니다.");
});
```

## 문제 3: select 초기값이 없어서 CRUD가 동작하지 않음

### 증상

페이지 최초 렌더링 시 `selectedCatalogId`가 `"release-check-bot"`으로 하드코딩되어 있는데, seed 데이터에 해당 ID가 없으면 `selectedCatalog`이 `null`이 되어 "저장" 버튼이 아무 동작도 하지 않는다.

### 원인

`useMemo`에서 `.find()`가 실패하면 `undefined` → `?? null`로 떨어진다.  
`saveCatalog()`는 `if (!selectedCatalog) return;` guard가 있어서 조용히 실패한다.

### 해결

seed 데이터에 `release-check-bot` ID가 반드시 존재하도록 catalog seed를 확인했다.  
shared 패키지의 `catalog.ts`에서 해당 ID가 포함된 세트를 export하고 있으므로, seed가 제대로 실행되면 문제없다.  
진짜 방어 로직은 seed 실행 순서를 보장하는 것이다.

## 문제 4: Playwright e2e에서 한글 정규식 매칭 실패

### 증상

e2e 테스트에서 candidate 추천 결과의 한글 설명 텍스트를 정규식으로 검증했는데, 간헐적으로 실패한다.

```typescript
await expect(
  page.getByText(
    /Release Check Bot는 release-management, changesets, semver 역량이 직접 맞습니다\..*실사용 신호/i
  )
).toBeVisible();
```

### 원인

API 응답의 `explanationKo` 필드에 줄바꿈이 포함될 수 있다.  
`.`는 기본적으로 줄바꿈을 매칭하지 않는다.

### 해결

정규식에서 `.*` 대신 `[\s\S]*`를 쓰거나, 핵심 키워드만 매칭하는 방식으로 변경했다.  
또는 `.toContainText()`를 사용해서 부분 문자열 매칭으로 우회한다.

## 문제 5: v2 대시보드에서 RC 삭제 후 selectedReleaseCandidateId가 stale

### 증상

Release Candidate를 삭제한 뒤에도 `selectedReleaseCandidateId`가 삭제된 RC의 ID를 가리키고 있어서, 이후 "수정" 버튼을 누르면 404가 반환된다.

### 해결

catalog 삭제와 동일한 패턴을 적용했다:

```typescript
async function removeReleaseCandidate() {
  if (!selectedReleaseCandidate) return;
  await apiFetch(`/api/release-candidates/${selectedReleaseCandidate.id}`, { method: "DELETE" });
  setSelectedReleaseCandidateId("");  // 초기화
  await loadAll();
}
```

삭제 직후 선택 ID를 빈 문자열로 리셋하고, `loadAll()` 후 목록의 첫 번째 항목을 자동 선택하는 로직을 추가했다.

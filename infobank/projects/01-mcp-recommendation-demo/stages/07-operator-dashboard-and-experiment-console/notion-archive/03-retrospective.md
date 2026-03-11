> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# 03 — 회고: 단일 컴포넌트 대시보드의 빛과 그림자

## 잘된 점

### 1. "한 화면에 모든 것"이 운영 효율을 올렸다

catalog 확인 → 추천 실행 → compare 확인 → feedback 입력 → 실험 관리까지,  
운영자가 페이지를 이동하지 않고 하나의 화면에서 전체 사이클을 돌릴 수 있다.

탭이나 라우터로 분리했다면 "지금 compare 결과를 보면서 feedback을 남기고 싶다" 같은 동시 참조가 불가능했을 것이다.

### 2. loadAll() 패턴의 단순함

모든 CRUD 동작 후 `await loadAll()`을 호출하는 것은 원시적이지만 확실하다.  
낙관적 업데이트를 쓰면 코드가 복잡해지고, 서버 상태와 UI 상태가 어긋날 가능성이 생긴다.  
운영 콘솔에서는 "정확함 > 속도"이므로 이 트레이드오프가 적절했다.

### 3. buildSampleCatalogEntry / buildSampleReleaseCandidate

seed 데이터를 기반으로 샘플 엔트리를 생성하는 빌더 함수를 대시보드에 내장한 것은 좋은 판단이었다.  
운영자가 "테스트용 MCP를 하나 만들어서 실험에 넣어보자"를 버튼 하나로 할 수 있다.  
이것은 개발 도구이자 운영 도구로서의 대시보드 역할을 동시에 수행한다.

### 4. e2e 테스트가 실제 운영 동선을 커버

Playwright 테스트가 "Candidate 실행 → Release Gate 실행 → 결과 확인"이라는 핵심 동선을 따라간다.  
이것만으로 API 연결, UI 렌더링, 비동기 상태 갱신이 모두 동작하는지 확인할 수 있다.

## 개선이 필요한 점

### 1. 컴포넌트가 너무 크다

v1 기준 550줄, v2는 800줄 이상.  
`useState` 14개(v1) → 20개 이상(v2)은 인지 부하가 크다.

**개선 방향**: 섹션별 커스텀 훅으로 분리할 수 있다:

```
useRecommendation() → query, desiredCapabilities, baseline/candidate 결과
useCatalogCrud() → selectedCatalogId, summaryDraft, freshnessDraft
useExperiment() → experimentName, hypothesis, experiments 목록
useFeedback() → feedbackCatalogId, feedbackNote, feedbackDelta
useReleaseConsole() → releaseCandidates, compatibility, gate, artifact
```

### 2. 에러 상태가 글로벌 1개

`error` 상태가 하나뿐이라 "Catalog 수정과 Experiment 삭제를 동시에 시도했을 때" 어느 쪽이 실패했는지 구분할 수 없다.  
각 섹션에 독립적인 에러 상태를 두거나, toast 알림을 쓰는 것이 나았을 것이다.

### 3. 한국어 UI 텍스트의 하드코딩

버튼 레이블, placeholder, 에러 메시지가 모두 한국어 문자열로 컴포넌트 안에 하드코딩되어 있다.  
국제화(i18n)가 필요하면 전면 리팩터링이 불가피하다.  
다만 이 프로젝트는 한국 시장 MCP 추천이 주제이므로, 현재로서는 적절한 선택이다.

### 4. 테스트 커버리지가 e2e happy path 하나

실패 케이스(API 에러, 빈 catalog, 잘못된 입력)가 테스트되지 않는다.  
운영 콘솔이라 사용자 수가 적으니 치명적이진 않지만, regression 방지를 위해 unit test도 있으면 좋았을 것이다.

## 핵심 교훈

> 운영 콘솔은 "사용자 앱"이 아니라 "개발자가 쓰는 도구"다.  
> UX 완성도보다 기능 커버리지와 정확한 상태 표시가 중요하다.  
> 코드 구조적 우아함은 "동작하는 콘솔"을 만든 뒤에 개선하면 된다.

v1에서 "일단 돌아가는 단일 컴포넌트"를 만들고, v2에서 Release Console을 추가하는 점진적 확장이  
이 프로젝트의 반복적 개선 패턴과 잘 맞았다.

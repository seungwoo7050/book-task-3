> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Monitoring Dashboard — 접근 기록

## FastAPI snapshot API 설계

### 엔드포인트 결정

프론트엔드 4개 페이지에 필요한 데이터를 역으로 추적해서 엔드포인트를 결정했다:

| 엔드포인트 | 메서드 | 페이지 | 반환 데이터 |
|-----------|--------|--------|------------|
| `/api/dashboard/overview` | GET | 개요 | avg_score, fail_rate, critical_count, grade_distribution |
| `/api/dashboard/failures` | GET | 실패 분석 | failure_type별 count, critical_count, avg_score |
| `/api/conversations` | GET | 세션 리뷰 | 세션 목록 (id, score, grade, created_at) |
| `/api/conversations/{id}` | GET | 세션 리뷰 상세 | 턴 목록 + 각 턴의 evaluation (lineage, judge_trace 포함) |
| `/api/golden-set/run` | POST | 평가 실행 | golden run 결과 (avg_score, pass/fail counts) |
| `/api/dashboard/version-compare` | GET | 개요 하단 | baseline vs candidate 비교 데이터 |

### SNAPSHOT dict 구조

모든 응답 데이터를 하나의 SNAPSHOT dict에 몰아넣었다.
왜? API 계약을 한 파일에서 한눈에 볼 수 있게 하기 위해서다.

SNAPSHOT의 compare 데이터는 실제 stage 06의 golden set 결과를 기반으로 한다:
- baseline(v1.0): avg_score 84.06, critical 2, pass 16, fail 14
- candidate(v1.1): avg_score 87.76, critical 0, pass 19, fail 11
- delta: +3.7점, pass +3개, fail -3개, critical -2개

이 수치들이 의미하는 건: v1.1이 v1.0보다 모든 지표에서 개선되었다는 것.

## React 대시보드 구현

### 기술 스택 선택

- **React + TypeScript**: 타입 안전성
- **Vite**: 빌드 속도
- **React Router**: 클라이언트 사이드 라우팅
- **Vitest + Testing Library**: 컴포넌트 테스트

별도의 상태 관리 라이브러리(Redux, Zustand 등)는 사용하지 않았다.
useState + useEffect로 충분한 규모이기 때문이다.

### 컴포넌트 구조

```
src/
  App.tsx              — 라우터 + 사이드바 레이아웃
  pages/
    Overview.tsx       — 개요 + version compare
    Failures.tsx       — failure_type 테이블
    SessionReview.tsx  — 세션 목록 + 상세 뷰
    EvalRunner.tsx     — golden run 트리거 + 결과
  components/
    ScoreCard.tsx      — 점수/등급 카드 UI
    FailureTable.tsx   — failure 목록 테이블
  api/
    client.ts          — fetch wrapper (apiGet, apiPost)
  i18n/
    ko.ts              — 한국어 라벨 매핑
```

### i18n 처리

grade를 한국어로 표시하기 위해 `i18n/ko.ts`에 매핑을 넣었다.
라이브러리(i18next 등)는 사용하지 않고, 단순 객체 매핑으로 처리했다.

### lineage 표시

세션 상세 뷰에서 각 평가의 lineage(run_label, dataset, trace_id, retrieval_version)를 표시한다.
이건 "이 평가가 어떤 환경에서, 어떤 데이터셋으로, 어떤 retrieval 버전으로 실행되었는지" 추적하기 위한 것이다.

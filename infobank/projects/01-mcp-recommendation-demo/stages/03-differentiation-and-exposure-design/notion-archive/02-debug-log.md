> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Differentiation & Exposure Design — 디버그 기록

## 한국어 tagline 줄바꿈 문제

### 상황

대시보드 카드에서 한국어 tagline이 길면 줄바꿈이 어색하게 발생했다.
"PostgreSQL 테이블 구조를 분석하고 변경 영향 범위를 파악합니다"가
"PostgreSQL 테이블 구조를 분석하" + "고 변경 영향 범위를 파악합니다"로 잘렸다.

### 해결

tagline을 15자 이내로 제한하는 가이드라인을 정했다.
긴 설명은 description에 넣고, tagline은 핵심 기능만 요약한다.

예: "스키마 영향 분석" (7자) → 줄바꿈 없이 표시됨.

## exposure 누락 시 fallback 처리

### 상황

catalog의 일부 도구에 exposure.ko가 없다.
대시보드에서 이 도구들이 빈 카드로 표시되었다.

### 해결

React 컴포넌트에서 fallback 로직 추가:

```typescript
const tagline = entry.exposure?.ko?.tagline ?? entry.description;
```

exposure.ko가 없으면 영문 description을 표시하되,
시각적으로 구분하기 위해 회색 텍스트로 렌더링한다.

## reason 중복 표시 문제

### 상황

reason template에서 도구 이름이 이미 카드 제목에 표시되는데,
reason 문장에도 도구 이름이 반복되어 "release-check-bot — release-check-bot을 추천합니다"처럼 보였다.

### 해결

reason 문장에서 도구 이름을 제거하고 동사로 시작하도록 변경:
"릴리즈 호환성을 자동으로 검증합니다. 사용자의 릴리즈 체크 요청과 가장 관련성이 높습니다."

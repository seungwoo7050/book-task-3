> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Source Brief — 디버그 기록

## 한국어 노출 필드 스키마 결정

### 상황

catalog의 각 도구에 한국어 description을 넣어야 하는데,
기존 영문 description과 어떻게 공존시킬지 결정해야 했다.

옵션 1: `description_ko` 필드 추가
옵션 2: `i18n: { ko: { description: "..." } }` 중첩 구조
옵션 3: `exposure: { ko: { tagline: "...", description: "..." } }` 별도 객체

### 결론

옵션 3을 선택했다.
이유: 한국어 노출은 단순 번역이 아니다. tagline(짧은 문구), description(설명), differentiator(차별점)까지 포함해야 한다.
영문 description과 구조가 다르므로 별도 객체가 맞다.

## eval case의 정답 순위 문제

### 상황

eval.ts에서 각 case의 기대 출력을 정의할 때,
1순위 도구만 기록하면 "2순위도 합리적인 추천"인 경우를 놓친다.

### 해결

기대 출력을 배열로 만들어 순위를 포함시켰다:

```typescript
expected: [
  { toolId: "release-check-bot", rank: 1 },
  { toolId: "github-repo-inspector", rank: 2 }
]
```

eval 평가 시 rank 1을 맞추면 만점, rank 2까지 맞추면 가산점을 주는 방식으로 설계했다.

> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Differentiation & Exposure Design — 접근 기록

## exposure 구조 설계

catalog.ts의 각 도구에 exposure 객체를 추가해야 했다.

최종 구조:

```typescript
exposure: {
  ko: {
    tagline: "짧은 한 줄 설명",
    description: "운영자가 이해할 수 있는 2-3문장 설명",
    differentiator: "비슷한 도구 대비 이 도구만의 장점"
  }
}
```

`ko` 키를 중첩으로 넣은 이유: 향후 다른 언어(en, ja)를 추가할 수 있다.
하지만 현재는 ko만 구현한다.

## reason template 설계

추천 결과에 포함할 근거 문장을 어떻게 생성할지 결정해야 했다.

후보:
1. LLM으로 자연어 생성 → 매번 결과가 다르므로 deterministic하지 않음. 제외.
2. 고정 템플릿 → 기계적이지만 일관되고 테스트 가능. 채택.
3. 규칙 기반 가변 템플릿 → 조건에 따라 다른 문장 패턴. 추후 고려.

recommendation-service.ts에서 추천 결과를 반환할 때,
`reasonTrace`에 reason 문장을 포함시켰다:

```typescript
{
  toolId: "release-check-bot",
  score: 0.85,
  reason: "release-check-bot을 추천합니다. 릴리즈 호환성을 자동으로 검증합니다.",
  exposure: { tagline: "...", description: "..." }
}
```

## 대시보드 표시

React 대시보드(mcp-dashboard.tsx)에서 추천 결과를 카드 형태로 표시한다.
각 카드에 한국어 tagline, differentiator, reason이 표시된다.
exposure.ko가 없는 도구는 영문 description을 회색으로 표시한다.

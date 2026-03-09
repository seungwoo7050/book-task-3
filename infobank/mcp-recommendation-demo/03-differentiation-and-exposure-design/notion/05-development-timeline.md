# Differentiation & Exposure Design — 개발 타임라인

## 1단계: catalog.ts에 한국어 exposure 추가

```bash
cd shared/src
# catalog.ts의 각 도구에 exposure.ko 객체 추가
```

10+ 도구 각각에 대해:
- tagline (15자 이내)
- description (2-3문장)
- differentiator (선택)

작성 후 타입 체크:

```bash
cd shared
pnpm tsc --noEmit
```

## 2단계: contracts.ts에 exposure schema 추가

```bash
# contracts.ts에 exposureSchema 추가
```

```typescript
const exposureSchema = z.object({
  ko: z.object({
    tagline: z.string(),
    description: z.string(),
    differentiator: z.string().optional()
  })
}).optional();
```

catalogEntrySchema에 `exposure: exposureSchema`를 추가.

## 3단계: recommendation-service.ts에 reason template 구현

```bash
cd 08-capstone-submission/v0-initial-demo/node/src/services
# recommendation-service.ts에 reason 생성 로직 추가
```

추천 결과 반환 시 각 도구에 대해:
1. exposure.ko.differentiator가 있으면 reason에 포함
2. 없으면 영문 description 기반 기본 문장 생성

## 4단계: React 대시보드 카드 구현

```bash
cd 08-capstone-submission/v0-initial-demo/react/components
# mcp-dashboard.tsx에 추천 결과 카드 구현
```

카드 구성:
- 상단: 도구 이름 + 점수 배지
- 중단: tagline (한국어) 또는 description (영문, 회색)
- 하단: reason 문장

```bash
cd react
pnpm dev  # 개발 서버에서 시각적 확인
```

## 5단계: 테스트

```bash
cd node
pnpm test
```

테스트 내용:
- 추천 결과에 reason 필드가 포함되는지
- exposure.ko 누락 시 fallback이 동작하는지
- reason 문장이 도구 이름으로 시작하지 않는지

## 비고

- 한국어 tagline/description은 수동으로 작성해야 한다. 자동 번역은 사용하지 않았다.
- differentiator가 없는 도구는 reason이 짧아지지만 기능적으로 문제없다.
- 대시보드 스타일 조정은 CSS 수준이므로 별도 패키지 설치 없음.

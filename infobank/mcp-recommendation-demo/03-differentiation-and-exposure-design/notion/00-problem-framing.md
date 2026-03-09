# Differentiation & Exposure Design — 문제 정의

## 풀어야 하는 문제

추천 결과에 도구 이름만 표시하면 운영자가 **왜 이 도구가 추천되었는지** 알 수 없다.
특히 한국어 사용 환경에서는 영문 description만으로는 부족하다.

필요한 것:
1. **한국어 노출 문구**: tagline, description, differentiator
2. **추천 근거(reason)**: "이 도구가 선택된 이유"를 한국어로 설명
3. **차별화 포인트**: 비슷한 도구들 사이에서 이 도구가 왜 나은지

## 왜 번역이 아닌 "노출 설계"인가

단순 번역은 i18n 라이브러리로 충분하다.
하지만 여기서 필요한 건 **운영자 관점의 설명**이다.

예: postgres-schema-mapper의 영문 description이 "Analyzes PostgreSQL table schemas"일 때,
한국어 tagline은 "PostgreSQL 테이블 구조 분석기"가 아니라
"스키마 변경 전 영향 범위를 파악할 때 사용합니다"여야 한다.

이건 번역이 아니라 **노출 문구 설계**다.

## reason template

추천 결과에 포함되는 근거 문장의 템플릿:

```
"[도구 이름]을(를) 추천합니다. [differentiator]. [추천 이유]."
```

예: "release-check-bot을 추천합니다. 릴리즈 호환성을 자동으로 검증합니다. 사용자의 릴리즈 체크 요청과 가장 관련성이 높습니다."

## 제약

- 모든 도구에 한국어 노출 필드가 있는 건 아니다. 없는 경우 영문 description을 fallback으로 사용한다.
- reason template은 고정 패턴이다. LLM 기반 자연어 생성은 사용하지 않는다.

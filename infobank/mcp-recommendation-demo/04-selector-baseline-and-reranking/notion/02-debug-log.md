# Selector Baseline & Reranking — 디버그 기록

## baseline 가중치 튜닝 문제

### 상황

초기 가중치: category(0.5) + description(0.3) + name(0.2)
이렇게 하면 category가 일치하는 모든 도구가 상위에 오고,
그 중에서 순서가 거의 랜덤이었다.

### 해결

category 가중치를 낮추고 name 매칭을 높임:
category(0.4) + description(0.3) + name(0.3)

이유: 사용자 query에 도구 이름이 부분적으로 포함된 경우가 많다.
"postgres 스키마 확인" → postgres-schema-mapper가 name 매칭으로 정확히 잡힌다.

## reranker signal에서 사용 빈도가 압도적인 문제

### 상황

usage_count signal의 범위가 0~1000인데,
한 도구만 500회 사용됐고 나머지는 10회 미만이었다.
정규화 없이 곱하면 그 도구가 항상 1순위가 된다.

### 해결

min-max 정규화를 적용:

```typescript
const normalized = (value - min) / (max - min || 1);
```

정규화 후 모든 signal이 0~1 범위가 되어, 가중치가 의도대로 작동한다.

## compare에서 baseline과 reranker의 차이가 없는 케이스

### 상황

일부 eval case에서 baseline과 reranker의 추천 순위가 동일했다.
이건 signal이 해당 case에 영향을 미치지 않는다는 뜻이다.

### 해결

이건 버그가 아니라 정상이다.
signal 데이터(usage, feedback)가 없는 도구는 reranker가 baseline과 동일한 결과를 낸다.
compare 출력에 "no change" 표시를 추가하여 이 케이스를 시각화했다.

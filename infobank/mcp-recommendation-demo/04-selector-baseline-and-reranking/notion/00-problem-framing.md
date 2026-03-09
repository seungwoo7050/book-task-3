# Selector Baseline & Reranking — 문제 정의

## 풀어야 하는 문제

사용자가 "릴리즈 체크를 해야 해"라고 하면, catalog의 10+ 도구 중 관련 있는 것을 골라야 한다.
이게 **selector**의 역할이다.

## 왜 baseline과 reranker를 분리하는가

한 번에 완벽한 추천 알고리즘을 만들 수 없다.
그래서 두 단계로 나눈다:

1. **baseline selector**: 간단한 가중치 기반 매칭. v0에서 동작.
   - query 키워드와 도구의 category/description을 매칭
   - 정적 가중치로 점수 계산
   - 점수 상위 N개 반환

2. **reranker**: baseline 결과를 추가 신호(signal)로 재정렬. v1에서 추가.
   - usage frequency (사용 빈도)
   - feedback score (사용자 피드백 점수)
   - recency (최근 업데이트 여부)
   - compatibility (다른 도구와의 호환성)

이 분리의 장점:
- baseline만으로도 동작한다 (v0 데모 가능)
- reranker를 추가해도 baseline을 수정할 필요 없다
- eval로 baseline과 reranker의 차이를 수치화할 수 있다

## compare runner

baseline과 reranker의 결과를 같은 eval case로 실행하고 비교하는 도구다.
chat-qa-ops의 version compare와 같은 역할이다.

```bash
pnpm compare  # baseline vs reranker 결과 비교
```

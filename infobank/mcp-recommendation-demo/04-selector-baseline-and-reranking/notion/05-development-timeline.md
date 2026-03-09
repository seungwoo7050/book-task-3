# Selector Baseline & Reranking — 개발 타임라인

## 1단계: baseline selector (v0)

```bash
cd 08-capstone-submission/v0-initial-demo/node/src/services
# recommendation-service.ts에 recommend() 함수 구현
```

구현 순서:
1. catalog에서 전체 도구 목록 로드
2. query 토큰화 (공백 분리)
3. 도구별 점수 계산: category(0.4) + description(0.3) + name(0.3)
4. 점수 기준 내림차순 정렬
5. 상위 N개 + reasonTrace 반환

```bash
cd 08-capstone-submission/v0-initial-demo
pnpm test  # recommendation-service 테스트 포함
```

## 2단계: reranker (v1)

```bash
cd 08-capstone-submission/v1-ranking-hardening/node/src/services
touch rerank-service.ts
```

구현 순서:
1. baseline 추천 결과를 입력으로 받음
2. DB에서 usage_count, avg_feedback 조회
3. 각 signal을 min-max 정규화
4. finalScore 계산 (baseline * 0.6 + signals * 0.4)
5. 재정렬된 결과 반환

```bash
cd 08-capstone-submission/v1-ranking-hardening
pnpm test
```

## 3단계: compare service (v1)

```bash
touch 08-capstone-submission/v1-ranking-hardening/node/src/services/compare-service.ts
```

```bash
pnpm compare  # baseline vs reranker 비교 실행
```

compare 스크립트:
1. eval case를 순회
2. 각 case에 대해 baseline과 reranker 모두 실행
3. 결과를 나란히 비교
4. delta 계산 + JSON 출력

## 4단계: reranker 테스트

```bash
touch 08-capstone-submission/v1-ranking-hardening/node/tests/rerank-service.test.ts
```

테스트 내용:
- signal이 없을 때 baseline과 동일한 결과
- usage_count가 높은 도구가 상위로 올라가는지
- 정규화가 0~1 범위를 유지하는지

```bash
pnpm test
```

## 비고

- baseline selector는 v0에서 구현하고, reranker는 v1에서 추가한다.
- compare runner는 CLI 도구로, 대시보드와 별도로 동작한다.
- signal 데이터(usage, feedback)는 stage 05에서 DB에 기록된다.
  v1 단계에서는 seed 데이터로 시뮬레이션한다.

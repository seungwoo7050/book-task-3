# 비교 리포트

`v3`에서도 compare는 `v1/v2`와 같은 deterministic rerank signal을 사용한다. 차이는 compare를 UI에서 동기 호출하지 않고 job으로 enqueue한다는 점이다.

## 기대 해석

- baseline과 candidate의 품질 비교를 운영 콘솔에서 안정적으로 다시 돌릴 수 있어야 한다.
- compare 결과는 `release gate`의 입력 증빙으로 재사용된다.

## 검증

```bash
pnpm release:gate rc-release-check-bot-1-5-0
```

release gate 출력 안에서 compare uplift를 함께 본다.

## 마지막 검증 대상

- `baselineNdcg3 = 0.9759`
- `candidateNdcg3 = 0.9759`
- `uplift = 0.1146`

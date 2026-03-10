# 평가 증빙

`v3`는 추천 로직 자체를 바꾸지 않으므로, deterministic seed 기준의 offline eval 결과는 `v2`와 동일한 품질선을 유지해야 한다.

## 기대 기준

- `top3Recall >= 0.90`
- `explanationCompleteness = 1.00`
- `forbiddenHitRate = 0.00`

## 검증 명령

```bash
pnpm eval
```

## 마지막 검증 대상

- `top3Recall = 0.9583`
- `explanationCompleteness = 1.0000`
- `forbiddenHitRate = 0.0000`

> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Quality Rubric — 디버깅 기록: critical failure가 묻히는 문제

## Case: critical failure가 있어도 평균 점수가 높게 계산됨

### 증상

테스트를 처음 작성했을 때, "모든 축 100점 + critical=True"인 케이스를 돌렸더니 총점이 100점으로 나왔다.
compliance에서 PII를 노출한 답변인데 만점이 나오는 건 분명히 잘못된 결과였다.

### 원인

처음 구현에서는 `critical` 파라미터를 weighted average 계산 **후에** 확인하고 있었다.
즉, 먼저 가중 평균을 구해놓고 나중에 critical이면 grade를 덮어쓰는 구조였는데, grade만 바꾸고 total은 안 바뀌었다.

더 근본적으로는, weighted average **안에서** critical severity를 표현하려고 하면 다른 축 점수에 묻힐 수 있다는 구조적 문제가 있었다.

### 해결

`critical=True`일 때 **가중 평균을 아예 계산하지 않고** 즉시 `{"total": 0.0, "grade": "CRITICAL"}`을 반환하도록 함수 진입부에서 분기했다.

```python
if critical:
    return {"total": 0.0, "grade": "CRITICAL"}
```

### 검증

`test_critical_override_wins`가 모든 축 100점 입력에서도 `CRITICAL` grade와 `0.0` total을 기대한다.
이 테스트는 이후 어떤 weight 조정이 있어도 critical 분기가 유지되는지를 보장한다.

## 이 경험에서 배운 것

"예외 케이스를 나중에 처리하자"는 습관이 여기서 문제가 됐다.
critical failure처럼 **다른 모든 계산을 무효화하는 조건**은, 함수의 가장 앞에서 처리해야 한다.
나중에 처리하면 "일단 계산한 값"이 어딘가에 남아서 혼란을 만든다.

# Python 내부 문서 안내

`v1-regression-hardening`의 Python 문서는 `v0` 데모를 깨지 않으면서 regression, rubric, dependency health 규칙을 강화하는 데 필요한 내부 메모를 담는다. baseline을 고정하고 acceptance를 더 엄격하게 보는 이유를 여기서 설명한다.

## 이 버전에서 중요하게 볼 내용

- regression case를 golden set처럼 다루기 위한 evaluator contract
- storage에 score/evidence를 남길 때 필요한 최소 필드
- dependency health check가 fail-open이 아니라 fail-closed에 가까워지는 지점
- `v2` 제출 단계에서 그대로 증빙으로 가져갈 수 있는 검증 규칙

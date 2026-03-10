# Python 내부 문서 안내

`v0-initial-demo`의 Python 문서는 "최소 동작 데모를 어떻게 안정적으로 재현하는가"에 초점을 둔다. evaluator 흐름, fixture 적재 방식, 초기 storage 구조, 첫 smoke test 범위를 확인할 때 이 디렉터리를 본다.

## 이 버전에서 중요하게 볼 내용

- evaluator가 seeded telecom fixture를 어떻게 점수화하는지
- knowledge base와 case fixture를 어떤 순서로 읽어 오는지
- demo에서 필요한 최소 persistence가 어디까지인지
- 이후 `v1` regression hardening으로 넘길 때 그대로 유지할 규칙이 무엇인지

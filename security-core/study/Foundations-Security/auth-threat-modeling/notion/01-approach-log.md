# 접근 로그

- 실제 FastAPI auth 서버를 만들지 않고 scenario evaluator로 고정했습니다.
- secure baseline 0 finding을 가장 중요한 품질 기준으로 두었습니다.
- OAuth redirect control과 cookie/JWT control을 같은 시나리오 안에서 함께 비교할 수 있게 `flow`와 `controls`를 분리했습니다.


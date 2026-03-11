# 접근 로그

- 실제 API 서버 대신 endpoint case evaluator로 고정했습니다.
- secure baseline 0 finding을 먼저 두고, 각 취약점은 가능한 한 한 케이스에 한 control gap만 보이게 단순화했습니다.
- finding 구조에 `attack`, `mitigation`, `evidence`를 같이 넣어 triage 설명력을 높였습니다.


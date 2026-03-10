# ticklab 개념 노트

## 먼저 잡아야 할 질문

- authoritative server는 왜 입력을 즉시 반영하지 않고 tick 경계에서 적용하는가
- reconnect는 transport 문제가 아니라 session continuity 문제라는 말이 무엇을 뜻하는가
- snapshot은 로그가 아니라 어떤 복구 계약인가

## 코드 읽기 포인트

- [../cpp/src/MatchEngine.cpp](../cpp/src/MatchEngine.cpp): phase 전이와 tick 처리
- [../cpp/tests/test_ticklab.cpp](../cpp/tests/test_ticklab.cpp): deterministic 검증 포인트
- [../notion-archive/02-debug-log.md](../notion-archive/02-debug-log.md): 이전 디버깅 메모 백업

## 흔한 오해

- tick 기반 엔진은 네트워크를 붙인 뒤에만 검증할 수 있는 것이 아니다.
- reconnect는 토큰 발급만 있으면 끝나는 기능이 아니다.
- deterministic test는 데모용이 아니라 회귀 방지 도구다.

## 다음 단계로 이어지는 지점

이 lab에서 simulation을 고정했으니, 이제 네트워크를 붙여 실제 게임 서버로 확장한 [../arenaserv/README.md](../arenaserv/README.md)를 읽으면 흐름이 자연스럽다.

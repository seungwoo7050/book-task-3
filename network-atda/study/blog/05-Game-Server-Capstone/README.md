# 05. Game Server Capstone blog

소켓, 프로토콜, 상태 관리, persistence, 테스트 설계를 하나의 capstone으로 묶는 단계입니다.

## 이 트랙에서 무엇을 따라가면 되나

이 레이어는 프로젝트를 나열하는 데서 멈추지 않고, 왜 이 순서가 자연스러운지까지 같이 보여 주려고 한다. 구현형 프로젝트는 진입점과 테스트를 먼저 보고, 분석형 프로젝트는 trace 질문과 filter target을 먼저 잡는 방식으로 읽으면 흐름이 편하다.

## 권장 읽기 순서

1. [Tactical Arena Server](tactical-arena-server/README.md) - 제어 채널, authoritative simulation, persistence, 검증 하네스를 한 서버 안에서 어떻게 맞물리게 했는가?

## 공통으로 보는 근거

- 프로젝트 README와 `problem/README.md`
- `problem/Makefile`의 실행/검증 target
- 구현형은 `python/` 또는 `cpp/`, 분석형은 `analysis/src/`
- 테스트 파일과 `docs/concepts/`

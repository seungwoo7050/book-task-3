# 05. Game Server Capstone

소켓, 프로토콜, 상태 관리, persistence, 테스트 설계를 하나의 capstone으로 묶는 단계입니다.

## 프로젝트 카탈로그

| 프로젝트 | 문제 | 이 레포의 답 | 검증 | 상태 | 왜 이 단계에 있는가 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`Tactical Arena Server`](tactical-arena-server/README.md) | 이 저장소에서 누적한 네트워크 학습을 하나의 설명 가능한 서버로 묶기 위해 직접 설계한 신규 capstone 프로젝트 | `cpp/src/` | `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test` | `verified` | 앞선 트랙에서 배운 TCP/UDP, 신뢰 전송, 진단 도구, deterministic test 패턴을 하나의 서버 설계로 통합해 설명하는 단계가 필요했기 때문에 추가한 capstone입니다. |

## 공통 읽기 순서

1. 프로젝트 README에서 문제, 답, 검증 명령을 먼저 확인합니다.
2. `problem/README.md`에서 제공 자료와 성공 기준을 확인합니다.
3. 구현형 과제는 `python/README.md` 또는 `cpp/README.md`, 분석형 과제는 `analysis/README.md`로 내려갑니다.
4. `docs/README.md`는 개념을 다시 확인할 때만 참고하고, `notion/README.md`는 보조 기록으로만 읽습니다.

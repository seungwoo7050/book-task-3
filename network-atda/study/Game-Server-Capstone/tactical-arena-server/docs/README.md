# 개념 문서 안내

    이 디렉터리는 `Tactical Arena Server`를 공부하면서 반복해서 다시 볼 만한 개념 문서만 남겨 둔 곳입니다.

    ## 읽는 순서

    1. [`architecture.md`](concepts/architecture.md)
2. [`load-testing.md`](concepts/load-testing.md)
3. [`persistence.md`](concepts/persistence.md)
4. [`protocol.md`](concepts/protocol.md)
5. [`simulation.md`](concepts/simulation.md)
6. [`presentation/README.md`](presentation/README.md)
7. [`references/README.md`](references/README.md)

    ## 이 폴더가 답하려는 질문

    - line-based TCP control protocol과 binary UDP packet을 함께 설계하는 방법
- room 단위 상태를 strand로 직렬화하는 authoritative simulation 구조
- reconnect window, forfeit, fixed tick, respawn 같은 게임 서버 상태 전이
- SQLite persistence를 deterministic test와 연결하는 방법

    ## 사용 원칙

    - 프로젝트 README와 중복되는 설명은 줄이고, 오래 남길 개념과 판단 근거를 우선합니다.
    - 이전 형식 노트는 `notion-archive/`에, 현재 읽을 작업 기록은 `notion/`에 둡니다.
    - 프로토콜 field 이름 같은 원문 용어는 필요할 때 그대로 유지합니다.

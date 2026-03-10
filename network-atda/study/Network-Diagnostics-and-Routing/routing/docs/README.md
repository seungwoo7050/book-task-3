# 개념 문서 안내

    이 디렉터리는 `Distance-Vector Routing`를 공부하면서 반복해서 다시 볼 만한 개념 문서만 남겨 둔 곳입니다.

    ## 읽는 순서

    1. [`bellman-ford.md`](concepts/bellman-ford.md)
2. [`count-to-infinity.md`](concepts/count-to-infinity.md)
3. [`distance-vector.md`](concepts/distance-vector.md)
4. [`dv-vs-ls.md`](concepts/dv-vs-ls.md)
5. [`references/README.md`](references/README.md)

    ## 이 폴더가 답하려는 질문

    - Bellman-Ford update 식
- 2-phase synchronous simulation
- 수렴 판정
- next hop과 cost를 함께 관리하는 방법

    ## 사용 원칙

    - 프로젝트 README와 중복되는 설명은 줄이고, 오래 남길 개념과 판단 근거를 우선합니다.
    - 이전 형식 노트는 `notion-archive/`에, 현재 읽을 작업 기록은 `notion/`에 둡니다.
    - 프로토콜 field 이름 같은 원문 용어는 필요할 때 그대로 유지합니다.

# 개념 문서 안내

    이 디렉터리는 `RDT Protocol`를 공부하면서 반복해서 다시 볼 만한 개념 문서만 남겨 둔 곳입니다.

    ## 읽는 순서

    1. [`gbn-vs-sr.md`](concepts/gbn-vs-sr.md)
2. [`go-back-n.md`](concepts/go-back-n.md)
3. [`rdt-principles.md`](concepts/rdt-principles.md)
4. [`rdt3.md`](concepts/rdt3.md)
5. [`reproducibility.md`](concepts/reproducibility.md)
6. [`references/README.md`](references/README.md)

    ## 이 폴더가 답하려는 질문

    - alternating bit와 cumulative ACK의 차이
- timeout 기반 재전송
- sliding window의 기본 구조
- 실제 네트워크 대신 시뮬레이션 채널에서 프로토콜을 검증하는 법

    ## 사용 원칙

    - 프로젝트 README와 중복되는 설명은 줄이고, 오래 남길 개념과 판단 근거를 우선합니다.
    - 이전 형식 노트는 `notion-archive/`에, 현재 읽을 작업 기록은 `notion/`에 둡니다.
    - 프로토콜 field 이름 같은 원문 용어는 필요할 때 그대로 유지합니다.

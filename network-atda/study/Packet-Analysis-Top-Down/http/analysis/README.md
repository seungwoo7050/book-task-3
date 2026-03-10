# 공개 답안 안내

    이 디렉터리는 `HTTP Packet Analysis`의 공개 답안과 근거 문서를 담습니다. packet/frame 번호, field 값, trace 범위를 직접 인용하는 문서를 우선 배치합니다.

    ## 어디서부터 읽으면 좋은가

    1. `analysis/src/http-analysis.md` - 질문별 답안과 근거를 확인합니다.

    ## 기준 명령

    - 검증: `make -C study/Packet-Analysis-Top-Down/http/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

    ## 현재 범위

    기본 GET, conditional GET, 긴 문서 전송, embedded object 요청을 패킷 수준에서 추적하는 랩입니다.

    ## 남은 약점

    - `HTTP/2` 이상은 다루지 않습니다.
- 브라우저별 헤더 차이는 관찰 범위 밖입니다.
- 실시간 캡처 대신 고정 trace에 기반합니다.

# 공개 답안 안내

    이 디렉터리는 `TLS Packet Analysis`의 공개 답안과 근거 문서를 담습니다. packet/frame 번호, field 값, trace 범위를 직접 인용하는 문서를 우선 배치합니다.

    ## 어디서부터 읽으면 좋은가

    1. `analysis/src/tls-ssl-analysis.md` - 질문별 답안과 근거를 확인합니다.

    ## 기준 명령

    - 검증: `make -C study/Packet-Analysis-Top-Down/tls-ssl/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

    ## 현재 범위

    TLS handshake, certificate, cipher suite, 버전 차이를 record/message 수준에서 읽는 보안 랩이다.

    ## 남은 약점

    - 현재 한계는 프로젝트 README를 기준으로 정리합니다.

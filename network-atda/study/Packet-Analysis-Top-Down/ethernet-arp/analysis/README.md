# 공개 답안 안내

    이 디렉터리는 `Ethernet and ARP Packet Analysis`의 공개 답안과 근거 문서를 담습니다. packet/frame 번호, field 값, trace 범위를 직접 인용하는 문서를 우선 배치합니다.

    ## 어디서부터 읽으면 좋은가

    1. `analysis/src/ethernet-arp-analysis.md` - 질문별 답안과 근거를 확인합니다.

    ## 기준 명령

    - 검증: `make -C study/Packet-Analysis-Top-Down/ethernet-arp/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

    ## 현재 범위

    링크 계층 프레임과 IP-MAC 주소 해석 과정을 ARP request/reply 쌍으로 읽는 랩이다.

    ## 남은 약점

    - 현재 한계는 프로젝트 README를 기준으로 정리합니다.

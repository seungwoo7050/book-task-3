# 802.11 Wireless Packet Analysis 구조 메모

## 문서 구성 의도

- `00-series-map.md`: 이 lab를 "station join ladder"라는 질문으로 먼저 묶는다.
- `10-development-timeline.md`: beacon -> probe -> auth -> association -> data -> ACK 순서를 chronology로 복원한다.
- `01-evidence-ledger.md`: answer markdown와 `tshark` 필터 출력을 짧게 묶는다.

## 이번 재작성에서 강조한 점

- Wi-Fi를 Ethernet 변형처럼 쓰지 않고 management frame 중심의 다른 링크 계층으로 설명한다.
- compact synthetic trace라는 점을 한계이자 장점으로 동시에 다룬다.
- security evolution, RF behavior, retry logic은 현재 범위 바깥으로 남긴다.

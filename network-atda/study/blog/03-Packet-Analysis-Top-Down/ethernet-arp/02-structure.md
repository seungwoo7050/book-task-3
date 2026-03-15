# Ethernet and ARP Packet Analysis 구조 메모

## 문서 구성 의도

- `00-series-map.md`: 이 lab를 "3 frame로 보는 주소 해석"이라는 질문으로 먼저 묶는다.
- `10-development-timeline.md`: request, reply, first IPv4 frame의 세 장면을 chronology로 복원한다.
- `01-evidence-ledger.md`: `tshark` 필터와 answer markdown를 짧게 고정한다.

## 이번 재작성에서 강조한 점

- ARP를 개념 문서처럼 길게 설명하지 않고, 현재 trace가 보여 주는 3-step handoff에 집중한다.
- HTTP GET offset, spoofing, gratuitous ARP는 trace 바깥 질문으로 분리한다.
- Ethernet header와 ARP payload의 주소 필드를 한 번에 읽도록 연결해 준다.

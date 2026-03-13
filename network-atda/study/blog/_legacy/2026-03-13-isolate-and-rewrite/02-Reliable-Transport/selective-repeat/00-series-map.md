# Selective Repeat 시리즈 지도

## 이 프로젝트를 한 줄로

GBN에서 "window 전체 재전송"이라는 비효율을 느낀 뒤, "필요한 packet만 다시 보내는" 방법을 구현한다. 대신 sender는 packet별 timer를, receiver는 out-of-order buffer를 가져야 하는데, 이 추가 복잡도가 실제로 GBN과 어떻게 다른 코드를 만드는지 직접 봤다.

## 문제 구조
- 제공물: `problem/code/channel.py`, `problem/code/packet.py`, skeleton
- 답안: `python/src/selective_repeat.py`
- 검증: `make -C study/02-Reliable-Transport/selective-repeat/problem test`

## 이 시리즈에서 따라갈 질문
1. receiver가 out-of-order packet을 buffer에 넣는 순간 GBN과 뭐가 달라지는가
2. per-packet timer는 단일 timer보다 뭐가 더 복잡하고 뭐가 더 정확한가
3. `send_base` slide가 "ACK 하나"가 아니라 "연속 ACK"에 의존하는 이유는 무엇인가

## 글 목록
| 번호 | 파일 | 범위 |
| :--- | :--- | :--- |
| `10` | [`10-development-timeline.md`](10-development-timeline.md) | GBN과의 차이 인식부터 검증까지 |

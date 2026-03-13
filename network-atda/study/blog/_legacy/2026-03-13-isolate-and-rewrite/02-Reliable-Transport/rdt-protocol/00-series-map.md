# RDT Protocol 시리즈 지도

## 이 프로젝트를 한 줄로

불신 채널 위에서 "packet을 하나씩 확실하게 보낸다"는 게 실제로 무슨 코드인지를 rdt3.0(stop-and-wait)과 GBN(Go-Back-N)으로 직접 구현한다. UDP Pinger에서 "timeout이 없으면 손실을 모른다"를 배웠다면, 여기서는 "timeout이 있어도 어떤 packet을 다시 보내야 하느냐"가 핵심 문제가 된다.

## 문제 구조
- 제공물: `problem/code/channel.py`, `problem/code/packet.py`, skeleton 파일들
- 답안: `python/src/rdt3.py` (stop-and-wait), `python/src/gbn.py` (Go-Back-N)
- 검증: `make -C study/02-Reliable-Transport/rdt-protocol/problem test`

## 이 시리즈에서 따라갈 질문
1. alternating bit라는 간단한 아이디어가 sender 상태 기계로 바뀔 때 무엇이 복잡해지는가
2. GBN이 timeout 시 window 전체를 다시 보내는 게 왜 "비효율"이면서도 "교육적"인가
3. `channel.py`와 `packet.py`라는 제공 도구가 구현의 경계를 어떻게 정하는가

## 글 목록
| 번호 | 파일 | 범위 |
| :--- | :--- | :--- |
| `10` | [`10-development-timeline.md`](10-development-timeline.md) | rdt3.0 구현부터 GBN window 검증까지 |

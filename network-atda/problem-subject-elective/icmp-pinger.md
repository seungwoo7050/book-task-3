# icmp-pinger 문제지

## 왜 중요한가

이 문서는 ICMP Pinger를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 구현 세부와 공개 구현 경로는 상위 프로젝트 README가 연결하는 경로를 따라가면 됩니다.

## 목표

시작 위치의 구현을 완성해 패킷 생성: ICMP Echo Request 형식이 올바릅니다, 체크섬: 인터넷 체크섬이 정확합니다, 응답 파싱: Echo Reply를 올바르게 추출하고 검증합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem/code/icmp_pinger_skeleton.py`
- `../study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py`
- `../study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem/script/test_icmp.sh`
- `../study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/tests/test_icmp_pinger.py`
- `../study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem/Makefile`

## starter code / 입력 계약

- ../study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem/code/icmp_pinger_skeleton.py에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- 패킷 생성: ICMP Echo Request 형식이 올바릅니다.
- 체크섬: 인터넷 체크섬이 정확합니다.
- 응답 파싱: Echo Reply를 올바르게 추출하고 검증합니다.
- RTT 측정: RTT를 올바르게 계산합니다.
- 통계: 최소/평균/최대 RTT와 손실률이 정확합니다.
- 코드 품질: 구조가 명확하고 문서화가 된 코드입니다.

## 제외 범위

- `../study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem/code/icmp_pinger_skeleton.py` starter skeleton을 정답 구현으로 착각하지 않는다.
- `../study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem/script/test_icmp.sh` fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- `../study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem/code/icmp_pinger_skeleton.py`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `internet_checksum`와 `build_echo_request`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestInternetChecksum`와 `TestPacketBuilding`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem/script/test_icmp.sh` fixture/trace 기준으로 결과를 대조했다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/network-atda/study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test
```

- `icmp-pinger`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`icmp-pinger_answer.md`](icmp-pinger_answer.md)에서 확인한다.

# 04 지식 인덱스

## 핵심 용어
- **TTL**: 패킷이 몇 hop까지 갈 수 있는지 제한하는 IPv4 헤더 필드다.
- **Time Exceeded**: TTL이 0이 되었을 때 라우터가 돌려주는 ICMP 오류다.
- **Port Unreachable**: 도착지에서 목적지 포트가 열려 있지 않음을 알리는 ICMP 오류이며, UDP traceroute의 종료 신호로 자주 사용된다.
- **probe correlation**: 응답을 원래 보낸 probe와 정확히 연결하는 과정이다.

## 다시 볼 파일
- [`../python/src/traceroute.py`](../python/src/traceroute.py): probe 포트 생성, ICMP 파싱, hop 출력이 모두 모여 있다.
- [`../python/tests/test_traceroute.py`](../python/tests/test_traceroute.py): 포트 규칙, 중첩 파싱, 종료 조건을 어떤 방식으로 검증하는지 보여준다.
- [`../docs/concepts/ipv4-header.md`](../docs/concepts/ipv4-header.md): TTL과 헤더 길이 필드를 다시 확인할 때 기준이 된다.
- [`../docs/concepts/icmp-protocol.md`](../docs/concepts/icmp-protocol.md): Traceroute에서 실제로 어떤 ICMP 오류를 소비하는지 정리해 둔 문서다.

## 자주 쓰는 확인 명령
- `make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test`
- `sudo python3 study/04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py 8.8.8.8`

## 참고 자료
- [`../docs/references/README.md`](../docs/references/README.md): 공개 문서를 정리할 때 다시 확인한 근거 모음

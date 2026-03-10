# 04 지식 인덱스

## 핵심 용어
- **Echo Request/Reply**: ICMP `type=8` 요청과 `type=0` 응답을 뜻한다.
- **raw socket**: IP/ICMP 헤더를 애플리케이션이 직접 다룰 수 있게 해 주는 저수준 소켓이다.
- **`IHL`**: IPv4 헤더 길이를 32비트 word 단위로 나타내는 필드다.
- **Internet checksum**: RFC 1071에서 설명하는 16비트 one’s complement checksum이다.

## 다시 볼 파일
- [`../python/src/icmp_pinger.py`](../python/src/icmp_pinger.py): checksum, 패킷 생성, 송수신 루프가 한 파일에 모여 있다.
- [`../python/tests/test_icmp_pinger.py`](../python/tests/test_icmp_pinger.py): 순수 함수 테스트와 출력 조건을 어떤 수준으로 보는지 보여준다.
- [`../docs/concepts/checksum.md`](../docs/concepts/checksum.md): checksum 알고리즘을 수식과 예제로 다시 확인할 때 본다.
- [`../docs/concepts/raw-sockets.md`](../docs/concepts/raw-sockets.md): 권한과 운영체제 제약을 정리해 둔 문서다.

## 자주 쓰는 확인 명령
- `make -C study/Network-Diagnostics-and-Routing/icmp-pinger/problem test`
- `sudo python3 study/Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py 8.8.8.8 -c 4`

## 참고 자료
- [`../docs/references/README.md`](../docs/references/README.md): 공개 문서를 정리할 때 다시 확인한 근거 모음

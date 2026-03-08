# Traceroute 문제 사양

## 개요

TTL 값을 1씩 늘려 가며 UDP probe를 보내고, 돌아오는 ICMP 응답을 읽어 원격 호스트까지의 경로를 추적하는 작은 **traceroute** 도구를 만든다. TTL이 0이 된 라우터는 보통 **ICMP Time Exceeded**를 돌려주고, 목적지에 도달하면 대개 **ICMP Port Unreachable**로 trace가 끝난다.

## 핵심 개념

- **TTL / Hop Limit**: 라우터를 한 hop씩 드러내도록 강제한다.
- **ICMP Time Exceeded**: probe가 중간 경로에서 만료된 지점을 알려 준다.
- **ICMP Port Unreachable**: probe가 목적지에 도착했음을 알려 준다.
- **Raw Sockets**: 커널이 수신한 ICMP control traffic을 직접 읽는다.

## 학습 목표

1. IP 이론의 TTL 동작을 실제 진단 도구 구현으로 연결한다.
2. ICMP 응답을 파싱해 어떤 UDP probe에 대한 응답인지 매칭한다.
3. 중간 hop의 ICMP 메시지와 목적지 응답을 구분한다.
4. live probing과 unit-level parser 검증을 분리해 재현성을 유지한다.

## 과제 규칙

- 언어: Python 3 표준 라이브러리만 사용
- live run: `make run-client HOST=8.8.8.8`는 대부분의 시스템에서 elevated privileges가 필요하다.
- canonical test: `make test`는 raw socket을 열지 않고 packet parsing과 hop formatting만 검증한다.
- 상태: unit check가 통과해도 live network validation은 별도 후속 과제로 남긴다.

# Traceroute 개발 타임라인

현재 구현을 다시 읽으면 이 lab의 흐름은 TTL을 1씩 올리는 단순 loop가 아니다. 실제 전환은 probe identity를 port에 심고, ICMP reply에서 그 identity를 다시 복원해, hop line으로 축약하는 데 있다. 전환점은 네 번이다.

## 1. 먼저 TTL별 probe를 port space에 안정적으로 매핑한다

`build_probe_port()`는 base port `33434`에서 출발해 `ttl`과 `probe_index`를 합쳐 probe별 UDP destination port를 만든다. 이 단계 덕분에 simultaneous probes가 있어도 각 reply를 어떤 hop attempt와 연결해야 하는지 기준이 생긴다.

즉 traceroute의 첫 핵심은 TTL이 아니라 probe identity design이다.

## 2. raw ICMP reply는 outer header만 봐서는 충분하지 않다

`parse_icmp_response()`는 outer ICMP type/code를 읽은 다음, 그 안에 포함된 original IP/UDP header까지 들어가 embedded dest port를 복원한다. 바로 이 때문에 traceroute는 "ICMP를 받았다"만으로 끝나지 않고, "이 ICMP가 어느 probe의 결과인가"까지 판정할 수 있다.

이 지점이 ping과 traceroute를 가르는 실제 구현 차이다.

## 3. `trace_route()`는 send/receive channel을 분리한 뒤 observation을 hop line으로 압축한다

실제 trace loop는 raw ICMP receive socket과 UDP send socket을 분리한다. TTL마다 probe를 보내고, matching ICMP reply가 오면 `ProbeObservation`에 responder IP, RTT, type/code를 채운다. 그 다음 `format_hop_line()`이 `*` 또는 `12.345 ms  10.0.0.1` 같은 human-readable line으로 바꾼다.

테스트가 formatting logic을 별도로 고정하는 이유도 այստեղ 있다. traceroute는 network logic과 terminal presentation이 모두 사용자 경험의 일부이기 때문이다.

## 4. 마지막 종료 조건은 destination IP와 `Port Unreachable` 조합으로 닫힌다

현재 구현은 destination IP에서 `ICMP type 3 code 3`이 관찰되면 trace를 멈춘다. synthetic integration test는 바로 이 규칙으로 `10.0.0.1 -> 10.0.1.1 -> 203.0.113.9` 세 hop 뒤 종료한다. 반대로 live `example.com` rerun은 현재 세션에서 5초 내 완료되지 않았다.

그래서 이 lab의 마지막 전환점은 "probe를 많이 보낸다"가 아니라, "어떤 reply를 destination 도달로 인정할 것인가"를 명시적인 rule로 고정하는 데 있다.

## 지금 남는 한계

현재 구현은 IPv4 UDP traceroute 한 종류에 집중한다. reverse DNS, ICMP echo variant, IPv6, ECMP path instability는 범위 밖이다. 그래도 probe identity, reply correlation, hop formatting, termination rule이라는 핵심 축은 충분히 선명하다.

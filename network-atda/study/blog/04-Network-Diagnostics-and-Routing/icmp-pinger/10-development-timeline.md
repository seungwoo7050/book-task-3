# ICMP Pinger 개발 타임라인

현재 구현을 다시 읽으면 이 lab의 흐름은 socket을 열고 패킷을 보내는 단일 이벤트가 아니다. 오히려 binary packet contract를 직접 만들고, 그 위에 timeout과 통계를 얹는 순서로 층이 쌓인다. 전환점은 네 번이다.

## 1. 먼저 checksum을 독립 함수로 분리해 packet correctness의 바닥을 만든다

`internet_checksum()`은 odd-length padding, 16-bit word sum, carry fold, one's complement를 모두 직접 처리한다. 이 함수가 분리돼 있기 때문에 나머지 구현은 "header를 어떻게 만들 것인가"와 "reply를 어떻게 읽을 것인가"에 집중할 수 있다. tests도 바로 이 함수의 invariants를 가장 먼저 고정한다.

## 2. Echo Request는 header와 payload를 두 번에 나눠 완성한다

`build_echo_request()`는 checksum 0인 임시 header를 먼저 만들고, 현재 `time.time()` 값을 double 8 bytes로 payload에 넣은 다음, header+payload 전체 checksum을 계산해 최종 header를 다시 pack한다. 즉 현재 payload는 단순 filler가 아니라 RTT 계산에 바로 쓰이는 timestamp carrier다.

이 단계 때문에 이 lab는 protocol packet builder와 latency tool을 동시에 겸하게 된다.

## 3. Reply parse는 ICMP보다 먼저 outer IP header를 해석해야 한다

`parse_echo_reply()`의 핵심은 `IHL`이다. raw socket으로 받은 bytes에는 outer IPv4 header가 먼저 붙기 때문에, implementation은 `data[0] & 0x0F`로 header length를 읽고 ICMP section offset을 계산한다. 그런 다음 type/id/sequence와 timestamp payload를 꺼낸다.

즉 이 lab는 ICMP 과제이지만, 실제 parse에서는 IP header awareness가 먼저 필요하다는 점이 중요하다.

## 4. 마지막으로 deterministic test와 live harness의 역할을 분리해 구현 경계를 고정한다

2026-03-14 재실행 기준 정식 테스트는 `11 passed`였다. fake raw socket과 fake clock을 쓰는 tests는 성공 reply, timeout, loss percentage, RTT summary까지 전부 deterministic하게 확인한다. `problem/script/test_icmp.sh`는 반대로 root와 외부 네트워크를 전제한 live harness다. 이번 세션에서 직접 시도한 `example.com` probe는 5초 내 완료되지 않았다.

그래서 이 lab의 마지막 전환점은 "실제 네트워크가 진실"이라는 기대에서, "환경 의존적인 live run과 재현성 높은 deterministic test를 분리해야 한다"는 쪽으로 이동하는 데 있다.

## 지금 남는 한계

현재 구현은 IPv4 ICMP Echo에 집중한다. duplicate reply, IPv6, richer statistics, live environment robustness는 범위 밖이다. 그래도 checksum, packet build, reply parse, RTT/loss summary라는 핵심 축은 현재 코드와 test로 충분히 고정돼 있다.

# 02 디버그 로그

이 파일은 과거의 날짜 순서를 복원하려는 문서가 아니다. 백업 노트와 현재 테스트를 함께 보고, 지금도 재현하거나 설명할 수 있는 문제만 남긴다.

## 사례 1. ICMP 응답이 어느 probe에 대한 것인지 구분되지 않음
- 증상: 동일 TTL에서 여러 probe를 보내면 응답을 올바른 칸에 배치하기 어려웠다.
- 원인: 겉 ICMP 헤더만 보면 내부에 어떤 UDP 패킷이 실려 있었는지 알 수 없다.
- 수정: ICMP payload 안의 원래 IP/UDP 헤더까지 파싱해 embedded destination port로 probe를 식별했다.
- 확인: `test_parse_icmp_response_extracts_embedded_udp_port`로 검증했다.

## 사례 2. 도착지에 닿았는데도 trace가 계속 진행됨
- 증상: 마지막 hop 이후에도 TTL이 계속 증가하며 불필요한 probe를 더 보냈다.
- 원인: 도착 판정을 ICMP Time Exceeded만 보고 처리하면 목적지의 `Port Unreachable`을 종료 신호로 쓰지 못한다.
- 수정: ICMP type `3`, code `3`을 목적지 도착으로 인식해 루프를 종료했다.
- 확인: `test_trace_route_returns_hops_until_destination`와 수동 실행으로 확인했다.

## 사례 3. timeout이 섞인 hop 출력이 읽기 어렵거나 형식이 깨짐
- 증상: 일부 probe가 응답하지 않을 때 줄 단위 출력이 들쭉날쭉했다.
- 원인: 성공 주소와 timeout 표시를 같은 포맷 규칙으로 다루지 않았다.
- 수정: `*`를 포함한 hop formatter를 따로 만들어 출력 형식을 고정했다.
- 확인: `test_format_hop_line_handles_mixed_results`로 검증했다.

# 참고 자료

IP/ICMP 패킷 분석 문서를 정리하면서 실제로 확인한 자료다. fragmentation, traceroute 관련 trace를 IPv4/ICMP 개념과 맞춰 설명하기 위해 사용했다.

## 저장소 내부 기준
### [문제 가이드](../../problem/README.md)
- 확인일: `2026-03-10`
- 왜 봤나: 분석 질문과 trace 범위를 다시 확인하려고 읽었다.
- 무엇을 확인했나: fragmentation과 traceroute 관련 패킷을 어떤 질문 단위로 읽어야 하는지 정리할 수 있었다.
- 반영 결과: README와 분석 답안 구조를 더 명확히 만들었다.

### [캡처 데이터 안내](../../problem/data/README.md)
- 확인일: `2026-03-10`
- 왜 봤나: 각 pcap 파일의 역할을 다시 확인했다.
- 무엇을 확인했나: fragmentation trace와 traceroute trace를 서로 다른 학습 포인트로 나눌 수 있었다.
- 반영 결과: 학생 안내 문장을 더 친절하게 만들었다.

### [분석 답안](../../analysis/src/ip-icmp-analysis.md)
- 확인일: `2026-03-10`
- 왜 봤나: 현재 해설이 어떤 패킷을 근거로 쓰였는지 확인했다.
- 무엇을 확인했나: 질문별 패킷 근거와 설명을 다시 맞출 수 있었다.
- 반영 결과: 문서 일관성이 높아졌다.

### [IPv4 헤더 문서](../concepts/ipv4-header.md)
- 확인일: `2026-03-10`
- 왜 봤나: fragment offset, TTL, protocol 필드를 다시 정리하려고 읽었다.
- 무엇을 확인했나: 패킷 해석과 개념 설명을 더 정확히 연결할 수 있었다.
- 반영 결과: 지식 설명의 품질이 올라갔다.

### [ICMP 개념 문서](../concepts/icmp-protocol.md)
- 확인일: `2026-03-10`
- 왜 봤나: echo, error message, traceroute 관련 ICMP 필드를 정리하려고 읽었다.
- 무엇을 확인했나: IP trace와 ICMP trace를 함께 설명하는 데 도움이 됐다.
- 반영 결과: 문서가 더 학습 친화적으로 바뀌었다.

### [검증 스크립트](../../problem/script/verify_answers.sh)
- 확인일: `2026-03-10`
- 왜 봤나: 현재 자동 검증 범위를 확인하려고 읽었다.
- 무엇을 확인했나: 답안과 문서가 어떤 최소 기준을 충족하는지 설명할 수 있었다.
- 반영 결과: `verified` 표현의 근거가 됐다.

## 외부 기준
### Computer Networking: A Top-Down Approach, network layer Wireshark lab
- 확인일: `2026-03-10`
- 왜 봤나: IP와 ICMP 실습이 무엇을 가르치려는지 다시 확인하려고 참고했다.
- 무엇을 확인했나: 패킷 해석을 네트워크 계층 개념과 연결하는 구조를 잡을 수 있었다.
- 반영 결과: 답안집 느낌을 줄이고 학습 기록 느낌을 살리는 데 도움이 됐다.

### [RFC 791 / RFC 792: IPv4 and ICMP](https://www.rfc-editor.org/rfc/rfc791)
- 확인일: `2026-03-10`
- 왜 봤나: IPv4 헤더와 ICMP 메시지 필드 정의를 다시 확인하려고 봤다.
- 무엇을 확인했나: fragmentation과 ICMP error 설명을 표준과 맞출 수 있었다.
- 반영 결과: 개념 문서 정확도가 높아졌다.

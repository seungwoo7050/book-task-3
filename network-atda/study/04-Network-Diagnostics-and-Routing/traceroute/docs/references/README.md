# 참고 자료

Traceroute 설명을 정리하면서 실제로 다시 본 자료다. TTL, ICMP 오류, probe 매칭을 현재 코드와 맞춰 기록하기 위해 사용했다.

## 저장소 내부 기준
### [문제 명세](../../problem/README.md)
- 확인일: `2026-03-10`
- 왜 봤나: hop 출력과 probe 동작 범위를 다시 확인하려고 읽었다.
- 무엇을 확인했나: 이 프로젝트가 path discovery 학습용 traceroute 구현이라는 점을 분명히 할 수 있었다.
- 반영 결과: README와 노트에서 기능 범위를 과장하지 않게 됐다.

### [현재 구현](../../python/src/traceroute.py)
- 확인일: `2026-03-10`
- 왜 봤나: probe 포트 생성, 응답 파싱, 종료 조건이 문서 설명과 맞는지 확인했다.
- 무엇을 확인했나: nested IP/UDP parsing과 type 3 code 3 종료 규칙을 코드 기준으로 정리할 수 있었다.
- 반영 결과: 노트의 설계 기록과 디버그 로그를 실제 소스에 맞춰 재작성했다.

### [자동 테스트](../../python/tests/test_traceroute.py)
- 확인일: `2026-03-10`
- 왜 봤나: 현재 저장소에서 어떤 부분이 공식 검증되는지 확인하려고 읽었다.
- 무엇을 확인했나: 포트 규칙, 응답 파싱, 출력 포맷, 종료 조건이 핵심 테스트 범위임을 알 수 있었다.
- 반영 결과: `verified` 설명이 구체적 근거를 갖게 됐다.

### [IPv4 헤더 문서](../concepts/ipv4-header.md)
- 확인일: `2026-03-10`
- 왜 봤나: TTL과 header parsing 설명을 더 정확히 쓰려고 읽었다.
- 무엇을 확인했나: nested header parsing 설명을 학생이 따라가기 쉬운 단위로 쪼갤 수 있었다.
- 반영 결과: 지식 인덱스의 용어 정의를 더 명확히 만들었다.

### [ICMP 문서](../concepts/icmp-protocol.md)
- 확인일: `2026-03-10`
- 왜 봤나: Time Exceeded와 Destination Unreachable 의미를 다시 확인했다.
- 무엇을 확인했나: 도착지 판정 설명을 표준 개념과 연결할 수 있었다.
- 반영 결과: 디버그 로그의 종료 조건 설명에 근거가 됐다.

### [raw socket 문서](../concepts/raw-sockets.md)
- 확인일: `2026-03-10`
- 왜 봤나: 권한과 실행 환경 차이를 다시 정리하려고 읽었다.
- 무엇을 확인했나: manual run 가이드가 더 현실적인 문서가 됐다.
- 반영 결과: 학습용 실습 안내를 더 친절하게 만들었다.

## 외부 기준
### [RFC 791: Internet Protocol](https://www.rfc-editor.org/rfc/rfc791)
- 확인일: `2026-03-10`
- 왜 봤나: TTL과 IPv4 헤더 필드 의미를 다시 확인하려고 봤다.
- 무엇을 확인했나: 왜 hop마다 TTL을 하나씩 늘리는지 표준 정의와 연결할 수 있었다.
- 반영 결과: Traceroute 개념 설명이 더 정확해졌다.

### [RFC 792: Internet Control Message Protocol](https://www.rfc-editor.org/rfc/rfc792)
- 확인일: `2026-03-10`
- 왜 봤나: 라우터와 목적지가 어떤 ICMP 오류를 돌려주는지 확인하려고 참고했다.
- 무엇을 확인했나: Time Exceeded, Port Unreachable 의미를 분명히 설명할 수 있었다.
- 반영 결과: 도착지 판정과 hop 출력 설명의 근거가 됐다.

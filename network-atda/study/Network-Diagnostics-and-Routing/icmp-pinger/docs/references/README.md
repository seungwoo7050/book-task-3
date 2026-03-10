# 참고 자료

ICMP Pinger를 정리하며 실제로 다시 본 자료다. checksum, raw socket, 응답 파싱을 현재 구현과 맞춰 설명하기 위해 사용했다.

## 저장소 내부 기준
### [문제 명세](../../problem/README.md)
- 확인일: `2026-03-10`
- 왜 봤나: raw socket 기반 ping 과제 범위를 다시 확인하려고 읽었다.
- 무엇을 확인했나: 이 프로젝트가 운영체제 `ping` 복제가 아니라 ICMP Echo 학습용 구현이라는 점을 분명히 할 수 있었다.
- 반영 결과: README와 노트에서 범위를 과장하지 않게 됐다.

### [현재 구현](../../python/src/icmp_pinger.py)
- 확인일: `2026-03-10`
- 왜 봤나: checksum, packet build, reply parsing이 문서 설명과 맞는지 확인했다.
- 무엇을 확인했나: PID 기반 identifier, `IHL` 파싱, timeout 처리 방식이 현재 코드와 일치함을 확인했다.
- 반영 결과: 설계 기록과 디버그 로그를 코드 기준으로 다시 쓸 수 있었다.

### [자동 테스트](../../python/tests/test_icmp_pinger.py)
- 확인일: `2026-03-10`
- 왜 봤나: 무엇이 현재 자동 검증 범위인지 확인하려고 읽었다.
- 무엇을 확인했나: checksum, packet build, 출력, 전손실 처리까지가 공식 테스트 범위임을 알 수 있었다.
- 반영 결과: `verified` 설명과 실제 검증 범위를 맞출 수 있었다.

### [checksum 문서](../concepts/checksum.md)
- 확인일: `2026-03-10`
- 왜 봤나: RFC 1071 checksum 설명을 더 친절하게 다시 쓰려고 읽었다.
- 무엇을 확인했나: odd byte 처리와 one’s complement 합산을 문장으로 풀어 쓸 수 있었다.
- 반영 결과: 지식 인덱스가 더 실용적으로 바뀌었다.

### [raw socket 문서](../concepts/raw-sockets.md)
- 확인일: `2026-03-10`
- 왜 봤나: 권한 제약과 실행 환경 차이를 다시 정리하려고 읽었다.
- 무엇을 확인했나: 왜 deterministic 테스트와 live 테스트를 분리해야 하는지 더 설득력 있게 설명할 수 있었다.
- 반영 결과: 실행 가이드가 현실적인 문서가 됐다.

### [비교 문서](../concepts/ping-comparison.md)
- 확인일: `2026-03-10`
- 왜 봤나: 시스템 `ping`과 구현체 차이를 정리하려고 읽었다.
- 무엇을 확인했나: 학생이 “왜 직접 구현하나”를 이해하는 데 필요한 문맥을 확보했다.
- 반영 결과: 친절한 설명 톤을 보강했다.

## 외부 기준
### [RFC 792: Internet Control Message Protocol](https://www.rfc-editor.org/rfc/rfc792)
- 확인일: `2026-03-10`
- 왜 봤나: ICMP Echo 메시지 필드 정의를 다시 확인하려고 봤다.
- 무엇을 확인했나: type/code, identifier, sequence의 의미를 표준과 맞춰 설명할 수 있었다.
- 반영 결과: 프로토콜 설명의 정확도가 올라갔다.

### [RFC 1071: Computing the Internet Checksum](https://www.rfc-editor.org/rfc/rfc1071)
- 확인일: `2026-03-10`
- 왜 봤나: checksum 알고리즘 설명을 검증하려고 참고했다.
- 무엇을 확인했나: 왜 16비트 one’s complement 합을 쓰는지와 구현 시 주의점을 다시 확인했다.
- 반영 결과: 디버그 로그와 개념 문서의 근거가 됐다.

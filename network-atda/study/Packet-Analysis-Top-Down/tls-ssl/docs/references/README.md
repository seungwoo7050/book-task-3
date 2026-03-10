# 참고 자료

TLS/SSL 분석 문서를 정리하면서 실제로 다시 확인한 자료다. handshake와 버전 차이를 trace와 개념 문서에 맞춰 설명하기 위해 사용했다.

## 저장소 내부 기준
### [문제 가이드](../../problem/README.md)
- 확인일: `2026-03-10`
- 왜 봤나: 질문 범위와 제출 형식을 다시 확인하려고 읽었다.
- 무엇을 확인했나: 이 실습이 handshake 관찰과 버전 비교에 초점을 둔다는 점을 분명히 할 수 있었다.
- 반영 결과: README와 분석 답안 구조를 더 명확히 만들었다.

### [캡처 데이터 안내](../../problem/data/README.md)
- 확인일: `2026-03-10`
- 왜 봤나: TLS trace가 어떤 실습 상황을 담는지 다시 확인했다.
- 무엇을 확인했나: handshake와 record 흐름을 어떤 패킷 순서로 설명할지 정리할 수 있었다.
- 반영 결과: 학생 안내 문장이 더 친절해졌다.

### [분석 답안](../../analysis/src/tls-ssl-analysis.md)
- 확인일: `2026-03-10`
- 왜 봤나: 현재 해설이 handshake의 어떤 단계에 기대는지 확인했다.
- 무엇을 확인했나: 질문별 답변과 패킷 근거를 현재 문서와 일치시킬 수 있었다.
- 반영 결과: 문서 일관성이 높아졌다.

### [TLS 개요 문서](../concepts/tls-protocol.md)
- 확인일: `2026-03-10`
- 왜 봤나: record layer와 handshake 흐름 설명을 다시 정리하려고 읽었다.
- 무엇을 확인했나: 암호 스위트와 인증서, 키 교환 설명을 더 차분하게 풀어 쓸 수 있었다.
- 반영 결과: 학습 친화적인 개념 요약이 강화됐다.

### [Handshake 상세 문서](../concepts/tls-handshake-detail.md)
- 확인일: `2026-03-10`
- 왜 봤나: 패킷 trace와 handshake 단계 매핑을 다시 정리하려고 읽었다.
- 무엇을 확인했나: ClientHello, ServerHello, key exchange 순서를 더 정확히 설명할 수 있었다.
- 반영 결과: 분석 답안이 더 설득력 있게 됐다.

### [버전 비교 문서](../concepts/tls-versions-comparison.md)
- 확인일: `2026-03-10`
- 왜 봤나: TLS 1.2와 1.3 차이를 정리하려고 읽었다.
- 무엇을 확인했나: trace에서 보이는 필드 차이를 버전 진화와 연결할 수 있었다.
- 반영 결과: 문서 품질이 올라갔다.

## 외부 기준
### Computer Networking: A Top-Down Approach, security / TLS discussion
- 확인일: `2026-03-10`
- 왜 봤나: TLS 실습의 학습 맥락을 다시 확인하려고 참고했다.
- 무엇을 확인했나: 패킷 해석을 보안 계층 개념과 연결하는 흐름을 잡을 수 있었다.
- 반영 결과: 문서를 더 학습 지향적으로 만들었다.

### [RFC 8446: The Transport Layer Security (TLS) Protocol Version 1.3](https://www.rfc-editor.org/rfc/rfc8446)
- 확인일: `2026-03-10`
- 왜 봤나: TLS 1.3 handshake와 record 의미를 다시 확인하려고 봤다.
- 무엇을 확인했나: 버전 비교와 handshake 설명을 표준과 맞출 수 있었다.
- 반영 결과: 개념 문서 정확도가 높아졌다.

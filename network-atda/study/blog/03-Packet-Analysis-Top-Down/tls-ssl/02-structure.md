# TLS Packet Analysis 구조 메모

## 문서 구성 의도

- `00-series-map.md`: TLS trace를 visibility boundary라는 질문으로 먼저 고정한다.
- `10-development-timeline.md`: TCP handshake 뒤 TLS handshake, 이어 encrypted application data로 넘어가는 전환을 chronology로 정리한다.
- `01-evidence-ledger.md`: answer markdown와 `tshark` 필터, 그리고 current env caveat를 짧게 묶는다.

## 이번 재작성에서 강조한 점

- cipher suite와 version field를 암기 포인트보다 trace-reading signal로 다룬다.
- malformed certificate와 current `tshark` field mismatch를 한계로 분명히 남긴다.
- decryption이 없으면 어디까지밖에 말할 수 없는지 선을 긋는다.

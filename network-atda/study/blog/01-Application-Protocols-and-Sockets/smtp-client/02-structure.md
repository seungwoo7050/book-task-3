# SMTP Client 구조 메모

## 문서 구성 의도

- `00-series-map.md`: 이 lab를 어떤 질문으로 읽을지 먼저 잡는다.
- `10-development-timeline.md`: TCP 연결, 명령 단계, `DATA`, 종료를 chronology로 복원한다.
- `01-evidence-ledger.md`: 실제 소스와 테스트 근거를 짧게 묶는다.

## 이번 재작성에서 강조한 점

- SMTP를 "메일 앱"이 아니라 "긴 텍스트 프로토콜 상태 기계"로 읽는다.
- `DATA` 구간과 일반 command/reply 구간의 차이를 분리해서 설명한다.
- 한계(`STARTTLS`, `AUTH LOGIN`, 외부 정책 미검증`)를 숨기지 않는다.

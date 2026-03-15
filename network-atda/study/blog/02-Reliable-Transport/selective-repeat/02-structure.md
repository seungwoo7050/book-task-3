# Selective Repeat 구조 메모

## 문서 구성 의도

- `00-series-map.md`: GBN 이후 무엇이 추가되는지 질문을 먼저 잡는다.
- `10-development-timeline.md`: per-packet timer, receiver buffer, buffer drain 순서를 chronology로 복원한다.
- `01-evidence-ledger.md`: source, test, rerun log를 짧게 고정한다.

## 이번 재작성에서 강조한 점

- 이 lab를 "window protocol 하나 더"가 아니라 `state explosion`을 감수하고 selective behavior를 얻는 단계로 읽는다.
- ACK와 delivery의 분리를 수신 버퍼 중심으로 설명한다.
- wraparound 미지원, 단일 loop timer scan, 성능 비교 미정리를 한계로 남긴다.

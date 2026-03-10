# 회고

## 왜 이 프로젝트가 재현성에 특히 좋은가
- 핵심 개념이 `merge`, `tombstone`, `manifest` 세 축으로 압축돼 있습니다.
- 구현 표면은 작지만, 한 줄만 틀려도 출력과 테스트 결과가 바로 달라집니다.
- 데모 출력이 짧고 결정적이라 “맞다/틀리다”를 학습자가 즉시 확인할 수 있습니다.

## 이번 단계에서 명확해진 것
- compaction의 본질은 정렬 병합이 아니라 “어떤 삭제를 언제 버려도 안전한가”를 판단하는 일입니다.
- data file과 metadata는 따로 설명하면 안 되고, 하나의 갱신 단위로 봐야 합니다.
- 읽기 성능 개선 단계도 결국 write path를 다시 조직하는 작업이라는 점이 더 분명해졌습니다.

## 아직 단순화한 부분
- single-shot compaction만 다루므로 scheduler, compaction debt, throttling은 없습니다.
- deepest level 판단도 학습용 단순화이며, 실제 시스템처럼 더 깊은 level map 전체를 계산하지는 않습니다.
- manifest crash recovery를 failure injection으로 증명하지는 않습니다.

## 다음에 확장한다면
- size-tiered와 leveled 정책을 같은 입력 데이터로 비교하는 실험을 붙일 수 있습니다.
- compaction 전후 파일 수, read amplification, tombstone 수를 시각화하면 학습 효과가 더 커집니다.
- L0 reverse를 일부러 깨뜨린 뒤 출력이 어떻게 망가지는지 보여 주는 failure demo를 추가할 수 있습니다.

## `06 Index Filter`로 넘길 질문
- compaction이 끝나도 point lookup은 여전히 파일을 읽습니다. 그 범위를 어떻게 더 줄일 것인가?
- 여러 SSTable을 하나로 합친 뒤, 어떤 메타데이터를 더 두면 `Get`이 덜 읽고도 끝날 수 있을까?

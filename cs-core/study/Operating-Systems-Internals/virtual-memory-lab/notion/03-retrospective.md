# 03 Retrospective

## 이번 설계에서 좋았던 점

- OPT를 같이 두니 다른 heuristic의 한계가 바로 보였다.
- dirty trace 하나만 추가해도 단순 hit/fault 계산기와의 차이가 분명해졌다.
- Clock을 포함해 “현실 구현에서 자주 택하는 근사 정책”도 함께 설명할 수 있었다.

## 아쉬운 점

- frame snapshot을 page 번호 기준으로 정렬했기 때문에 실제 frame slot 교체 순서는 숨겨진다.
- TLB와 page table이 없어서 address translation 전체 흐름까지는 이어지지 않는다.

## 다음 확장 후보

- frame count sweep
- write-back cost metric
- true frame-slot replay와 sorted snapshot의 이중 출력

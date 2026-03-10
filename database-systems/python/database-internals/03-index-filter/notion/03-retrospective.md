# 회고

## 이번 단계에서 명확해진 것
- point lookup 최적화는 “덜 읽는다”를 측정 가능하게 만들어야 학습 효과가 큽니다.
- false positive는 허용되지만 false negative는 금지된다는 asymmetric contract가 bloom filter의 핵심입니다.
- 희소 인덱스는 정렬된 파일 포맷 위에서만 자연스럽게 작동합니다.

## 아직 단순화한 부분
- block cache가 없어 반복 lookup의 이득은 아직 보여 주지 못합니다.
- 실제 workload별 false positive tuning은 실험하지 않았습니다.

## 다음에 확장한다면
- block cache를 더해 filter/index/cache 삼단계를 비교할 수 있습니다.
- key 분포와 목표 rate를 바꿔 filter sizing 실험을 추가할 수 있습니다.

## `04 Buffer Pool`로 넘길 질문
- 디스크 page를 여러 query가 반복해서 읽을 때는 어떤 cache 정책이 필요한가?
- 읽기 최적화 위에 transaction visibility를 얹으면 어떤 새 실패 모드가 생기는가?

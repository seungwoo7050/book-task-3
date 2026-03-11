# 03 Retrospective

## 이번 설계에서 좋았던 점

- 세 primitive를 같은 문제에 억지로 맞추기보다, 각자 잘 드러나는 시나리오를 나누는 편이 설명 가능성이 높았다.
- timing은 noisy하지만 wait count와 invariant는 비교적 안정적인 교육용 신호였다.
- shell test만으로도 세 시나리오의 핵심 계약을 빠르게 다시 확인할 수 있었다.

## 아쉬운 점

- unsafe baseline이 없어서 race가 실제로 얼마나 쉽게 생기는지는 문서 설명에 기대는 부분이 있다.
- wait event 정의가 primitive별로 완전히 같은 의미는 아니다.

## 다음 확장 후보

- unsafe counter baseline
- thread sanitizer 보조 실행 경로
- rwlock과 reader-heavy workload 추가

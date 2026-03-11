# 03 Retrospective

## 이번 설계에서 좋았던 점

- single burst만으로도 response/waiting 차이는 충분히 드러났다.
- SJF의 이상화된 가정과 MLFQ의 heuristic 성격을 같은 프로젝트 안에서 대비해 설명하기 좋았다.
- replay와 평균 지표를 함께 두니 “눈으로 보는 순서”와 “숫자로 보는 결과”가 같이 남는다.

## 아쉬운 점

- context switch overhead가 없어서 RR의 비용은 문서로만 설명된다.
- blocking/I/O가 없어서 실제 interactive workload의 복잡도는 아직 단순화돼 있다.

## 다음 확장 후보

- worst-case waiting time 출력
- context switch cost toggle
- CPU burst / I/O burst 혼합 workload

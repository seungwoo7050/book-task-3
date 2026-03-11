# References

## 핵심 참고 자료

- Operating Systems: Three Easy Pieces, Scheduling chapter
- Modern Operating Systems, CPU Scheduling overview
- Computer Systems: A Programmer's Perspective, process execution background

## 왜 이 자료를 참고했는가

- OSTEP은 waiting/response/turnaround와 MLFQ 규칙을 가장 학습 친화적으로 설명한다.
- Modern Operating Systems는 policy를 breadth 관점으로 비교할 때 용어 기준점이 된다.
- CS:APP는 실제 process 실행 흐름과 CPU 관점을 기존 `cs-core` 트랙과 연결할 때 도움이 된다.

## 현재 프로젝트에 남긴 흔적

- fixture는 textbook 예제를 그대로 복사하지 않고, convoy와 interactive mix를 설명하기 쉬운 self-authored workload로 재구성했다.
- MLFQ는 교육용 deterministic replay를 위해 dispatch-boundary boost로 단순화했다.

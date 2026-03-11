# References

## 핵심 참고 자료

- Operating Systems: Three Easy Pieces, Paging chapter
- Modern Operating Systems, virtual memory overview
- Belady anomaly classic examples

## 왜 이 자료를 참고했는가

- OSTEP은 locality와 replacement intuition을 가장 짧게 다시 잡기 좋다.
- Modern Operating Systems는 FIFO/LRU/Clock을 breadth 관점에서 연결해 읽을 때 기준이 된다.
- Belady anomaly 예시는 FIFO가 왜 단순하지만 위험한지 설명하는 가장 좋은 fixture 출발점이다.

## 현재 프로젝트에 남긴 흔적

- trace는 textbook 문장을 그대로 옮기지 않고, anomaly/locality/dirty eviction이 각각 드러나는 self-authored 파일로 재구성했다.
- replay는 frame index보다 어떤 page가 남아 있는지 먼저 보이도록 정렬 출력으로 단순화했다.

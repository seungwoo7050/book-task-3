# Locality And Faults

## locality를 왜 먼저 보는가

page replacement policy를 비교할 때 “어떤 policy가 더 똑똑한가”만 보면 자주 막힌다. 실제 fault 수는 policy만으로 정해지지 않고, trace가 어떤 locality를 가지는지가 먼저 결정한다.

- temporal locality가 강하면 최근에 본 page를 다시 볼 확률이 높다.
- spatial locality가 강하면 근처 page를 연속으로 접근하는 경향이 생긴다.
- page fault 수는 trace, frame 수, policy가 같이 만든 결과다.

## 이 프로젝트에서의 의미

- `locality.trace`는 LRU와 OPT가 FIFO보다 유리한 패턴을 보여 준다.
- 같은 trace라도 frame 수가 바뀌면 fault 수가 달라진다.
- OPT가 가장 적은 fault를 만들더라도, 그건 미래 접근을 안다는 비교 기준선일 뿐이다.

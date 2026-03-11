# Correctness Before Timing

## 왜 timing을 테스트 기준으로 쓰지 않는가

contention benchmark는 같은 머신에서도 run마다 시간이 흔들린다. scheduler noise, background load, CPU frequency 변화만으로도 값이 쉽게 달라진다.

- 따라서 테스트는 절대 elapsed time이 아니라 invariant와 upper bound를 확인해야 한다.
- timing은 demo와 회고 문서에서만 보조 지표로 보는 편이 안전하다.

## 이 프로젝트의 선택

- `ok=1`이 가장 중요한 결과다.
- `wait_events`는 contention이 있었는지 보는 보조 signal이다.
- `elapsed_ms`는 시나리오 간 상대적 느낌을 보는 값이지, pass/fail 기준이 아니다.

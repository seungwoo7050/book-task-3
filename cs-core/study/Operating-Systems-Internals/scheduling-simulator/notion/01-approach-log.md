# 01 Approach Log

## 설계 선택

- fixture를 JSON으로 고정해 policy 구현과 입력 해석을 분리했다. workload를 바꿔도 CLI와 test shape는 그대로 유지된다.
- process metric은 timeline을 재파싱하지 않고 `start`, `completion`, `burst`에서 직접 계산하게 했다. replay와 metrics 계산 로직이 엇갈리는 일을 줄이기 위해서다.
- MLFQ boost는 tick 도중이 아니라 dispatch boundary에서만 적용했다. 교육용 replay를 읽기 쉽게 만들고 golden test를 안정화하려는 선택이었다.
- canonical 명령은 `make -C problem test`와 `make -C problem run-demo`로 고정했다. README, notion, 실제 검증 루프가 어긋나지 않게 하기 위해서다.

## fixture를 두 개만 둔 이유

- `convoy.json`은 긴 job이 앞에 있을 때 FCFS와 SJF의 차이를 뚜렷하게 보여 준다.
- `interactive-mix.json`은 짧은 job이 뒤늦게 들어올 때 RR/MLFQ가 response time을 어떻게 바꾸는지 보여 준다.

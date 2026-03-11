# Scheduling Simulator 검증 기록

## canonical 명령

```bash
cd problem
make test
make run-demo
```

## 테스트가 고정하는 것

- `convoy.json`에서 FCFS, SJF, RR, MLFQ golden timeline
- SJF 평균 waiting time < FCFS 평균 waiting time
- RR 평균 response time < FCFS 평균 response time
- `interactive-mix.json`에서 MLFQ response time 개선

## demo에서 확인할 것

- policy별 replay 구간이 `start-end:PID` 형태로 출력된다
- summary 표에 `waiting / response / turnaround` 평균이 함께 나온다
- 같은 fixture를 다시 실행해도 출력 순서가 흔들리지 않는다

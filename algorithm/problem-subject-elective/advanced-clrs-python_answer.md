# advanced-clrs-python 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 주제: NP-완전성 실습, 학습 초점: 이론 중심 알고리즘을 작은 실험과 검증 가능한 입출력 문제로 재구성하는 연습, canonical fixture는 data/input*.txt, data/output*.txt에 둔다를 한 흐름으로 설명하고 검증한다. 핵심은 `verify_vc`와 `verify_3sat`, `solve` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 주제: NP-완전성 실습
- 학습 초점: 이론 중심 알고리즘을 작은 실험과 검증 가능한 입출력 문제로 재구성하는 연습
- canonical fixture는 data/input*.txt, data/output*.txt에 둔다.
- 첫 진입점은 `../study/Advanced-CLRS/0x18-np-completeness-lab/python/src/solution.py`이고, 여기서 `verify_vc`와 `verify_3sat` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/Advanced-CLRS/0x18-np-completeness-lab/python/src/solution.py`: `verify_vc`, `verify_3sat`, `solve`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Advanced-CLRS/0x18-np-completeness-lab/problem/code/starter.py`: `solve`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Advanced-CLRS/0x18-np-completeness-lab/problem/data/input1.txt`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `../study/Advanced-CLRS/0x18-np-completeness-lab/problem/data/input2.txt`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `../study/Advanced-CLRS/0x18-np-completeness-lab/problem/data/output1.txt`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `../study/Advanced-CLRS/0x18-np-completeness-lab/problem/Makefile`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.
- `verify_vc` 등이 맡는 책임을 한 함수에 뭉개지 말고 상태 전이 단위로 분리한다.
- 회귀 게이트는 `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Advanced-CLRS/0x18-np-completeness-lab/problem test`이며, 핵심 상태 전이를 바꿀 때마다 중간 검증으로 다시 실행한다.

## 정답을 재구성하는 절차

1. `../study/Advanced-CLRS/0x18-np-completeness-lab/problem/code/starter.py`와 `../study/Advanced-CLRS/0x18-np-completeness-lab/python/src/solution.py`를 나란히 열어 먼저 바뀌는 경계를 잡는다.
2. `verify_vc` 등이 맡는 책임을 분리해 각 출력 계약을 완성한다.
3. `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Advanced-CLRS/0x18-np-completeness-lab/problem test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make -C /Users/woopinbell/work/book-task-3/algorithm/study/Advanced-CLRS/0x18-np-completeness-lab/problem test
```

- `../study/Advanced-CLRS/0x18-np-completeness-lab/problem/code/starter.py` starter skeleton의 빈칸을 그대로 정답으로 착각하지 않는다.
- `../study/Advanced-CLRS/0x18-np-completeness-lab/problem/data/input1.txt` 등 fixture/trace를 읽지 않고 동작을 추측하지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Advanced-CLRS/0x18-np-completeness-lab/problem test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/Advanced-CLRS/0x18-np-completeness-lab/python/src/solution.py`
- `../study/Advanced-CLRS/0x18-np-completeness-lab/problem/code/starter.py`
- `../study/Advanced-CLRS/0x18-np-completeness-lab/problem/data/input1.txt`
- `../study/Advanced-CLRS/0x18-np-completeness-lab/problem/data/input2.txt`
- `../study/Advanced-CLRS/0x18-np-completeness-lab/problem/data/output1.txt`
- `../study/Advanced-CLRS/0x18-np-completeness-lab/problem/data/output2.txt`
- `../study/Advanced-CLRS/0x18-np-completeness-lab/problem/Makefile`

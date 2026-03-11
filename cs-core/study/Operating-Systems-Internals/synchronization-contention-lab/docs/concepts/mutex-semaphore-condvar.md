# Mutex Semaphore Condvar

## mutex

- shared state를 한 번에 한 thread만 만지게 하는 가장 기본적인 도구다.
- counter처럼 “업데이트 자체가 critical section”인 문제에 잘 맞는다.

## semaphore

- permit 수만큼의 동시 진입을 허용한다.
- gate처럼 “한 번에 N개까지만 안으로 들여보낸다”는 제약을 모델링할 때 자연스럽다.

## condition variable

- 어떤 조건이 만족될 때까지 잠들었다가 깨어나는 패턴을 만든다.
- bounded buffer처럼 producer와 consumer가 서로의 상태 변화를 기다리는 문제에 맞는다.

같은 synchronization이라도 primitive가 표현하는 계약이 다르기 때문에, 이 프로젝트는 세 도구를 한 시나리오에 억지로 맞추지 않고 각자 잘 드러나는 예제로 분리했다.

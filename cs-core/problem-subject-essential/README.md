# CS-Core 서버 개발 필수 문제지

`cs-core`에서 서버 공통 필수로 남긴 문제지만 모아 둡니다.
프로세스 제어, 프록시 I/O, 메모리 모델처럼 서버 런타임을 직접 설명하게 만드는 문제만 남깁니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [proxylab-c](proxylab-c.md) | 시작 위치의 구현을 완성해 프록시 구현 전에 기본 계약과 제약을 확인하고 싶은 학습자, shared helper와 driver wrapper의 역할을 알고 싶은 사람, 구현 디렉터리와 문제 경계를 분리하고 싶은 사람을 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/proxylab/c test` |
| [proxylab-cpp](proxylab-cpp.md) | 시작 위치의 구현을 완성해 프록시 구현 전에 기본 계약과 제약을 확인하고 싶은 학습자, shared helper와 driver wrapper의 역할을 알고 싶은 사람, 구현 디렉터리와 문제 경계를 분리하고 싶은 사람을 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/proxylab/cpp test` |
| [shlab-c](shlab-c.md) | 시작 위치의 구현을 완성해 공식 starter 없이도 과제 목적을 먼저 파악하고 싶은 학습자, 어떤 자산을 제거했고 무엇으로 대체했는지 알고 싶은 사람, 공개 가능한 문제 경계 문서를 설계하고 싶은 사람을 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/shlab/c test` |
| [virtual-memory-lab-python](virtual-memory-lab-python.md) | 시작 위치의 구현을 완성해 classic Belady anomaly 예제가 FIFO에서 재현된다, locality trace에서 LRU/OPT가 FIFO보다 나쁘지 않다, dirty trace에서 dirty eviction이 정확히 계산된다를 한 흐름으로 설명하고 검증한다. | `make test && make run-demo` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.

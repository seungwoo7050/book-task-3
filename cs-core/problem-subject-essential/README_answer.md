# CS-Core 서버 개발 필수 답안지

이 문서는 `cs-core` 필수 문제의 해답을 실제 소스와 테스트만으로 읽히게 정리한 답안지다. 핵심은 운영체제와 시스템 프로그래밍 개념을 "설명할 수 있다" 수준이 아니라, 프로세스 제어와 네트워크 I/O, 메모리 정책을 재현 가능한 코드로 구현하는 데 있다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [proxylab-c](proxylab-c_answer.md) | 시작 위치의 구현을 완성해 프록시 구현 전에 기본 계약과 제약을 확인하고 싶은 학습자, shared helper와 driver wrapper의 역할을 알고 싶은 사람, 구현 디렉터리와 문제 경계를 분리하고 싶은 사람을 한 흐름으로 설명하고 검증한다. 핵심은 handle_client와 client_error, parse_uri 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/proxylab/c test` |
| [proxylab-cpp](proxylab-cpp_answer.md) | 시작 위치의 구현을 완성해 프록시 구현 전에 기본 계약과 제약을 확인하고 싶은 학습자, shared helper와 driver wrapper의 역할을 알고 싶은 사람, 구현 디렉터리와 문제 경계를 분리하고 싶은 사람을 한 흐름으로 설명하고 검증한다. 핵심은 remove_entry와 insert_front, promote_entry 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/proxylab/cpp test` |
| [shlab-c](shlab-c_answer.md) | 시작 위치의 구현을 완성해 공식 starter 없이도 과제 목적을 먼저 파악하고 싶은 학습자, 어떤 자산을 제거했고 무엇으로 대체했는지 알고 싶은 사람, 공개 가능한 문제 경계 문서를 설계하고 싶은 사람을 한 흐름으로 설명하고 검증한다. 핵심은 handler_t와 eval, builtin_cmd 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/shlab/c test` |
| [virtual-memory-lab-python](virtual-memory-lab-python_answer.md) | 시작 위치의 구현을 완성해 classic Belady anomaly 예제가 FIFO에서 재현된다, locality trace에서 LRU/OPT가 FIFO보다 나쁘지 않다, dirty trace에서 dirty eviction이 정확히 계산된다를 한 흐름으로 설명하고 검증한다. 핵심은 build_parser와 main, PageAccess 흐름을 구현하고 테스트를 통과시키는 것이다. | `make test && make run-demo` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.

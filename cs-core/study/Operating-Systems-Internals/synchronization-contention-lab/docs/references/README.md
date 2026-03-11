# References

## 핵심 참고 자료

- Operating Systems: Three Easy Pieces, Concurrency chapters
- Modern Operating Systems, synchronization primitives overview
- POSIX threads and semaphore man pages

## 왜 이 자료를 참고했는가

- OSTEP은 race condition과 bounded buffer 예제를 가장 짧고 강하게 연결해 준다.
- Modern Operating Systems는 mutex, semaphore, condvar를 breadth 관점으로 다시 정리할 때 기준이 된다.
- POSIX 문서는 실제 `pthread`/`sem_*` API contract를 확인하는 데 필요하다.

## 현재 프로젝트에 남긴 흔적

- 세 시나리오는 textbook 예제를 그대로 복사하지 않고, invariant가 잘 드러나도록 self-authored benchmark로 재구성했다.
- macOS 호환성 때문에 unnamed semaphore 대신 named POSIX semaphore를 사용했다.

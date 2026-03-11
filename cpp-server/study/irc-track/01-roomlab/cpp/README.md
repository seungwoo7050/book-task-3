# roomlab C++ 구현

상태: `verified`  
기준일: `2026-03-11`

## 빌드와 테스트

```sh
make clean && make
make test
```

## 엔트리포인트

- [src/main.cpp](src/main.cpp): 서버 시작점

## 핵심 구현 파일

- [src/Connection.cpp](src/Connection.cpp): 연결별 상태 저장
- [src/Executor.cpp](src/Executor.cpp): core command 처리
- [src/execute_join.cpp](src/execute_join.cpp): JOIN/PART와 room lifecycle
- [src/Server.cpp](src/Server.cpp): 연결 수명주기와 cleanup

## 검증 파일

- [tests/test_roomlab.py](tests/test_roomlab.py): registration과 broadcast smoke test

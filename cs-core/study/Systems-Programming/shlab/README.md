# Shell Lab

`shlab`은 프로세스 그룹, foreground/background job control, `SIGCHLD` 처리, `fork` 주변 race를 작은 셸 구현으로 익히는 프로젝트다.

## 한눈에 보기

| 문제 | 중요 제약 | 이 레포의 답 | 검증 시작점 | 배우는 개념 | 상태 |
| --- | --- | --- | --- | --- | --- |
| foreground/background job control, builtin command, signal forwarding을 갖춘 tiny shell을 구현한다. | 공식 starter shell과 공식 trace는 저장소에 두지 않고, self-owned trace와 테스트 하네스로 계약을 재구성한다. | C 답은 [`c/src/tsh.c`](c/src/tsh.c), C++ 답은 [`cpp/src/tsh.cpp`](cpp/src/tsh.cpp), 공용 trace는 `tests/`와 각 구현 테스트에 둔다. | [`problem/README.md`](problem/README.md), [`c/README.md`](c/README.md), [`cpp/README.md`](cpp/README.md) | process group, signal forwarding, race discipline, job list 관리 | `public verified` |

## 디렉터리 역할

- `problem/`: self-owned 문제 계약과 최소 검증 경계
- `c/`, `cpp/`: shell 구현과 구현별 테스트
- `tests/`: 공용 trace와 시나리오
- `docs/`: job control flow, signal/race reasoning 정리
- `notion/`: 디버그 로그와 재검증 timeline

## 검증 빠른 시작

문제 경계 확인:

```bash
cd problem
make status
```

C 구현 검증:

```bash
cd c
make clean && make test
```

C++ 구현 검증:

```bash
cd cpp
make clean && make test
```

## 공개 경계

- 공개 문서는 process group, signal forwarding, race discipline을 설명한다.
- 공식 starter shell과 공식 trace는 공개 트리에 싣지 않고, `tests/`, `c/tests/`, `cpp/tests/`의 self-owned 검증 경로를 중심으로 유지한다.
- 긴 구현 reasoning은 `docs/`, `notion/`으로 분리한다.

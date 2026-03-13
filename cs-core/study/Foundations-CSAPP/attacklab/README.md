# Attack Lab

`attacklab`은 stack layout, code injection, ROP, 상대 주소 계산을 단계적으로 익히는 프로젝트다.

## 한눈에 보기

| 문제 | 중요 제약 | 이 레포의 답 | 검증 시작점 | 배우는 개념 | 상태 |
| --- | --- | --- | --- | --- | --- |
| 주어진 target의 호출 규약과 메모리 배치를 읽고, phase별로 control flow를 원하는 지점으로 유도한다. | 공식 target, cookie, exploit 검증은 로컬 전용이고, course target에 바로 적용 가능한 raw exploit은 저장소에 두지 않는다. | 공개 답은 [`c/src/mini_attacklab.c`](c/src/mini_attacklab.c), [`cpp/src/mini_attacklab.cpp`](cpp/src/mini_attacklab.cpp) companion과 [`docs/README.md`](docs/README.md) payload model 정리다. | [`problem/README.md`](problem/README.md), [`c/README.md`](c/README.md), [`cpp/README.md`](cpp/README.md) | stack layout, calling convention, ROP, 상대 주소 계산 | `verified (local-only asset)` |

실제 소스코드·테스트·검증 엔트리 기준의 blog 시리즈: [`../../blog/Foundations-CSAPP/attacklab/00-series-map.md`](../../blog/Foundations-CSAPP/attacklab/00-series-map.md)

## 디렉터리 역할

- `problem/`: 공식 target 복원, local-only verifier, 실행 스크립트
- `c/`, `cpp/`: 공격 모델을 설명하기 위한 companion 구현
- `docs/`: payload model, ROP, relative addressing 개념 정리
- `notion/`: phase별 분석 기록과 재검증 timeline

## 검증 빠른 시작

공식 self-study target 검증:

```bash
cd problem
make restore-official
make verify-official
```

C companion 검증:

```bash
cd c
make clean && make test
```

C++ companion 검증:

```bash
cd cpp
make clean && make test
```

## 공개 경계

- 공개 문서는 payload 사고법과 방어 기법 차이를 설명한다.
- 비공개 course target에 바로 적용 가능한 raw exploit 정보는 늘리지 않는다.
- `problem/official/` 아래 복원되는 target과 cookie 파일은 로컬 전용 자산이다.

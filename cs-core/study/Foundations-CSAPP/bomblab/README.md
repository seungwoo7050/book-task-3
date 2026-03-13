# Bomb Lab

`bomblab`은 x86-64 bomb를 brute force가 아니라 해석 절차로 풀어 가는 프로젝트다.

## 한눈에 보기

| 문제 | 중요 제약 | 이 레포의 답 | 검증 시작점 | 배우는 개념 | 상태 |
| --- | --- | --- | --- | --- | --- |
| phase별 입력 조건을 어셈블리에서 복원하고, 문자열 비교, 재귀, 리스트, 트리 패턴을 읽어낸다. | 공식 bomb 인스턴스별 정답은 저장소에 두지 않고, 공식 바이너리는 로컬 전용 자산으로 유지한다. | 공개 답은 [`c/src/mini_bomb.c`](c/src/mini_bomb.c), [`cpp/src/mini_bomb.cpp`](cpp/src/mini_bomb.cpp) companion과 [`docs/README.md`](docs/README.md) 분석 노트다. | [`problem/README.md`](problem/README.md), [`c/README.md`](c/README.md), [`cpp/README.md`](cpp/README.md) | reverse-engineering workflow, phase pattern 복원, 입력 조건 추론 | `verified (local-only asset)` |

실제 소스코드·테스트·검증 엔트리 기준의 blog 시리즈: [`../../blog/Foundations-CSAPP/bomblab/00-series-map.md`](../../blog/Foundations-CSAPP/bomblab/00-series-map.md)

## 디렉터리 역할

- `problem/`: 공식 bomb 복원과 로컬 분석 절차
- `c/`, `cpp/`: phase 패턴을 재현하는 companion 구현
- `docs/`: reverse-engineering workflow와 phase pattern 정리
- `notion/`: 가설, 디버깅, 재현 순서를 기록한 학습 노트

## 검증 빠른 시작

공식 self-study bomb 경계 검증:

```bash
cd problem
make restore-official
make verify-official
```

C companion 검증:

```bash
cd c
make clean && make test
printf 'Assembly reveals intent.\n1 2 4 8 16 32\n1 311\n6 6\n01234.\n4 6 2 3 5 1\n35\n' > /tmp/bomblab_c_answers.txt
./build/mini_bomb /tmp/bomblab_c_answers.txt
rm /tmp/bomblab_c_answers.txt
```

C++ companion 검증:

```bash
cd cpp
make clean && make test
printf 'Assembly reveals intent.\n1 2 4 8 16 32\n1 311\n6 6\n01234.\n4 6 2 3 5 1\n35\n' > /tmp/bomblab_cpp_answers.txt
./build/mini_bomb /tmp/bomblab_cpp_answers.txt
rm /tmp/bomblab_cpp_answers.txt
```

## 공개 경계

- 공개 문서는 역공학 workflow와 pattern 인식 중심으로 설명한다.
- course-instance 전용 bomb 정답과 대량 disassembly dump는 공개하지 않는다.
- `problem/official/` 아래 복원되는 공식 bomb 바이너리는 로컬 전용 자산이다.

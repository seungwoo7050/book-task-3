# Bomb Lab

## 이 프로젝트가 가르치는 것

`bomblab`은 x86-64 역공학을 "정답 맞히기"가 아니라 "모르는 바이너리를 해석하는 절차"로 배우게 만드는 프로젝트입니다.
문자열 비교, 분기 구조, 재귀, 연결 리스트, 트리 탐색 같은 패턴을 어셈블리에서 읽어내는 감각이 핵심입니다.

## 누구를 위한 문서인가

- `gdb`, `objdump`, `strings`, `nm`을 함께 써 보는 법이 필요한 학습자
- 공개 저장소에서 어디까지 설명하고 어디서 멈춰야 하는지 감이 필요한 사람
- companion 구현과 공식 과제 경계를 함께 정리하고 싶은 사람

## 먼저 읽을 곳

1. [`problem/README.md`](problem/README.md)
2. [`docs/README.md`](docs/README.md)
3. [`c/README.md`](c/README.md)
4. [`cpp/README.md`](cpp/README.md)
5. [`notion/README.md`](notion/README.md)

## 디렉터리 구조

```text
bomblab/
  README.md
  problem/
  c/
  cpp/
  docs/
  notion/
  notion-archive/
```

## 검증 방법

2026-03-10 문서 정비 기준으로 유지하는 검증 경로는 다음과 같습니다.

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

## 스포일러 경계

- 공개 문서는 역공학 워크플로와 패턴 인식 중심으로 설명합니다.
- course-instance 전용 bomb 정답이나 대량 disassembly dump는 공개하지 않습니다.
- `problem/official/` 아래 복원되는 공식 bomb 바이너리는 로컬 전용 자산입니다.

## 포트폴리오로 확장하는 힌트

- 이 프로젝트는 "문제를 어떻게 관찰하고 가설을 세웠는가"를 보여 주기 좋습니다.
- 개인 저장소에서는 phase별 사고 절차를 짧은 체크리스트로 재구성하면 학습 흔적이 더 선명해집니다.

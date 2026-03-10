# Bomb Lab 검증 기록

## 검증을 두 층으로 나누는 이유

이 프로젝트에는 두 종류의 검증이 있습니다.

- 공식 self-study bomb 경계 검증
- 저장소가 직접 작성한 companion mini-bomb 검증

둘을 분리해 두면 공개 범위를 지키면서도 학습 결과를 재실행할 수 있습니다.

## 공식 self-study bomb 검증

```bash
cd problem
make restore-official
make verify-official
```

2026-03-10 기준 기록:

- 복원한 공개 self-study bomb가 추적된 answers 파일로 6개 phase를 통과한다
- 공식 bomb 바이너리는 `problem/official/` 아래 로컬 전용으로만 유지한다

## C companion 검증

```bash
cd c
make clean && make test
printf 'Assembly reveals intent.\n1 2 4 8 16 32\n1 311\n6 6\n01234.\n4 6 2 3 5 1\n35\n' > /tmp/bomblab_c_answers.txt
./build/mini_bomb /tmp/bomblab_c_answers.txt
rm /tmp/bomblab_c_answers.txt
```

기록:

- `make test` 통과
- 예시 answers 파일로 phase 1~6과 secret phase까지 통과

## C++ companion 검증

```bash
cd cpp
make clean && make test
printf 'Assembly reveals intent.\n1 2 4 8 16 32\n1 311\n6 6\n01234.\n4 6 2 3 5 1\n35\n' > /tmp/bomblab_cpp_answers.txt
./build/mini_bomb /tmp/bomblab_cpp_answers.txt
rm /tmp/bomblab_cpp_answers.txt
```

기록:

- `make test` 통과
- 동일한 answers 파일 구조로 phase 1~6과 secret phase까지 통과

## 현재 판단

이 저장소는 공식 bomb 자체를 싣지 않으면서도,
"공식 과제 경계"와 "공개 가능한 companion 구현"을 둘 다 검증 가능한 형태로 유지하고 있습니다.

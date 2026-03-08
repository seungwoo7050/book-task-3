# Verification

## Official Problem Track

Commands:

```bash
cd problem
make restore-official
make verify-official
```

Current result:

- the restored public self-study bomb defuses all six phases with the tracked sample answers
- the official bomb binary remains local-only under the ignored `problem/official/` tree

## C Companion Track

Commands:

```bash
cd c
make clean && make test
printf 'Assembly reveals intent.\n1 2 4 8 16 32\n1 311\n6 6\n01234.\n4 6 2 3 5 1\n35\n' > /tmp/bomblab_c_answers.txt
./build/mini_bomb /tmp/bomblab_c_answers.txt
rm /tmp/bomblab_c_answers.txt
```

Actual result:

- `make clean && make test` passes
- end-to-end run defuses all six phases plus the secret phase

## C++ Companion Track

Commands:

```bash
cd cpp
make clean && make test
printf 'Assembly reveals intent.\n1 2 4 8 16 32\n1 311\n6 6\n01234.\n4 6 2 3 5 1\n35\n' > /tmp/bomblab_cpp_answers.txt
./build/mini_bomb /tmp/bomblab_cpp_answers.txt
rm /tmp/bomblab_cpp_answers.txt
```

Actual result:

- `make clean && make test` passes
- end-to-end run defuses all six phases plus the secret phase

## Current Judgment

The project is verifiable at both the official self-study and companion-track levels.

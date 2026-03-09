# msglab — 개발 타임라인

작성일: 2026-03-08

이 문서는 `msglab` 프로젝트의 전체 개발 과정을 시간순으로 기록한다. 소스코드에서 보이지 않는 정보 — 어떤 순서로 파일을 만들었고, 어떤 판단이 코드 구조를 결정했는지 — 를 복원하는 것이 목적이다.

---

## Phase 0: 환경과 설계 결정

### 전제 조건

- macOS 환경, C++17 컴파일러 (`c++` = Apple Clang)
- `legacy/` 디렉토리에 원본 프로젝트 보존
- `eventlab` 완료 상태 — event loop는 이미 분리됨

### 핵심 설계 결정

이 lab은 **서버가 없다.** 바이너리 이름도 `msglab_tests`이다 — 테스트 실행 파일이 곧 결과물이다. Python test runner도 불필요하다. C++ executable 하나로 모든 검증이 끝난다.

이 결정의 배경: parser는 네트워크 없이 검증 가능해야 한다. socket을 띄워야만 테스트할 수 있다면, parser bug와 network bug가 섞인다.

### 디렉토리 생성

```sh
mkdir -p study/msglab/cpp/src
mkdir -p study/msglab/cpp/include/inc
mkdir -p study/msglab/cpp/tests
mkdir -p study/msglab/docs/concepts
mkdir -p study/msglab/docs/references
mkdir -p study/msglab/notion
mkdir -p study/msglab/problem/code
mkdir -p study/msglab/problem/data
mkdir -p study/msglab/problem/script
```

---

## Phase 1: 레거시 분석과 파일 추출

### 레거시 코드 읽기

대상 파일:
- `legacy/src/Message.cpp` — prefix, command, params 추출 로직
- `legacy/src/Parser.cpp` — frame split, toupper, validator
- `legacy/src/inc/Message.hpp` — Message 데이터 모델
- `legacy/src/inc/Parser.hpp` — Parser 인터페이스

읽으면서 발견한 문제점:
1. `Parser.cpp`가 `Server.hpp`의 상수에 의존 → parser만 빌드할 수 없다
2. `Protocol.hpp`(WebSocket) 흔적이 parser 계층에 남아있다
3. `Message.hpp`에 game 전용 필드가 있다

### 복사가 아닌 재작성

이 발견들 때문에 단순 복사 대신 **재작성** 전략을 택했다. 레거시의 구조적 골격은 따르되, 불필요한 의존성을 제거하고 parser lab에 맞게 단순화한다.

---

## Phase 2: Message 클래스 작성

### Message.hpp

`include/inc/Message.hpp`를 작성했다.

핵심 결정:
- `label` enum: `PASS`, `NICK`, `USER`, `JOIN`, `PART`, `PRIVMSG`, `NOTICE`, `KICK`, `INVITE`, `TOPIC`, `MODE`, `PING`, `PONG`, `QUIT`, `CAP`, `UNK` — 총 16개
- `prefix`, `command`, `params` 세 멤버로 구성
- game 전용 필드 제거

### Message.cpp

`src/Message.cpp`를 작성했다. 레거시의 파싱 로직을 기반으로 하되, 다음을 변경:

1. prefix 읽기: 첫 문자가 `:`이면 다음 공백까지를 prefix로 추출
2. **prefix 읽기 후 `token.clear()`** — 이 한 줄이 레거시에 없어서 버그가 발생했다
3. command 읽기: 빈 토큰을 건너뛰고 첫 번째 비빈 토큰을 command로 취급, `Parser::toupper`로 정규화
4. `translator` 배열과 비교해서 `label` enum 결정
5. remaining params: trailing(`:` prefix)은 `\0`까지 한 덩어리로 읽음

---

## Phase 3: Parser 클래스 작성

### Parser.hpp

`include/inc/Parser.hpp`를 작성. static 함수들만 있는 utility 클래스 형태.

### Parser.cpp

`src/Parser.cpp`를 작성했다. 핵심 함수:

1. **`make_messages(stream, batch)`** — stream에서 `\n`으로 끝나는 line만 추출, incomplete fragment 보존
2. **`is_channel(token)`** — `#` 또는 `&`로 시작, 공백/콤마 불포함, 길이 2~32
3. **`is_nickname(token)`** — 알파벳 또는 특수문자(`[]\\{}|-`)로 시작, 길이 1~30
4. **`toupper/tolower`** — case 변환 helper
5. **`is_integer`, `is_facing`, `is_binary_flag`** — arena 커맨드용 validation helper
6. **`tokenize`** — delimiter 기반 string split

중요한 결정: `channel_types`(`#&`)와 길이 제한을 `Parser` 클래스의 static 상수로 정의. 레거시에서는 `Server`가 들고 있던 것을 parser 계층으로 옮겼다.

---

## Phase 4: 테스트 작성

### test_parser.cpp

`tests/test_parser.cpp`를 C++로 작성했다. `main()` 함수에서 테스트 함수를 순서대로 호출하고, 실패 시 `std::runtime_error`를 throw하는 구조.

테스트 함수 구성:

1. **`test_prefix_and_trailing()`**
   - 입력: `:nick!user@host PRIVMSG #cpp :hello world`
   - 검증: prefix, command label, parameter 개수, trailing text

2. **`test_validators()`**
   - valid/invalid nickname: `alice` (통과), `1alice` (거절), `bad nick` (거절)
   - valid/invalid channel: `#cpp` (통과), `cpp` (거절), `#bad,name` (거절)

3. **`test_make_messages_keeps_partial_line()`**
   - 입력: `"PING one\r\nJOIN #cpp\r\nPART #cpp"` (마지막은 `\n` 없음)
   - 검증: batch 크기 2, stream에 `"PART #cpp"` 보존

4. **`test_golden_transcripts()`**
   - 9개 IRC 명령에 대해 command label과 parameter 개수 검증
   - PASS, NICK, USER, JOIN, PRIVMSG, TOPIC, MODE, KICK, INVITE

5. **`test_arena_commands()`**
   - HELLO, INPUT, REJOIN의 parameter 파싱과 validator 확인
   - `is_integer`, `is_facing`, `is_binary_flag`의 경계 케이스 포함

---

## Phase 5: Makefile과 빌드

### Makefile 작성

```makefile
NAME := msglab_tests
SRCS := src/Message.cpp src/Parser.cpp tests/test_parser.cpp
```

특이점: `main.cpp`가 별도로 없다. `test_parser.cpp`에 `main()` 함수가 있어서 테스트 실행 파일이 곧 프로젝트의 유일한 바이너리다.

### 첫 빌드와 테스트

```sh
cd study/msglab/cpp
make clean && make
./msglab_tests
```

첫 실행에서 `test_prefix_and_trailing`이 실패 — "command translation failed". 이게 02-debug-log의 문제 1(prefix 뒤 token.clear 누락)이다.

수정 후:

```sh
make clean && make && make test
# → msglab parser tests passed.
```

---

## Phase 6: 문서 작성

### 프로젝트 문서

1. `problem/README.md` — 재구성된 문제 설명
2. `cpp/README.md` — 구현 상태, 빌드/테스트 명령
3. `docs/README.md` — 핵심 개념 포인터
4. `README.md` (프로젝트 루트) — 소개와 진입점

### notion/ 문서

1. `00-problem-framing.md` — 문제 해석과 범위 정의
2. `01-approach-log.md` — 접근 선택지와 결정 과정
3. `02-debug-log.md` — 버그와 해결
4. `03-retrospective.md` — 회고
5. `04-knowledge-index.md` — 재사용 가능한 지식

---

## Phase 7: 최종 검증

```sh
cd study/msglab/cpp
make clean && make && make test
# → msglab parser tests passed.
```

---

## 최종 파일 목록

```
study/msglab/
├── README.md
├── cpp/
│   ├── Makefile
│   ├── README.md
│   ├── include/inc/
│   │   ├── Message.hpp
│   │   └── Parser.hpp
│   ├── src/
│   │   ├── Message.cpp    ← 레거시 기반 재작성
│   │   └── Parser.cpp     ← 레거시 기반 재작성 + 의존성 제거
│   └── tests/
│       └── test_parser.cpp ← 신규 작성
├── docs/
│   ├── README.md
│   ├── concepts/
│   └── references/
├── notion/
│   ├── 00-problem-framing.md
│   ├── 01-approach-log.md
│   ├── 02-debug-log.md
│   ├── 03-retrospective.md
│   ├── 04-knowledge-index.md
│   └── 05-development-timeline.md
└── problem/
    ├── README.md
    ├── code/
    ├── data/
    └── script/
```

## 사용한 주요 도구와 명령어 요약

| 도구/명령 | 용도 |
| --- | --- |
| `c++` (Apple Clang) | C++17 컴파일러 |
| `make` | 빌드 자동화 |
| `./msglab_tests` | 테스트 직접 실행 (Python 불필요) |
| `diff` | 레거시 코드와 비교하며 불필요한 의존성 식별 |

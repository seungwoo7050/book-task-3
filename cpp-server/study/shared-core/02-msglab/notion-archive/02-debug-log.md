# msglab — 파서에서 만난 버그들, 그리고 눈에 안 보이던 문제

작성일: 2026-03-08

## 문제 1. prefix가 있으면 command가 엉뚱한 값으로 바뀌었다

### 어떻게 발견했는가

테스트를 처음 돌렸을 때 이런 실패 메시지가 나왔다:

> msglab parser tests failed: command translation failed

실패 케이스는 prefix가 붙은 `PRIVMSG`였다: `:nick!user@host PRIVMSG #cpp :hello world`

prefix가 없는 메시지(예: `NICK alice`)는 잘 통과했기 때문에, 처음에는 "특정 command에만 있는 문제인가?" 하고 삽질했다.

### 진짜 원인

`Message` 생성자에서 prefix를 읽고 나서, 임시 변수 `token`을 비우지 않는 코드가 있었다. prefix를 읽을 때 사용한 `token`에 값이 남아 있으면, 다음 while 루프에서 "비어있지 않은 첫 번째 토큰"으로 command를 잡을 때 prefix 잔재가 들어갈 수 있었다.

이 버그는 코드를 눈으로만 읽을 때는 잘 안 보인다. prefix가 있는 메시지와 없는 메시지를 모두 테스트해야만 드러난다.

### 어떻게 고쳤는가

prefix를 읽은 직후 `token.clear()`를 한 줄 추가했다. 수정 자체는 사소하지만, 이 버그는 parser의 핵심 신뢰도를 깨는 문제였다. command가 잘못 분류되면 그 위에 쌓이는 모든 로직이 무의미해지기 때문이다.

### 이 경험에서 배운 것

parser를 테스트할 때는 "정상 입력만 넣어보는" 것으로는 부족하다. **입력의 구조적 변형**(prefix 유/무, trailing 유/무, 빈 parameter 등)을 반드시 교차 검증해야 한다.

## 문제 2. partial line을 버리면 stream parser로서 위험하다

### 어떤 상황이었는가

레거시 parser에는 특정 흐름에서 stream을 통째로 비우는 방향으로 짜인 부분이 있었다. 제품 전체 안에서는 동작했더라도, 독립 parser lab 기준에서 보면 "아직 `\n`이 오지 않은 불완전한 line을 날려버릴 수 있다"는 점이 위험했다.

예를 들어 socket에서 `PING one\r\nJOIN #cpp\r\nPART #cpp`라는 데이터가 한 번에 들어왔다고 하자. 앞의 두 줄은 완전한 메시지이지만, `PART #cpp`는 아직 `\n`이 도착하지 않은 중간 상태일 수 있다. 이걸 무시하고 stream을 비워버리면, 다음 read에서 `\r\n`만 도착했을 때 "아무것도 없는 빈 메시지"가 된다.

### 어떻게 바꿨는가

`Parser::make_messages`를 `\n`으로 끝나는 완전한 line만 소비하도록 수정했다. 마지막 incomplete fragment는 stream에 그대로 남긴다. 테스트에서도 이 동작을 명시적으로 검증한다:

```
stream = "PING one\r\nJOIN #cpp\r\nPART #cpp"
→ batch.size() == 2 (PING, JOIN)
→ stream == "PART #cpp" (보존)
```

이 수정 덕분에 socket read cycle과 분리된 parser 테스트가 가능해졌고, 이후 `roomlab`과 `ircserv`에서도 같은 parser를 안전하게 재사용할 수 있게 되었다.

## 문제 3. parser가 Server와 Protocol을 끌고 다녔다

### 왜 문제였는가

레거시 프로젝트에서는 parser가 `Server.hpp`의 상수에 의존했고, WebSocket JSON envelope를 다루는 `Protocol.hpp`와도 연결되어 있었다. 이 상태에서는 parser만 따로 빌드할 수가 없다 — 컴파일하려면 `Server`와 `Protocol`의 전체 헤더 체인을 같이 들고 와야 한다.

이건 기술적 문제이기도 하지만 **커뮤니케이션 문제**이기도 하다. "msglab은 parser만 다루는 과제"라고 말하면서 내부적으로 서버 전체를 참조하고 있으면, 과제의 정체성이 모호해진다.

### 어떻게 해결했는가

- `channel_types`(`#&`)와 길이 제한을 `Parser` 클래스의 static 상수로 옮겼다.
- `Protocol.hpp` 의존성을 완전히 제거했다.
- `Message` 클래스에서 lab 범위 밖 필드(game 관련 등)를 제거했다.

결과적으로 `msglab`은 `Message.cpp`, `Parser.cpp`, `test_parser.cpp` 세 파일만으로 빌드하고 테스트할 수 있는 독립 과제가 되었다.

## 현재 남은 약점에 대한 솔직한 평가

- validator는 RFC의 모든 예외 규칙을 구현하지 않는다. 실용적 subset이라고 부를 수 있는 수준이다.
- command coverage도 이 트랙에서 실제 사용하는 명령 위주다 — 지원하지 않는 IRC 명령은 `UNK`로 분류된다.
- malformed line에 대한 세밀한 분류(가령 "command만 있고 parameter도 trailing도 없는 경우")는 테스트에서 깊이 다루지 않았다.

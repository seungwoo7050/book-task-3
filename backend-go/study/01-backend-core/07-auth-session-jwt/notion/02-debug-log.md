# 디버그 기록 — 인증에서 잘못될 수 있는 것들

## bcrypt 해시 길이와 포맷

bcrypt 해시는 `$2a$10$...` 형태의 60자 문자열이다. 처음에 해시를 잘라서 저장했다면 `CompareHashAndPassword`는 무조건 실패한다. 에러 메시지가 "crypto/bcrypt: hashedSecret too short"처럼 나오는데, 이걸 보지 않고 "비밀번호가 틀렸나?" 하고 비밀번호만 의심하면 시간을 낭비한다.

**교훈**: bcrypt 관련 에러가 나면 해시 문자열 자체를 먼저 출력해서 길이와 포맷이 맞는지 확인한다.

## Set-Cookie와 curl

`curl`에서 쿠키를 자동 저장하려면 `-c` 플래그를 쓴다:

```bash
curl -c cookies.txt -X POST http://localhost:4030/login/session \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"swordfish"}'
```

그리고 다음 요청에서 `-b cookies.txt`로 보낸다. 이걸 빠뜨리고 "세션이 안 된다"고 고민한 적이 있다면, 클라이언트가 쿠키를 실제로 보내는지 먼저 확인하라.

## JWT 만료 시간

`time.Now().Add(1 * time.Hour)` — 1시간 후 만료. 만료 시간을 `time.Now()`로 설정하면 생성 즉시 만료된다. 테스트에서 "방금 만든 토큰인데 왜 만료라고 나오지?"라면 `exp` 값이 과거인지 확인한다.

디코딩은 간단하다. JWT의 payload 부분을 base64 디코딩하면 JSON이 나온다:

```bash
echo "eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cCI6...}" \
  | base64 -d 2>/dev/null
```

## HMAC 검증 실패

JWT를 직접 구현했기 때문에, 서명 검증에서 `hmac.Equal`을 쓰지 않으면 타이밍 공격에 취약해진다. `bytes.Equal`이나 `==` 연산자는 첫 바이트가 틀리면 즉시 반환하기 때문에, 공격자가 서명을 바이트 단위로 추측할 수 있다. `crypto/hmac` 패키지의 `hmac.Equal`은 상수 시간 비교를 보장한다.

## sync.Mutex 필드 누락

세션 맵(`map[string]session`)은 동시 접근을 받는다. `Mutex`를 빠뜨리면 `-race` 플래그로 테스트할 때 즉시 data race가 감지된다. 서버 구조체에 `sync.Mutex`를 포함시키고, 세션 읽기/쓰기마다 Lock/Unlock을 호출한다.

```go
s.mu.Lock()
s.sessions[token] = sess
s.mu.Unlock()
```

## Content-Type 없이 POST

`curl`로 JSON을 보내면서 `-H "Content-Type: application/json"`을 빼먹으면, 서버의 `json.NewDecoder`는 정상 작동하지만 일부 프레임워크에서는 415 (Unsupported Media Type)를 반환한다. 이 프로젝트에서는 직접 `Decode`를 호출하므로 Content-Type을 검사하지 않지만, 실무에서는 미들웨어로 Content-Type을 강제하는 게 일반적이다.

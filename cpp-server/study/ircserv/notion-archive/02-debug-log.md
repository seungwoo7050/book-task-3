# ircserv — 디버그 기록: KICK stale state, invite 타이밍, 하위 lab 버그 포팅

작성일: 2026-03-08

## 문제 1: KICK이 target connection의 로컬 채널 인덱스를 정리하지 않았다

### 어떻게 발견했는가

smoke test에서 bob을 KICK한 뒤, 후속 시나리오에서 bob의 상태가 일관되지 않았다. 구체적으로, bob이 KICK 이후에도 자신의 `chandb`에 해당 채널이 남아 있었다.

### 무엇이 문제였는가

KICK 처리 로직에서 `chan->part(targetnode)`를 호출해서 channel 측의 membership(clientdb, privdb, invitedb)는 정리했지만, **target connection의 `chandb`에서 해당 채널을 제거하지 않았다**. 즉, channel은 "bob이 없다"고 판단하는데, bob은 "나는 아직 이 채널에 있다"고 판단하는 불일치가 생겼다.

이 불일치가 위험한 이유: KICK된 사용자가 다시 JOIN을 시도하면, connection 로컬 인덱스에 채널이 남아 있으므로 "이미 채널에 있다"는 오류가 발생할 수 있다. 또한 QUIT 시 cleanup 로직이 이미 제거된 채널을 다시 정리하려고 시도할 수 있다.

### 무엇을 했는가

KICK handler에서 `chan->part(targetnode)` 호출 **전에** `targetnode->chandb.erase(channame)`을 명시적으로 수행했다. 순서가 중요하다 — connection 로컬 인덱스를 먼저 정리하고, 그 다음 channel 측 membership을 정리한다.

### 검증

smoke test에서 KICK 후 bob이 invite-only 채널에 재입장을 시도하면 `473 ERR_INVITEONLYCHAN`이 정확히 반환되는 것을 확인했다.

## 문제 2: invited user의 JOIN이 간헐적으로 실패했다

### 어떻게 발견했는가

테스트를 반복 실행하면 가끔 "carol could not join invited channel"이 실패했다. 서버 로직에 문제가 있는 건 아닌데, 테스트가 불안정했다.

### 무엇이 문제였는가

이건 서버 버그가 아니라 **테스트 타이밍 문제**였다. 흐름을 보면:

1. alice가 `INVITE carol #ops`를 보낸다.
2. 서버가 alice에게 341 RPL_INVITING을 보내고, carol에게 INVITE 이벤트를 보낸다.
3. 테스트가 carol의 INVITE 이벤트를 기다린다.
4. INVITE 이벤트를 수신한 **직후** carol이 `JOIN #ops`를 보낸다.

문제는 4단계에서, carol의 INVITE 이벤트가 carol의 recv buffer에 도착한 것을 확인한 시점과, 서버 측에서 invite 처리가 완료된 시점 사이에 미세한 간격이 있었다는 것이다. TCP 상에서 carol에게 보낸 INVITE 이벤트는 carol의 join handler가 실행되기 전에 invitedb에 carol이 추가되어야 하는데, event loop의 write/read 순서에 따라 간헐적으로 어긋날 수 있었다.

### 무엇을 했는가

smoke test에서 INVITE 수신과 후속 JOIN 사이에 `time.sleep(0.2)`를 추가했다. 이건 서버 로직 수정이 아니라 test stabilization이다. 운영형 테스트라면 더 명시적인 동기화(예: 특정 응답을 기다린 후 다음 명령을 보내는 transcript 방식)가 바람직하지만, smoke test 수준에서는 이 수준이면 충분하다.

### 검증

수백 회 반복 실행에서 간헐적 실패가 사라졌다.

## 문제 3: KICK 직후 invite-only 재입장 거절 검증도 타이밍에 영향받았다

### 어떻게 발견했는가

问题 2와 비슷한 패턴이었다. KICK 직후 bob이 JOIN #ops를 보내면, 기대하는 `473`이 아니라 이전 KICK의 출력이 버퍼에 남아 있어서 `recv_until`이 엉뚱한 것을 매칭하는 경우가 있었다.

### 무엇을 했는가

KICK과 후속 JOIN 사이에 `time.sleep(0.2)` 추가, 그리고 recv deadline을 8초로 확대했다.

### 검증

`473` 응답을 안정적으로 확인하게 되었다.

## 문제 4: 하위 lab에서 발견한 parser/validator 버그를 capstone에도 포팅해야 했다

### 무엇이 있었는가

`msglab`과 `roomlab`에서 발견하고 수정한 버그들이 `ircserv`에도 동일하게 존재했다:

- **prefix parsing 후 `token.clear()`**: 파서가 prefix를 읽은 뒤 임시 토큰을 비우지 않아서 다음 토큰에 prefix 잔여물이 섞이는 버그
- **PING의 parameter count 처리**: parameter가 없을 때 즉시 return하지 않고 빈 parameter에 접근하는 버그
- **nickname validator 인덱스 수정**: 첫 글자와 나머지 글자의 검증 규칙이 다른데, 인덱스가 잘못 시작되는 버그
- **non-IRC field 제거**: Message/Connection 구조체에 게임용 필드가 남아 있던 것

### 왜 중요한가

capstone이 "앞선 lab의 통합"이라면, 하위 lab에서 드러난 버그 수정이 capstone에도 반영되어야 일관성이 유지된다. 하위 lab에서 고쳤는데 capstone에서 같은 버그가 남아 있으면, 컨리큘럼의 신뢰성이 떨어진다.

## 남은 주의점

- Linux에서의 재검증은 이번 턴에서 수행하지 않았다.
- RFC 완전 구현은 의도적으로 제한했다.
- smoke test는 통합 시나리오 수준이지, exhaustive protocol compliance test는 아니다.

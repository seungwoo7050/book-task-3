# Failure-Injected Log Replication 에세이

leader election이 끝났다고 해서 분산 시스템이 끝난 것은 아니다. 이제부터는 실제 write가 partial failure를 만나도 어떻게 살아남는지를 보여 줘야 한다.  
이 프로젝트는 그 질문을 아주 작은 replication harness로 압축한다.

## commit과 convergence는 같은 말이 아니다

학습자가 가장 자주 헷갈리는 지점이 바로 이것이다.

- `commit`: 이 write를 성공으로 인정해도 되는가
- `convergence`: 뒤처진 follower가 결국 leader와 같은 상태에 도달하는가

quorum commit은 모든 follower가 다 따라와야만 성립하는 게 아니다. 반대로 follower convergence는 commit이 일어났다고 저절로 끝나는 것도 아니다.  
이 둘을 분리해서 보여 주면 partial failure의 의미가 훨씬 분명해진다.

## 왜 drop, duplicate, pause 세 가지면 충분한가

실제 네트워크는 더 복잡하지만, 학습용 프로젝트에서 가장 먼저 봐야 하는 실패는 세 가지다.

### drop
메시지가 아예 사라진다.  
이 장면이 있어야 retry의 필요성이 보인다.

### duplicate
같은 메시지가 두 번 온다.  
이 장면이 있어야 follower apply가 idempotent해야 한다는 점이 보인다.

### pause
특정 follower로 가는 메시지가 잠시 막힌다.  
이 장면이 있어야 quorum commit은 유지되지만 lagging follower가 남는다는 점이 보인다.

## 왜 explicit message type을 드러냈는가

이 프로젝트는 메시지를 `append`와 `ack` 두 종류로만 유지한다.  
메시지 종류를 줄이면 failure injection이 무엇을 흔드는지 바로 읽힌다.

- `append`가 drop되면 follower가 뒤처진다.
- `ack`는 leader의 commit 판단을 움직인다.
- duplicate `append`는 follower safety를 시험한다.

메시지를 명시적으로 드러내면 네트워크 하네스도 단순해지고, 테스트도 훨씬 읽기 쉬워진다.

## nextIndex를 왜 leader가 가져야 하는가

retry는 “다시 보내자”만으로는 충분하지 않다. 어디부터 다시 보내야 하는지를 알아야 한다.  
그래서 leader는 follower별 `nextIndex`를 들고 있고, follower가 뒤처지면 그 위치부터 다시 보낸다.

이 구조를 통해 다음 장면이 가능해진다.

- node-2가 첫 entry를 놓친다.
- leader는 node-2의 `nextIndex`가 아직 0인 것을 안다.
- 다음 tick에 같은 entry를 다시 보낸다.
- follower가 결국 leader를 따라잡는다.

이게 retry의 최소 형태다.

## 왜 duplicate safety가 먼저여야 하는가

retry를 넣으면 duplicate delivery는 거의 필연적으로 따라온다.  
그런데 duplicate handling이 안전하지 않으면 retry 자체가 상태를 망가뜨린다.

그래서 이번 프로젝트는 follower 쪽에서 같은 index의 같은 entry를 idempotent하게 무시하게 했다.  
이 규칙이 있어야 retry와 failure recovery를 안심하고 보여 줄 수 있다.

## 트랙 안에서의 역할

이 프로젝트는 Go DDIA 심화 트랙의 마지막 분산 슬롯으로, 앞선 두 질문을 실제 write path에 다시 연결한다.

- 06은 최신 read 조건을 본다.
- 07은 authority 교체 조건을 본다.
- 08은 authority가 있다고 가정한 뒤 partial failure를 견디는 복제 경로를 본다.

즉, 이 프로젝트는 “leader가 있다고 치면 그 leader의 write는 장애 앞에서 어떻게 살아남는가?”를 묻는 단계다.

## 다시 구현할 때 기억할 것

- commit index와 follower watermark를 같은 값으로 취급하지 말 것
- duplicate append는 log와 apply count를 두 번 늘리면 안 됨
- paused follower는 resume 뒤 retry로 catch-up시켜야 하며, 그 전에도 quorum commit은 가능해야 함

이 세 가지를 지키면 작은 하네스만으로도 partial failure의 핵심을 충분히 전달할 수 있다.

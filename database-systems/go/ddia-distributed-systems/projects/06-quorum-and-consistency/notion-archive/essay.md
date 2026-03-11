# Quorum and Consistency 에세이

`replication`을 구현한 뒤 가장 먼저 부딪히는 질문은 “그래서 어느 값을 최신이라고 믿을 것인가?”다. follower catch-up까지만 구현하면 복제 경로는 보이지만, read가 어떤 replica를 봤는지에 따라 결과가 달라질 수 있다는 사실은 아직 흐릿하다. 이 프로젝트는 그 질문을 `N/W/R` 세 숫자로 압축한다.

## 왜 register부터 시작하는가

실제 분산 저장소는 shard, leader election, background repair, anti-entropy, conflict merge까지 한꺼번에 얽혀 있다. 이 상태에서 consistency를 설명하면 대부분의 학습자는 “왜 stale read가 생겼는지”보다 “기능이 너무 많다”는 인상만 받는다.

그래서 이 단계에서는 single-key, single-version register로 줄였다.

- key는 하나여도 충분하다.
- replica는 3개면 quorum 겹침을 보기에 충분하다.
- version은 정수 하나면 read merge를 설명하기에 충분하다.

복잡성을 버리는 대신 핵심만 남긴 셈이다.

## `W + R > N`의 진짜 의미

많이 알려진 식이지만, 학습자가 가장 자주 오해하는 식이기도 하다.

- 이 식은 “모든 replica가 항상 최신”을 뜻하지 않는다.
- 이 식은 “read quorum과 write quorum이 반드시 한 번은 겹친다”를 뜻한다.

그 겹치는 한 replica만 최신 version을 들고 있어도 read merge는 최신값을 고를 수 있다. 반대로 `W + R <= N`이면 read quorum이 write quorum과 완전히 분리될 수 있고, stale replica만 봐도 read가 성공한다.

이 차이를 코드로 보면 consistency는 추상적 철학이 아니라 responder 집합의 수학이라는 사실이 드러난다.

## 왜 responder 선택을 결정적으로 고정했는가

랜덤 responder를 쓰면 stale read 데모가 실행마다 달라진다. 그건 실전 시스템에서는 자연스럽지만 학습용 프로젝트에서는 오히려 독이다.  
이번 구현은 replica order를 고정하고, read quorum도 그 순서대로 responder를 고른다.

이 선택 덕분에 다음이 가능해진다.

- stale read를 항상 같은 fixture로 재현할 수 있다.
- “운이 나빠서 stale read가 나왔다”가 아니라 “이 responder 집합이 write quorum과 안 겹쳤다”로 설명할 수 있다.
- 테스트가 deterministic해진다.

## 이번 단계가 일부러 하지 않은 것

이 프로젝트는 Dynamo clone이 아니다. 다음 요소들은 의도적으로 뺐다.

- sloppy quorum
- hinted handoff
- read repair
- vector clock
- concurrent write merge

이것들을 넣으면 현실성은 올라가지만, 첫 consistency lab의 전달력은 오히려 떨어진다. 현재 목표는 “왜 quorum이 필요한가”를 한 번에 이해시키는 것이다.

## 이 프로젝트가 트랙 안에서 하는 일

Go DDIA 트랙을 순서대로 보면 이 프로젝트의 역할이 분명해진다.

1. `02-leader-follower-replication`은 복제가 어떻게 움직이는지 보여 준다.
2. `05-clustered-kv-capstone`은 routing, replication, storage를 한 흐름으로 묶는다.
3. `06-quorum-and-consistency`는 그다음 질문, 즉 “무엇을 최신이라고 읽을 것인가”를 떼어 낸다.

authority 문제는 아직 다루지 않는다. 그건 다음 `07-heartbeat-and-leader-election`의 역할이다.

## 다시 구현할 때 기억할 것

- version은 quorum write 성공 뒤에만 올라가야 한다.
- stale read는 read quorum이 write quorum과 안 겹치도록 fixture를 설계해야 한다.
- responder를 함께 반환해야 “왜 이 값이 나왔는가”를 설명할 수 있다.

이 세 가지만 지키면 코드는 작아도 메시지는 충분히 강하다.

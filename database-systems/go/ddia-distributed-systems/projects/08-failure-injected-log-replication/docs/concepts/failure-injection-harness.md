# Failure Injection Harness

이 프로젝트의 하네스는 실제 네트워크를 흉내 내는 게 아니라, replication 코드가 어떤 실패에 반응해야 하는지 관찰 가능한 장면으로 압축하는 장치입니다.

## 지원하는 세 가지 실패

- `drop`: 특정 메시지를 한 번 버립니다.
- `duplicate`: 특정 메시지를 두 번 전달합니다.
- `pause`: 특정 node로 가는 메시지를 잠시 막습니다.

## 왜 이 세 가지면 충분한가

- `drop`은 retry 필요성을 보여 줍니다.
- `duplicate`는 idempotent apply가 왜 필요한지 보여 줍니다.
- `pause`는 quorum commit은 유지되지만 lagging follower가 생기는 장면을 보여 줍니다.

## 일부러 생략한 것

- out-of-order delivery
- ack corruption
- long-tail latency distribution

이번 단계는 replication path가 실패를 어떻게 견디는지 설명하는 데만 집중합니다.

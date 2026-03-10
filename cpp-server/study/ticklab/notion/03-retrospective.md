# ticklab 회고

## 이 lab의 가치

`ticklab`은 작지만 게임 서버 문서에서 가장 설명력이 높은 질문을 다룬다. 네트워크를 붙이기 전에 simulation을 고정해 두면, 나중에 버그와 설계 논의를 훨씬 분명하게 나눌 수 있다.

## 아직 약한 부분

- 네트워크 지연과 재전송은 다루지 않는다.
- prediction, rollback 같은 고급 주제는 아직 없다.

## 포트폴리오로 옮길 때의 조언

- deterministic test를 꼭 증거로 남긴다.
- reconnect와 snapshot을 “있다”가 아니라 “왜 필요한가”로 설명한다.
- `arenaserv`에서 네트워크 층이 어떻게 붙는지 이어서 보여 준다.

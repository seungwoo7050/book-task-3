# shared-core

## 이 트랙이 푸는 문제

IRC 서버와 게임 서버를 읽기 전에, 공통으로 필요한 두 가지를 먼저 분리해야 한다. 하나는 non-blocking 런타임이고, 다른 하나는 입력을 구조화하는 parser 경계다. 이 둘을 먼저 떼어 두지 않으면 뒤쪽 capstone에서 버그 원인이 계속 섞여 보인다.

## 내가 만든 답

- [01-eventlab](01-eventlab/README.md)에서 연결 수명주기와 event loop만 먼저 검증한다.
- [02-msglab](02-msglab/README.md)에서 parser와 validation을 네트워크에서 분리해 검증한다.
- 두 lab을 모두 마친 뒤 IRC 축과 게임 서버 축으로 갈라진다.

## 포함 lab

| 순서 | lab | 답의 형태 |
| --- | --- | --- |
| 1 | [01-eventlab](01-eventlab/README.md) | non-blocking TCP loop와 smoke test |
| 2 | [02-msglab](02-msglab/README.md) | parser/validator와 transcript test |

## 읽는 순서

1. [01-eventlab/README.md](01-eventlab/README.md)
2. [02-msglab/README.md](02-msglab/README.md)
3. IRC 서버를 계속 보려면 [../irc-track/README.md](../irc-track/README.md)
4. 게임 서버를 보려면 [../game-track/README.md](../game-track/README.md)

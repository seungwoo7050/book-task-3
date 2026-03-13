# shared-core Source-First Blog

`shared-core`는 이 저장소의 가장 아래층을 먼저 정리해 보는 축이다. 뒤의 capstone이 무엇을 더했는지 보려면, 먼저 서버가 최소한으로 가져야 할 runtime과 parser 표면이 어디서 끝나는지부터 분명해야 한다. 이 트랙은 바로 그 바닥을 두 개의 작은 lab으로 나눠 보여 준다.

읽는 순서는 `eventlab` 다음 `msglab`이 자연스럽다. 먼저 event loop와 keep-alive 같은 런타임 문제를 따로 고정하고, 그다음 line framing과 validation을 네트워크 I/O에서 떼어 낸다. 그렇게 읽고 나면 뒤의 IRC와 game server 문서에서 어떤 책임이 재사용되는지 훨씬 잘 보인다.

- [eventlab](01-eventlab/README.md)
- [msglab](02-msglab/README.md)


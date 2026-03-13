# irc-track Source-First Blog

`irc-track`은 공용 기초 위에 실제 상태 전이를 얹는 첫 축이다. 시작점인 `roomlab`은 registration과 room lifecycle만 분명하게 보이는 IRC subset 서버를 다루고, `ircserv`는 같은 뼈대 위에 capability, mode, invite, kick 같은 capstone 범위를 열어 준다.

두 문서를 이어서 읽으면 차이가 기능 수보다 설계 경계에서 더 잘 보인다. 같은 runtime과 parser를 쓰더라도, 어떤 명령을 dispatcher에 열었는지와 channel privilege/state를 어디까지 모델링했는지가 capstone의 진짜 변화라는 점이 드러난다.

- [roomlab](01-roomlab/README.md)
- [ircserv](02-ircserv/README.md)


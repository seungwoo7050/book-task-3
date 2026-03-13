# game-track Source-First Blog

`game-track`은 게임 서버를 바로 소켓 위에 올리지 않고, 먼저 authoritative simulation을 고정한 뒤 transport를 붙이는 흐름으로 읽는 축이다. 그래서 `ticklab`과 `arenaserv`의 차이는 "규칙이 더 많아졌다"보다 "같은 규칙을 어떤 bridge 코드로 TCP에 연결했는가"에 더 가깝다.

읽을 때는 먼저 `ticklab`에서 phase, input, projectile, reconnect grace를 headless engine으로 확인하고, 그다음 `arenaserv`에서 timed event loop와 session token bridge가 어떻게 붙는지 보는 편이 가장 자연스럽다. 이렇게 보면 capstone이 새 규칙을 만든다기보다, 이미 검증한 규칙을 네트워크 위로 올리는 과정이라는 점이 잘 드러난다.

- [ticklab](01-ticklab/README.md)
- [arenaserv](02-arenaserv/README.md)


# Simulation

## match 규칙

- 매치 시간: 기본 `90초`
- server tick: `20 Hz`
- snapshot 전송: `10 Hz`
- 액션: `move`, `dash`, `fire`
- projectile hit: 피해 적용
- death: `3초` 뒤 respawn
- reconnect window: 기본 `20초`

## 시작 조건

이 구현에서는 `room->players.size() == room->max_players`이고 전원이 `READY=1`일 때만 매치를 시작한다. 4인 방이면 4명이 모두 차야 하고, 2인 방이면 2명이 모두 준비되어야 한다.

이 규칙을 둔 이유는 load smoke와 포트폴리오 설명이 "설계한 room size대로 정확히 매치를 구성한다"는 전제를 더 쉽게 보여주기 때문이다.

## fixed tick 처리

- tick timer는 room strand에서 `1000 / tick_hz` 간격으로 돈다.
- 각 tick에서 disconnect timeout, respawn, input 적용, projectile 이동을 순서대로 처리한다.
- 종료 조건은 `match_duration_ms` 만료 또는 non-forfeited player가 1명 이하가 되는 시점이다.

## reconnect / forfeit

- TCP disconnect가 감지되면 해당 player를 disconnected 상태로 표시한다.
- resume window 안에 `RESUME + UDP_BIND`가 오면 같은 player/session으로 복구한다.
- resume window가 지나면 해당 플레이어는 forfeit 처리된다.
- 최종 승자 계산은 non-forfeited player를 우선한다.

## 구현 메모

- scripted bot은 `ROOM_UPDATE`를 받을 때 `READY=1`을 한 번만 보낸다.
- 서버도 ready 값이 바뀐 경우에만 `ROOM_UPDATE`를 다시 브로드캐스트한다.
- 이 규칙이 없으면 `ROOM_UPDATE -> READY -> ROOM_UPDATE` echo loop가 생긴다.

# Persistence

## 저장 범위

전투 중 상태는 메모리에만 두고, 계정과 누적 전적, 매치 결과만 SQLite에 저장한다.

## schema

- `players(id, name UNIQUE, created_at, last_login_at)`
- `player_stats(player_id, games_played, wins, losses, kills, deaths)`
- `match_history(id, started_at, ended_at, winner_player_id, result_blob)`

## login 흐름

- `LOGIN name=<player_name>`이 오면 없으면 생성하고, 있으면 기존 player를 재사용한다.
- `player_stats` row가 없으면 같이 만든다.
- `LOGIN_OK`에는 `player_id`, `resume_token`, 누적 전적이 함께 포함된다.

## match 결과 저장

- match 종료 시 `match_history`에 한 행을 추가한다.
- snapshot entity 목록을 바탕으로 `player_stats`의 `games_played`, `wins`, `losses`, `kills`, `deaths`를 갱신한다.
- 저장 과정은 transaction으로 감싼다.

## 구현 주의점

SQLite 연결은 하나만 열고 공유하지만, repository 내부 mutex로 모든 DB 호출을 직렬화한다. 초기 구현에서는 login path가 잠금 없이 동시에 들어와서 flaky hang을 만들 수 있었고, 최종 버전에서 이를 수정했다.

# References

이 프로젝트는 외부 링크보다 저장소 내부의 재현 가능한 자료를 우선 참조한다.

## 확인한 로컬 자료

- 확인일: `2026-03-07`
- `problem/code/control-protocol.txt`
  이유: TCP/UDP public interface를 프로젝트 README와 구현 설명에 맞추기 위해 확인했다.
  반영: `docs/concepts/protocol.md`
- `problem/data/schema.sql`
  이유: SQLite schema와 문서 설명이 어긋나지 않게 맞추기 위해 확인했다.
  반영: `docs/concepts/persistence.md`
- `cpp/include/arena/protocol.hpp`
  이유: binary packet field와 테스트 범위를 문서에 정확히 반영하기 위해 확인했다.
  반영: `docs/concepts/protocol.md`
- `cpp/include/arena/state.hpp`
  이유: fixed tick, projectile, respawn, forfeit 규칙을 문서화하기 위해 확인했다.
  반영: `docs/concepts/simulation.md`
- `cpp/src/arena_server.cpp`
  이유: room strand, session strand, match start 조건, reconnect 흐름을 설명하기 위해 확인했다.
  반영: `docs/concepts/architecture.md`, `docs/concepts/simulation.md`
- `problem/script/load_smoke_test.py`
  이유: canonical smoke가 실제로 무엇을 검증하는지 정리하기 위해 확인했다.
  반영: `docs/concepts/load-testing.md`

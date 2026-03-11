# 지식 인덱스

## 핵심 용어
- `replication log`: leader가 follower에게 전달할 mutation의 순서화된 기록입니다.
- `offset`: log 안에서 entry의 순서를 나타내는 번호입니다.
- `watermark`: follower가 어디까지 적용했는지 나타내는 위치입니다.
- `idempotence`: 같은 entry를 다시 적용해도 결과가 바뀌지 않는 성질입니다.
- `log shipping`: leader가 follower에 변경분을 보내는 복제 방식입니다.

## 다시 볼 파일
- `../src/leader_follower/core.py`: log append, follower apply, watermark 기반 incremental sync가 한 파일 안에서 이어집니다.
- `../src/leader_follower/__main__.py`: delete 이후 follower value와 watermark를 바로 확인하는 데모 진입점입니다.
- `../tests/test_replication.py`: offset 부여, follower idempotence, incremental delete replication을 검증합니다.
- `../docs/concepts/log-shipping.md`: leader가 follower에 어떤 단위로 log를 보내는지 먼저 복기할 때 좋습니다.

## 개념 문서
- `../docs/concepts/idempotent-follower.md`: 중복 로그 적용에도 follower 상태가 어긋나지 않아야 하는 이유를 설명합니다.
- `../docs/concepts/log-shipping.md`: leader가 offset과 watermark를 기준으로 follower에 변경분을 보내는 방식을 정리합니다.

## 검증 앵커
- 확인일: 2026-03-11
- 테스트 파일: `../tests/test_replication.py`
- 다시 돌릴 테스트 이름: `test_replication_log_assigns_sequential_offsets`, `test_follower_apply_is_idempotent`, `test_replicate_once_incremental_and_deletes`
- 데모 경로: `../src/leader_follower/__main__.py`
- 데모가 보여 주는 장면: `alpha` 삭제 후 적용된 entry 수와 follower value를 dict로 보여 줍니다.
- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 읽을 때 바로 필요한 정보만 남깁니다.

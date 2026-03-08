# Replicated Write Pipeline

write pipeline은 다음 순서를 따른다.

1. key를 shard로 라우팅한다.
2. shard leader의 local store가 operation을 append-only log에 기록한다.
3. follower는 자신의 watermark 이후 entry만 받아 적용한다.
4. routed read는 leader 또는 최신 follower에서 수행할 수 있다.

이 구현은 network transport 대신 in-process orchestration을 사용하지만, write ordering, catch-up, disk-backed replay라는 핵심 의미는 그대로 유지한다.

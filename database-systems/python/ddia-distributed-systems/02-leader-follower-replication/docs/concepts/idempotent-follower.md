# Idempotent Follower

실제 복제에서는 같은 entry batch가 재전송될 수 있다. follower가 `offset <= current_watermark`인 entry를 다시 적용하지 않도록 만들면 replay가 안전해진다.

이 프로젝트의 follower는 `lastAppliedOffset`를 유지하고, 더 낮거나 같은 offset의 entry는 건너뛴다. 그래서 같은 batch를 두 번 받아도 결과 상태와 watermark가 바뀌지 않는다.

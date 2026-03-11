# Log Shipping

leader-follower 복제의 핵심은 "store state 자체"보다 "state를 만든 ordered mutation stream"을 보내는 것이다. follower는 leader의 현재 key-value map을 통째로 받지 않고, 자신이 마지막으로 적용한 offset 이후의 entry만 가져온다.

이 모델의 장점은 다음과 같다.

- follower가 중간에 끊겨도 watermark부터 다시 이어갈 수 있다
- delete도 일반 mutation과 같은 방식으로 복제된다
- replay 의미가 명확해 테스트가 단순해진다

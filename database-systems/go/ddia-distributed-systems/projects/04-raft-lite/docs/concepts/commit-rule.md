# Commit Rule

leader는 단순히 local append 했다고 commit하지 않는다. 현재 term의 entry가 과반수 노드에 replicate 되었을 때만 `commitIndex`를 올린다.

이 규칙은 예전 term의 불완전한 entry를 잘못 commit하는 것을 막는다. 구현에서는 각 follower의 `matchIndex`를 보고 가장 높은 다수결 index를 찾는다.

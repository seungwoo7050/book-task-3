# 10 범위를 다시 좁히기

`08-btree-index-and-query-scan`에서 제일 먼저 확인한 건 파일 이름보다 경계였다. `internal/btreeindex`는 split과 cursor만 책임지고, `internal/queryscan`은 planner와 row collection만 책임진다.

## 이번 단계에서 바로 보인 것

- split과 duplicate key lookup이 한 패키지에 묶여 있다.
- planner는 `index-point-lookup`, `index-range-scan`, `full-scan` 세 전략만 돌려준다.
- CLI는 세 전략이 실제로 언제 쓰이는지 바로 보여 준다.

이렇게 표면을 줄여 두면 B+Tree와 query executor를 한 프로젝트 안에서 다뤄도 과하게 커지지 않는다.

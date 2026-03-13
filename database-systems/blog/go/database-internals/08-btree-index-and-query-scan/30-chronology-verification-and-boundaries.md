# 30 검증과 경계

테스트는 split 이후 point lookup, duplicate key lookup, ordered range scan, planner fallback을 각각 고정한다. demo는 같은 내용을 사람 눈으로 다시 확인하는 표면이다.

이번 단계에서 아직 없는 것은 MVCC, delete merge, cost-based optimizer다. 그래서 이 lab은 "query execution 입문"이지 "mini SQL engine"은 아니다.

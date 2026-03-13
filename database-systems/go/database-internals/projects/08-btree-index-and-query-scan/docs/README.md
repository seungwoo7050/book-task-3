# BTree Index And Query Scan Notes

## 이 문서 묶음의 역할

이 폴더는 이번 lab의 두 축만 잡는다. 하나는 B+Tree split이 leaf order를 어떻게 유지하는가이고, 다른 하나는 range cursor와 작은 planner가 query surface를 어떻게 결정하는가다.

## 문서 목록

- `concepts/b-plus-tree-page-splits.md`: leaf split과 separator key가 왜 필요한가
- `concepts/range-cursor-and-rule-based-planner.md`: range cursor와 planner가 어떤 약속을 고정하는가
- `references/README.md`: 다시 읽을 자료

## 어디까지 다루나

- B+Tree leaf / internal split
- duplicate key lookup
- linked-leaf range scan
- rule-based planner

## 일부러 다루지 않는 것

- delete merge
- cost-based optimizer
- MVCC visibility

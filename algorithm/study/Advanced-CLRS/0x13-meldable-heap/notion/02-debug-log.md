# 0x13 Meldable Heap — 디버깅 기록

## sibling 초기화

merge 시 sibling 포인터를 None으로 끊지 않으면 merge_pairs에서 무한 루프. `a.sibling = b.sibling = None` 필수.

## 테스트

```bash
make -C problem test
```

PASS.

# 0x12 Red-Black Tree — 디버깅 기록

## Sentinel 초기화

`self.nil = Node(0)` → color=BLACK. 모든 leaf와 부모 없는 포인터가 nil을 가리켜야 경계 조건 단순화.

## fixup 대칭 처리

`if z.parent == z.parent.parent.left:` 와 대칭 else 블록. 코드 길지만 논리는 mirror.

## 테스트

```bash
make -C problem test
```

PASS. INORDER 결과로 정렬 우검증.

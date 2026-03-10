# 0x15 String Matching — 회고

## 배운 것

- KMP: 결정론적, 최악 $O(n+m)$ 보장. prefix function이 핵심 전처리.
- Rabin-Karp: 기대 $O(n+m)$, 해시 충돌 시 최악 $O(nm)$. 다중 패턴 검색에 유리.
- 두 알고리즘의 트레이드오프: KMP는 단일 패턴에 안정적, Rabin-Karp는 다중 패턴/2D 매칭에 확장성.

## 실무 연결

`grep -F`는 Aho-Corasick (KMP 확장), `grep -E`는 NFA/DFA. Rabin-Karp는 plagiarism detection에 활용.

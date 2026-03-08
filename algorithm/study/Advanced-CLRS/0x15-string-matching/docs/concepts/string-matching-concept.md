# Prefix Function and Rolling Hash

## CLRS Connection

CLRS Ch 32 compares finite-automaton style matching, KMP prefix fallback, and Rabin-Karp fingerprinting.

## Study Notes

- KMP는 deterministic fallback으로 O(n + m)을 보장한다.
- Rabin-Karp는 hash collision check를 포함하지만 여러 패턴이나 streaming 상황에서 직관적이다.
- 동일한 input/output contract로 두 알고리즘을 바꾸어 실행하면 trade-off가 선명해진다.

# Meld First

## CLRS Connection

CLRS Ch 19 motivates special heaps because meld and decrease-key matter more than raw insertion speed in graph algorithms.

## Study Notes

- pairing heap은 Fibonacci heap보다 단순하지만 meld가 매우 자연스럽다.
- named heaps interface로 meld semantics를 fixture에서 바로 검증할 수 있다.
- 이후 Fibonacci heap을 읽을 때 root list와 lazy consolidation 아이디어를 비교 대상으로 삼는다.

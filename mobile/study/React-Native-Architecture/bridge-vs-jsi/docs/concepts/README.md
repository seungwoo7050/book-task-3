# Concepts

- RN 0.84에서는 old/new runtime 전환보다 JS surface 차이를 비교하는 편이 실용적이다.
- async serialized payload는 queue hop과 object shape 비용을 드러낸다.
- sync direct-call surface는 blocking cost와 빠른 응답을 동시에 보여 준다.

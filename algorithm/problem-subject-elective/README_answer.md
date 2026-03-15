# algorithm 비필수 답안지

이 문서는 핵심 경로를 지난 뒤 들어가는 `Advanced-CLRS` 트랙을 실제 실험 코드 기준으로 정리한 답안지다. 이 구간의 가치는 “이론을 읽었다”가 아니라 “proof-heavy 주제를 검증 가능한 프로그램으로 재구성했다”는 데 있다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [advanced-clrs-python](advanced-clrs-python_answer.md) | 시작 위치의 구현을 완성해 주제: NP-완전성 실습, 학습 초점: 이론 중심 알고리즘을 작은 실험과 검증 가능한 입출력 문제로 재구성하는 연습, canonical fixture는 data/input*.txt, data/output*.txt에 둔다를 한 흐름으로 설명하고 검증한다. 핵심은 verify_vc와 verify_3sat, solve 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/algorithm/study/Advanced-CLRS/0x18-np-completeness-lab/problem test` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.

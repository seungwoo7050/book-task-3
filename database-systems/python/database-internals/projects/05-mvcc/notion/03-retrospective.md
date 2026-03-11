# 회고

## 왜 이 프로젝트가 재현성에 특히 좋은가
- 구현이 한 파일에 모여 있어 추적 경로가 짧습니다.
- 테스트 이름만 읽어도 어떤 규칙이 있는지 거의 드러납니다.
- 복잡한 인프라 없이도 transaction visibility의 핵심을 직접 손으로 따라갈 수 있습니다.

## 이번 단계에서 명확해진 것
- MVCC의 핵심은 자료구조보다 visibility rule입니다.
- read-your-own-write, snapshot isolation, first-committer-wins는 서로 다른 규칙이지만 하나의 version chain 위에서 함께 설명할 수 있습니다.
- GC는 메모리 최적화 이전에 “누구의 snapshot도 깨지지 않게 지우는 일”이라는 점이 더 중요합니다.

## 아직 단순화한 부분
- disk persistence가 없어 version chain은 메모리 모델에 머뭅니다.
- predicate read와 phantom 문제는 다루지 않습니다.
- serializable isolation이나 write skew까지는 들어가지 않습니다.

## 다음에 확장한다면
- version chain을 실제 저장 엔진 위로 내려 persistence와 연결할 수 있습니다.
- range scan과 secondary index를 붙여 phantom 문제를 다룰 수 있습니다.
- 다른 isolation level과 비교해 “왜 snapshot isolation을 택했는가”를 더 분명히 할 수 있습니다.

## 다음 단계로 넘길 질문
- 분산 환경에서 각 replica는 어떤 snapshot을 기준으로 읽기를 제공해야 할까?
- leader-follower replication과 MVCC를 연결하면 conflict detection 경계는 어디에 두어야 할까?

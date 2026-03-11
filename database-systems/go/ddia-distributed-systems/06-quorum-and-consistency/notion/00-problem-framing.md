# 문제 프레이밍

## 왜 이 프로젝트를 하는가
replication만 배우면 “복제는 되는데 어떤 값을 최신이라고 믿을 것인가”가 비어 있습니다. 이 단계는 quorum overlap을 작은 register 실험으로 분리해 consistency trade-off를 먼저 눈에 보이게 만듭니다.

## 커리큘럼 안에서의 위치
- 트랙: DDIA Distributed Systems / Go
- 이전 단계: 05 Clustered KV Capstone
- 다음 단계: 07 Heartbeat and Leader Election
- 지금 답하려는 질문: 일부 replica가 뒤처진 상태에서 read는 어떤 조건일 때 최신값을 볼 수 있는가?

## 이번 구현에서 성공으로 보는 것
- `W + R > N`이면 최신 version이 읽혀야 합니다.
- `W + R <= N`이면 stale read가 재현돼야 합니다.
- write quorum 실패 시 version이 전진하면 안 됩니다.
- read는 어떤 replica가 응답했는지 함께 돌려줘야 합니다.

## 의도적으로 남겨 둔 범위 밖 항목
- read repair, hinted handoff, anti-entropy는 없습니다.
- concurrent write merge도 없습니다.
- failure detector와 leader election은 다음 단계로 넘깁니다.

# 20 핵심 invariant

이번 프로젝트의 핵심 invariant는 세 가지다.

1. leaf entry는 항상 key 오름차순이어야 한다.
2. separator key는 오른쪽 child의 첫 key여야 한다.
3. range cursor는 sibling leaf로 넘어가도 key order를 깨면 안 된다.

이 세 가지가 동시에 맞아야 split 이후 lookup과 range scan이 모두 살아남는다. 여기에 duplicate key row id list가 얹히면서 secondary index가 비로소 query executor와 연결된다.

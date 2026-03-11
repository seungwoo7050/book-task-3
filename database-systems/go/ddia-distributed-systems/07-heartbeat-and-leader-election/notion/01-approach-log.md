# 접근 로그

## 1. heartbeat와 election을 한 파일에 묶었습니다
이번 단계의 질문은 authority 교체 하나뿐이라서, failure detector와 election을 같은 `Node` 안에서 읽히게 두었습니다.

## 2. suspicion tick을 일부러 따로 뒀습니다
`silence >= suspicionTTL`과 `silence >= electionTTL`을 분리해, 데모에서 “의심”과 “선출” 사이에 한 장면이 생기도록 했습니다.

## 3. log rule은 전부 뺐습니다
majority vote와 higher term step-down만 남겨서, Raft-lite보다 작은 모델이라는 사실이 코드에서도 드러나게 했습니다.

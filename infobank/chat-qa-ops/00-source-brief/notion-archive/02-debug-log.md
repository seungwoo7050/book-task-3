# Source Brief — 디버깅 기록: 코드 없는 stage에서 뭘 디버깅하나

## "디버깅할 게 있나?"

Source brief는 실행 코드가 거의 없다. dataclass 하나와 상수 tuple 하나가 전부다.
그래서 처음에는 "이 stage에 debug log가 필요한가?"라고 생각했다.

하지만 실제로 부딪힌 문제가 있었다.

## Case: stack 설명이 문서마다 조금씩 달라질 위험

### 증상

stage 07에서 React dashboard를 만들고 있었는데, README에는 "FastAPI + React"라고 써 있고, 다른 문서에서는 "Vite"나 "PostgreSQL"이 빠져 있었다.
사소해 보이지만, 나중에 "이 프로젝트에서 PostgreSQL을 쓰나요?"라는 질문에 한 문서는 "쓴다", 다른 문서는 "안 나온다"가 되면 혼란이 생긴다.

### 원인

Python 버전(3.12)과 backend/frontend 주력 기술이 **코드가 아니라 서술에만** 존재했다.
서술은 복사-붙여넣기 과정에서 자연스럽게 변형된다.

### 해결

`SourceBrief` dataclass에 Python 3.12, FastAPI, React, PostgreSQL, Langfuse를 **명시적으로 나열**하고, 테스트에서 `"FastAPI" in brief.primary_stack`을 검증하도록 만들었다.

### 검증

`python/tests/test_source_brief.py`가 stack membership과 baseline version을 고정한다.
이후 누군가 stack 목록을 바꾸면 테스트가 깨지므로, 의도적인 변경만 통과한다.

## 이 경험에서 배운 것

코드가 아닌 stage에서도 "정보가 여러 곳에 흩어지면 drift가 생긴다"는 문제는 동일하게 발생한다.
그리고 그 drift를 잡는 가장 확실한 방법은, 서술 대신 **한 곳에서 정의하고 테스트로 잠그는 것**이다.

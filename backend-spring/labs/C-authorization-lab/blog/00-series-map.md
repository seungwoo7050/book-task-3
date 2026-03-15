# C-authorization-lab series map

이 시리즈는 "인가를 설명한다"와 "인가를 실제로 강제한다" 사이의 거리를 보여 준다. `C-authorization-lab`의 코드는 organization 생성, invite, accept, role 변경이라는 membership lifecycle은 갖췄지만, 아직 인증된 actor나 method security, durable membership store는 없다.

## 읽는 순서

1. [10-development-timeline.md](10-development-timeline.md)
   membership 흐름을 먼저 만들고, 그다음에 무엇이 비어 있는지까지 확인한 과정을 따라간다.

## 이 시리즈가 답하는 질문

- authorization을 role 이름이 아니라 membership lifecycle로 먼저 설명하면 무엇이 보이는가
- 현재 구현에서 owner check, actor identity, validation은 어디까지 비어 있는가
- scaffold 단계 authorization 문서를 쓸 때 어떤 검증 신호까지 같이 남겨야 하는가

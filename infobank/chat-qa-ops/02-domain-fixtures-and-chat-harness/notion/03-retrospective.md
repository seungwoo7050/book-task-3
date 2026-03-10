# 02-domain-fixtures-and-chat-harness 회고

## 이번 stage로 강화된 점

- fixture와 harness 경계가 분명해 회귀 입력을 버전 관리하기 쉽다.
- 사람이 읽을 수 있는 KB와 replay transcript를 유지한다.

## 아직 약한 부분

- 실제 고객 대화처럼 다중 턴 상태를 반영하지는 않는다.

## 학생이 여기서 바로 가져갈 것

- fixture와 harness를 섞지 않고, 입력 데이터와 검증 러너를 분리해서 관리하는 방식
- KB 문서, replay transcript, expected evidence를 함께 버전 관리하는 방식

## 다음 stage로 넘기는 자산

- seeded KB 설계
- deterministic replay harness
- expected evidence document 확인 방식

## 05-development-timeline.md와 같이 읽을 포인트

- 어떤 fixture가 최소 재현 세트인지 먼저 잡고, 그 뒤에 테스트를 실행한다.
- capstone으로 내려가기 전에 stage 입력셋이 어떤 상담 실패를 재현하려는지 문서와 데이터에서 같이 확인한다.

## 나중에 다시 볼 것

- 추후 replay fixture를 YAML까지 확장하면 capstone의 richer metadata를 더 잘 반영할 수 있다.

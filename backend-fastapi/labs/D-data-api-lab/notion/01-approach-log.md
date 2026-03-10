# 접근 로그

## 고려한 선택지

- hard delete 중심 모델
- soft delete + include_deleted 모델
- cursor pagination
- page-based pagination
- DB 잠금 중심 충돌 처리
- version 필드 중심 optimistic locking

## 채택한 방향

- 삭제는 `deleted_at` 기반 soft delete로 유지했다.
- 페이지네이션은 page-based 모델로 단순화했다.
- 수정 충돌은 version 필드로 감지하는 optimistic locking을 채택했다.
- 엔드포인트에서 ORM을 직접 다루기보다 서비스 계층에 규칙을 모았다.

## 버린 대안

- cursor pagination은 교육적 대비 효과보다 구현 비용이 커서 이번 랩에서는 제외했다.
- hard delete는 복구 가능성과 목록 정책을 설명하기 어려워 채택하지 않았다.

## 트레이드오프

- 장점: CRUD 예제를 넘어서 현실적인 데이터 설계 질문을 같이 다룰 수 있다.
- 단점: 인증/인가가 없어서 실제 제품 맥락은 일부러 비워 두어야 한다.

이런 선택은 작은 예제에서도 "데이터 API는 엔드포인트 모음이 아니라 규칙의 집합"이라는 설명을 가능하게 만든다.

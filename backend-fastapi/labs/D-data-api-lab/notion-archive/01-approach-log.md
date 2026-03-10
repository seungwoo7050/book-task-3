# Approach Log

## 기본 CRUD를 넘어서: 무엇을 보여줄 것인가

모든 웹 프레임워크 튜토리얼이 CRUD를 다루지만, 대부분은 "create → read → update → delete"를 일직선으로 보여주고 끝난다. 이 랩에서는 CRUD를 기본 뼈대로 놓되, 실무에서 반드시 처리해야 하는 다섯 가지 관심사를 의도적으로 포함했다.

**왜 page-based pagination인가?** Cursor pagination이 대규모 데이터셋에서 성능상 유리하다는 것은 알지만, 먼저 "페이지네이션이란 무엇이며 왜 필요한가"를 명확히 하는 것이 우선이다. page/page_size → OFFSET/LIMIT → total count의 변환이 명시적으로 보여야 나중에 cursor의 장점도 설명할 수 있다.

**왜 optimistic locking인가?** 이 랩에서 가장 실무적인 가치가 있는 주제다. 두 명의 개발자가 같은 프로젝트의 상태를 동시에 바꾸려 할 때, 마지막 기록이 무조건 이기는 것(last-write-wins)은 데이터 손실이다. version 필드를 도입하면 "당신이 읽은 이후 누군가 변경했으니 다시 확인하라"는 409를 돌려줄 수 있다.

**왜 soft delete인가?** 물리 삭제(DELETE FROM)는 되돌릴 수 없다. `deleted_at` 타임스탬프를 찍으면 "삭제된 것처럼 보이지만 데이터는 남아있어서" 감사 추적이나 복구가 가능하다. 동시에 모든 읽기 쿼리에 `WHERE deleted_at IS NULL` 조건이 필요해지는 비용이 있다.

## 세 모델 간의 관계

Project → Task → Comment의 계층 구조를 택한 이유는 aggregate boundary를 보여주기 위해서다. Task는 반드시 Project에 속해야 하고, Comment는 반드시 Task에 속해야 한다. FK에 `ondelete="CASCADE"`를 설정하여 부모가 삭제되면 자식도 함께 사라진다.

하지만 soft delete에서는 이 cascade가 자동으로 작동하지 않는다. Project를 soft delete해도 하위 Task의 deleted_at은 바뀌지 않는다—대신 service layer에서 soft-deleted 프로젝트에 새 Task를 생성하지 못하게 막는다. 이 불일치는 의도적으로 남겨둔 학습 포인트다.

## Repository 패턴과 쿼리 분리

`DataRepository`에 list/get 쿼리를 분리한 이유는, 서비스 계층이 SQL 문을 직접 조립하지 않게 하기 위해서다. `list_projects`에서 status 필터, deleted_at 필터, 정렬, 페이지네이션 로직이 모두 repository 안에 있고, 서비스는 그 결과(items, total)만 받는다.

## 기각된 방향

- **인증 포함**: 데이터 접근 패턴이 보안 로직에 묻힌다.
- **Single-table CRUD**: relation과 aggregate boundary가 보이지 않는다.
- **Cursor pagination**: 더 복잡한 개념이므로 먼저 기본 개념을 확립한 뒤 비교하는 것이 낫다.

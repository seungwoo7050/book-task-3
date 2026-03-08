# Core Concepts

## 핵심 개념

- store는 레코드 바이트를 순차 append하는 역할이다.
- index는 logical offset을 물리 위치로 빠르게 찾기 위한 보조 구조다.
- segment는 store와 index를 묶은 관리 단위다.
- log는 여러 segment를 회전시키며 append-only 추상화를 제공한다.

## Trade-offs

- mmap index는 빠르지만 운영체제 의존성과 자원 정리 규칙을 같이 이해해야 한다.
- replication을 빼면 범위는 줄지만 “분산”이라는 이름이 다소 강하게 들릴 수 있다.

## 실패하기 쉬운 지점

- reopen 시 base offset과 파일 포인터 복원이 틀리면 테스트는 간헐적으로 깨질 수 있다.
- truncate/reset 시 store와 index를 같이 정리하지 않으면 논리적 오염이 남는다.


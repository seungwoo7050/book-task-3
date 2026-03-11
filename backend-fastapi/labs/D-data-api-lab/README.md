# D-data-api-lab

데이터 중심 백엔드 API를 어떻게 구조화할지 연습하는 랩입니다. CRUD 자체보다도 필터링, 정렬, 소프트 삭제, 낙관적 락처럼 시간이 지나도 설명 가치가 남는 설계 포인트에 집중합니다.

## 문제 요약

- 프로젝트, 태스크, 댓글을 다루는 데이터 중심 API를 만든다고 가정합니다. 단순 CRUD를 넘어서, 목록 조회 조건, 삭제 정책, 동시 수정 충돌 같은 현실적인 데이터 API 문제를 같이 다뤄야 합니다.
- 세 가지 핵심 엔터티의 생성, 조회, 수정, 삭제가 가능해야 합니다.
- 필터링, 정렬, 페이지네이션이 일관된 형태로 노출되어야 합니다.
- 상세 성공 기준과 제외 범위는 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- projects / tasks / comments CRUD
- 목록 조회용 query parameter
- 버전 필드 기반 충돌 감지
- health endpoint

## 핵심 설계 선택

- 프로젝트, 태스크, 댓글 API 설계
- 서비스 계층과 ORM 경계 정리
- 필터링, 정렬, 페이지 기반 페이지네이션
- 인증/인가를 붙이지 않고 데이터 경계에 집중합니다.
- 페이지네이션은 cursor 대신 page-based 모델로 유지합니다.

## 검증

```bash
make lint
make test
make smoke
docker compose up --build
```

- 실행과 환경 설명은 [fastapi/README.md](fastapi/README.md)에서 다룹니다.
- 마지막 기록된 실제 검증 결과는 [../../docs/verification-report.md](../../docs/verification-report.md)에 있습니다.

## 제외 범위

- 인증과 인가
- 전문 검색이나 대규모 인덱싱
- 복잡한 이벤트 소싱이나 CQRS

## 다음 랩 또는 비교 대상

- 다음 단계는 [E-async-jobs-lab](../E-async-jobs-lab/README.md)입니다.
- 설계 설명은 [docs/README.md](docs/README.md), 학습 로그는 [notion/README.md](notion/README.md), 실행 진입점은 [fastapi/README.md](fastapi/README.md)에서 읽습니다.

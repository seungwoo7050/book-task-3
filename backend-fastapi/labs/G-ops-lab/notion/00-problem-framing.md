# 문제 프레이밍

## 학습 목표

운영성을 "기능이 다 끝난 뒤 붙이는 부가 요소"가 아니라 독립된 백엔드 주제로 이해하는 것이 목표다. health check, metrics, 구조화 로그, CI, 배포 문서를 최소 단위로 다룬다.

## 왜 중요한가

- 서비스가 살아 있는지, 준비되었는지, 어디서 실패하는지 모르면 기능만으로는 운영할 수 없다.
- 운영 문서 역시 코드처럼 공개 레포에서 설명 가치가 큰 자산이다.

## 선수 지식

- FastAPI 애플리케이션 수명주기
- Docker Compose 기본
- health check와 readiness 개념

## 성공 기준

- live / ready endpoint를 구분해 설명할 수 있어야 한다.
- 최소 metrics surface와 구조화 로그를 노출해야 한다.
- CI와 Compose probe가 어떤 수준까지 검증하는지 분명해야 한다.
- AWS 문서는 target shape일 뿐 실제 배포 완료가 아님을 명확히 적어야 한다.

## 제외 범위

- full observability stack
- IaC 기반 실제 배포 자동화
- 장시간 부하와 장애 주입 실험

이 랩은 "운영성도 기능이다"라는 관점을 만드는 데 초점이 있다. 그래서 실제 배포 자동화보다 health, metrics, 문서화된 가정이 먼저 등장한다.

# 문제 정의

## 문제

기능은 단순해도, 백엔드가 어떻게 살아 있는지 확인하고 어떻게 배포 가정을 설명할지 정리해야 합니다. health check, readiness, metrics, CI, 배포 문서는 개발용 API와 별개의 운영성 문제입니다.

## 성공 기준

- live / ready health endpoint가 구분되어야 합니다.
- 요청 수 같은 최소 metrics surface가 있어야 합니다.
- 로컬 Compose 부팅과 CI 명령이 정리되어야 합니다.
- AWS target shape가 실제 배포 완료처럼 과장되지 않고 문서로 설명되어야 합니다.

## 제외 범위

- 풀 observability stack 구축
- IaC로 실제 인프라를 생성하는 자동화
- 장시간 부하 테스트와 장애 주입 실험

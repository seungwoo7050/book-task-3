# 02 Capstone blog

이 트랙의 블로그는 앞선 아홉 개 프로젝트의 결과를 하나의 local control plane으로 묶는 과정을 실제 API, worker, DB, demo 산출물 기준으로 다시 읽습니다.

## 이 트랙이 다루는 질문

- 개별 스캐너를 어떤 API와 worker 경계로 묶어야 하는가
- finding, exception, remediation, report를 어떤 상태 저장소와 흐름으로 연결해야 하는가
- local demo가 어느 정도까지 end-to-end 검증을 대신할 수 있는가

## 프로젝트 인덱스

1. [10 Cloud Security Control Plane](10-cloud-security-control-plane/00-series-map.md)

## 권장 읽기 순서

1. `00-series-map.md`에서 캡스톤이 통합하는 입력과 레이어를 먼저 확인합니다.
2. `10-chronology-inputs-and-api-surface.md`에서 공개 표면과 입력 경계를 따라갑니다.
3. `20-chronology-workers-state-and-reporting.md`에서 DB, worker, suppression, remediation, report를 읽습니다.
4. `30-chronology-demo-verification-and-boundaries.md`에서 end-to-end 테스트와 demo 산출물, 의도적 한계를 정리합니다.

## 공통 검증 경로

```bash
make test-capstone
make demo-capstone
```

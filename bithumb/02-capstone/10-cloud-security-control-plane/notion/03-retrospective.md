# 회고

## 이 프로젝트가 실제로 증명한 것

- 이 프로젝트는 앞선 아홉 개 프로젝트가 별개의 연습문제가 아니라, 하나의 운영 흐름 안에서 재사용 가능한 building block이었다는 점을 분명히 증명했습니다.
- FastAPI API, worker, DB, lake, report를 분리해 두면 scan request 처리, CloudTrail ingestion, K8s ingestion, exception, remediation, report export를 같은 서비스 안에서 반복 재현할 수 있습니다.
- SQLite fallback을 유지한 덕분에 Docker/PostgreSQL이 없는 환경에서도 demo-capstone 흐름을 끝까지 따라갈 수 있게 되었습니다.

## 이번 버전이 의도적으로 단순화한 것

- 인증/인가, 멀티테넌시, 외부 큐, migration tool, 운영 모니터링은 최소 수준이거나 비어 있습니다.
- 실제 AWS API와 live cloud state를 읽지 않고 fixture 기반으로만 동작합니다.
- worker는 프로세스 내부 함수 호출에 가깝고, 분산 처리 환경까지는 확장하지 않았습니다.

## 학습자가 여기서 반드시 가져가야 할 판단

- 학습자 관점에서 가장 중요한 것은 캡스톤 자체의 화려함보다, 앞선 작은 엔진들이 정확히 어디서 재사용되는지를 추적하는 일입니다.
- 이 capstone의 성공 기준은 배포가 아니라 end-to-end 흐름을 repeatable하게 재현하고, 그 결과를 markdown report로 남길 수 있는지에 있습니다.
- 테스트와 데모를 분리해 둔 이유는 검증과 설명의 역할이 다르기 때문입니다. 테스트는 자동 검증, 데모는 사람이 읽는 증거 수집을 담당합니다.

## 공개 기록으로 확장할 때 보강할 증거

- 공개용 문서에서는 `processed_jobs == 2`, findings 6건 이상, report에 `## Findings`가 포함된다는 세 근거를 함께 제시하는 것이 좋습니다.
- demo asset 디렉터리에 생성되는 `01`~`08` 파일을 보여 주면, 단순 성공 메시지보다 훨씬 강한 재현 증거가 됩니다.
- SQLite fallback과 PostgreSQL 경로를 같이 설명하면 학습용 레포에서 “완전한 재현성”을 어떻게 확보했는지 더 설득력 있게 보여 줄 수 있습니다.

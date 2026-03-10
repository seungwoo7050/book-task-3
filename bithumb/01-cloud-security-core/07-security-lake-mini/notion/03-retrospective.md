# 회고

## 이 프로젝트가 실제로 증명한 것

- 이 프로젝트는 정규화된 로그가 있어야 detection engineering이 시작된다는 점을 분명히 증명했습니다.
- CloudTrail suspicious fixture 하나만으로도 다섯 개 alert를 재현할 수 있어, lake 개념을 지나치게 큰 인프라 없이도 학습할 수 있음을 보여 줍니다.
- Parquet 산출물을 남기면서 즉시 query 결과를 확인하는 구조는 이후 capstone ingestion 흐름의 좋은 축소판이 됩니다.

## 이번 버전이 의도적으로 단순화한 것

- multi-source correlation, time window tuning, triage priority, suppression baseline 같은 운영형 탐지 요소는 제외했습니다.
- query는 코드 안에 고정돼 있고 외부 룰셋으로 관리되지 않습니다.
- 실제 alert delivery, notification, SIEM integration은 아직 없습니다.

## 학습자가 여기서 반드시 가져가야 할 판단

- 학습자에게 중요한 것은 alert 수를 외우는 것이 아니라, 어떤 event pattern이 어떤 control_id로 이어지는지 설명하는 능력입니다.
- 정규화와 detection을 별도 프로젝트로 나눈 이유는, 적재 문제와 규칙 문제를 섞지 않기 위해서입니다.
- 이 프로젝트의 성공 기준은 복잡한 lake 아키텍처 소개가 아니라, 작은 fixture에서 repeatable detection이 가능하다는 사실을 보여 주는 데 있습니다.

## 공개 기록으로 확장할 때 보강할 증거

- 공개용 문서로 옮길 때는 `LAKE-001`부터 `LAKE-005`까지 각 control이 어떤 행위를 잡는지 한 줄씩 적어 두는 편이 좋습니다.
- Parquet 파일 생성 여부와 alert 목록을 함께 제시하면, 적재와 탐지가 같은 흐름 안에 있음을 더 쉽게 보여 줄 수 있습니다.
- capstone으로 연결할 때는 “query가 API 뒤로 들어간다”는 점보다 “같은 suspicious fixture가 다시 사용된다”는 점을 강조하는 편이 더 실효적입니다.

# 회고

## 이 프로젝트가 실제로 증명한 것

- 이 프로젝트는 CSPM의 핵심이 “클라우드 설정을 사람이 대신 읽어 주는 규칙 집합”이라는 점을 매우 작은 코드로 증명했습니다.
- Terraform plan과 access key snapshot이라는 서로 다른 입력을 같은 finding 모델로 묶어, 정적 misconfiguration과 운영 상태 문제를 같은 triage 흐름에 올릴 수 있음을 보여 줍니다.
- 특히 secure fixture에서 0건이 나와야 한다는 기준을 테스트로 고정해, rule 엔진 품질은 검출 건수보다 precision에 더 크게 좌우된다는 점을 분명히 했습니다.

## 이번 버전이 의도적으로 단순화한 것

- 현재 rule 수는 네 개이고, 리소스 타입도 S3, security group, encryption, access key age 정도로 제한돼 있습니다.
- benchmark 매핑, exception baseline, suppression logic, 외부 rule registry는 아직 없습니다.
- severity와 title은 학습용으로 충분한 수준으로 단순화돼 있어, 운영형 CSPM 제품처럼 방대한 메타데이터를 담지는 않습니다.

## 학습자가 여기서 반드시 가져가야 할 판단

- 학습자에게 가장 중요한 포인트는 insecure 입력에서 finding이 많이 나오는 장면보다, secure 입력에서 왜 아무것도 나오지 않는지를 설명하는 장면입니다.
- CSPM rule은 단순 문자열 검색이 아니라, 입력 구조를 해석하고 `control_id`를 안정적으로 붙이는 데이터 모델링 작업이라는 점을 의식해야 합니다.
- 이 프로젝트는 뒤의 remediation과 control plane 통합을 염두에 두고 있으므로, 출력에 사람이 읽을 summary와 시스템이 읽을 control_id가 같이 있어야 합니다.

## 공개 기록으로 확장할 때 보강할 증거

- 공개용 문서에서는 insecure plan 한 장만 보여 주지 말고, secure fixture가 0건을 보장하는 테스트 이름을 반드시 같이 적어야 합니다.
- `CSPM-001`부터 `CSPM-004`까지 각 control이 어떤 운영 질문을 대신하는지 표로 설명하면 문서 밀도가 크게 올라갑니다.
- `06-remediation-pack-runner`가 같은 finding을 받아 dry-run plan을 만드는 장면을 연결하면, rule이 단순 탐지로 끝나지 않는다는 점을 더 잘 보여 줄 수 있습니다.

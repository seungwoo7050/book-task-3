# 회고

## 이 프로젝트가 실제로 증명한 것

- 이 프로젝트는 보안 자동화의 핵심이 “자동으로 고친다”가 아니라 “안전하게 제안하고 승인 단계를 분리한다”는 점을 증명했습니다.
- finding 하나를 받아 remediation plan으로 변환하는 과정에서 mode, status, summary, patch 초안을 함께 관리해야 운영 흐름으로 확장할 수 있음을 보여 줍니다.
- 테스트는 public access finding 하나만으로도 auto patch 제안과 approval 전이를 재현할 수 있다는 점을 확인합니다.

## 이번 버전이 의도적으로 단순화한 것

- rollback plan, change window, owner resolution, 배치 처리 같은 운영형 기능은 아직 없습니다.
- 조치안은 구조화된 실행 엔진이 아니라 사람이 읽을 수 있는 문자열 리스트에 머뭅니다.
- 승인자는 단순 텍스트로만 기록되고, 권한 체계나 RBAC는 없습니다.

## 학습자가 여기서 반드시 가져가야 할 판단

- 학습자 입장에서는 patch를 많이 만드는 것보다, 어떤 경우에 승인 전 단계가 필요한지 설명하는 것이 훨씬 중요합니다.
- remediation 모델은 결국 예외 관리, audit, capstone worker 흐름과 연결되므로 status 전이를 별도 데이터로 남겨야 합니다.
- 이 프로젝트의 성공 기준은 실제 리소스를 바꾸는 것이 아니라, 사람이 검토 가능한 조치 계획을 일관된 구조로 생성하는 데 있습니다.

## 공개 기록으로 확장할 때 보강할 증거

- 공개용 문서에는 patch 라인 일부만 떼어 넣기보다, `mode`, `status`, `summary`를 한 번에 보여 주는 JSON 예시가 더 효과적입니다.
- 왜 `block_public_acls` 같은 문구가 들어가는지 control_id와 연결해 설명하면 뒤 프로젝트와의 연계가 선명해집니다.
- capstone의 remediation dry-run API가 이 프로젝트 결과를 어떻게 재사용하는지 함께 적으면 더 좋습니다.

# 접근 기록

## 핵심 선택

- Terraform plan과 운영 snapshot을 함께 읽게 했습니다. 그래야 CSPM이 정적 분석만이 아니라는 점이 드러납니다.
- S3 public access 플래그 네 개는 개별 finding이 아니라 하나의 “퍼블릭 차단 불완전” finding으로 묶었습니다.
- finding 구조는 IAM analyzer와 같은 형태를 유지해 뒤 단계 remediation과 control plane에서 재사용할 수 있게 했습니다.

## 버린 대안

- 화려한 rule DSL은 만들지 않았습니다. 학습 초점은 rule language가 아니라 입력 해석과 기준 설계입니다.
- 모든 리소스를 다루지 않고, 보안 차이가 선명한 리소스만 남겼습니다.
- plan만 읽는 방향으로 끝내지 않고 access key snapshot을 추가해 운영 상태 감각을 살렸습니다.

## 다음 프로젝트와의 연결

이 프로젝트가 잘 되면 finding은 “경고”가 아니라 remediation 후보가 됩니다. 그래서 `06-remediation-pack-runner`는
여기서 나온 control_id를 그대로 받아 조치 계획을 만듭니다. 지금 단계에서 control 정의를 분명하게 잡는 이유가 여기에 있습니다.

## 다시 써도 유지할 기준

- 오탐보다 설명 가능성을 우선합니다.
- secure fixture에서 0건이 나오는 negative path를 꼭 유지합니다.
- 사람이 보고 바로 조치 방향을 떠올릴 수 있는 title이어야 합니다.

# 회고

## 이 프로젝트가 실제로 증명한 것

- 이 프로젝트는 컨테이너 보안 학습이 반드시 클러스터나 admission controller에서 시작될 필요가 없다는 점을 증명했습니다.
- manifest와 image metadata라는 두 입력을 결합하면 runtime 이전 단계에서 이미 많은 guardrail 위반을 설명할 수 있음을 보여 줍니다.
- secure fixture가 빈 결과를 보장해야 scanner가 단순 공포 생성기가 아니라는 점도 함께 증명됩니다.

## 이번 버전이 의도적으로 단순화한 것

- RBAC, NetworkPolicy, PodSecurity Admission, CVE, SBOM, image layer 분석은 포함하지 않았습니다.
- Helm/Kustomize 렌더링이나 multi-document deployment orchestration도 다루지 않습니다.
- 현재는 manifest 구조와 image metadata에 보이는 위험만 해석합니다.

## 학습자가 여기서 반드시 가져가야 할 판단

- 학습 초반에는 cluster setup보다, 각 guardrail이 어떤 운영 사고로 이어지는지 설명하는 것이 더 중요합니다.
- manifest 검사와 image 검사 결과를 같은 finding 모델로 반환해야 뒤의 capstone 통합이 쉬워집니다.
- 이 프로젝트의 성공 기준은 룰을 많이 나열하는 것이 아니라, insecure와 secure fixture가 분명히 갈리는지 확인하는 데 있습니다.

## 공개 기록으로 확장할 때 보강할 증거

- 공개용 기록에서는 여덟 개 control을 보안 위험별로 묶어 설명하면 이해가 빨라집니다.
- manifest-only와 image-only finding을 구분한 이유를 적어 두면 데이터 모델링 의도가 더 잘 드러납니다.
- capstone에서 같은 scanner가 API 뒤로 들어가는 장면을 연결하면, 로컬 학습 코드가 통합 서비스로 이어지는 흐름을 보여 줄 수 있습니다.

# EKS 없이 컨테이너 보안 감각 잡기

## 왜 이 과제를 만들었나

클라우드 보안 직무에서 "컨테이너/EKS 보안 정책"은 단골 요구사항이다.
그런데 EKS 클러스터를 실제로 띄우려면 AWS 계정, VPC, IAM 역할 등이 필요하고,
비용도 든다. 학습 단계에서 그걸 전부 세팅하는 건 과도하다.

다행히, 컨테이너 보안의 상당 부분은 Kubernetes manifest와 이미지 메타데이터만 읽어도 잡을 수 있다.
`Pod`이나 `Deployment`의 YAML에 적힌 설정을 검사하는 것만으로도,
실제 운영에서 가장 흔하게 발견되는 위험 패턴을 대부분 탐지할 수 있다.

이 과제는 그 사실을 코드로 증명한다.

## 여덟 가지 탐지 규칙

manifest 검사와 이미지 메타데이터 검사를 합쳐서 여덟 가지 규칙을 만들었다.

### Kubernetes manifest 검사 (K8S-001 ~ K8S-005)

**K8S-001: hostPath 볼륨 사용**

컨테이너가 호스트 노드의 파일시스템에 직접 접근한다.
이건 컨테이너 격리를 무력화하는 설정이다.
공격자가 컨테이너를 탈취했을 때, hostPath를 통해 노드 전체에 접근할 수 있다.

**K8S-002: latest 태그 사용**

`image: nginx:latest`처럼 latest 태그를 사용하면,
언제 어떤 버전의 이미지가 실행되는지 추적할 수 없다.
보안 취약점이 있는 이미지로 자동 업데이트될 수도 있고,
재현 가능한 배포가 불가능해진다.

**K8S-003: privileged 컨테이너**

`securityContext.privileged: true`는 컨테이너에 호스트 커널의 거의 모든 권한을 부여한다.
실질적으로 컨테이너 격리가 없는 것과 같다.

**K8S-004: root로 실행**

`securityContext.runAsUser: 0`이거나 명시하지 않은 경우(기본값이 0),
컨테이너 프로세스가 root 권한으로 실행된다.
컨테이너 탈출 취약점이 있을 때, root 권한이면 호스트까지 장악당할 수 있다.

**K8S-005: ALL capabilities 추가**

`capabilities.add: ["ALL"]`은 Linux의 모든 capability를 컨테이너에 부여한다.
`privileged: true`와 비슷한 효과를 가진다.

### 이미지 메타데이터 검사 (IMG-001 ~ IMG-003)

**IMG-001**: 이미지가 latest 태그를 사용 (K8S-002와 같은 이유)
**IMG-002**: 이미지가 root로 실행되도록 설정
**IMG-003**: 이미지가 ALL capabilities를 요청

이미지 메타데이터는 manifest와 별도로 검사한다.
이미지 빌드 시점의 설정과 배포 시점의 설정이 다를 수 있기 때문이다.

## 설계 선택

### insecure/secure fixture를 두 쌍으로 만든 이유

과제 02(Terraform)와 같은 패턴이다.
insecure fixture에서 모든 규칙이 발동하고,
secure fixture에서 finding이 0개인 것을 확인하면,
규칙 엔진의 정확성을 양방향으로 검증할 수 있다.

### YAML 파싱에 PyYAML을 사용한 이유

Kubernetes manifest는 YAML 포맷이다.
`yaml.safe_load_all`을 사용하면 하나의 파일에 여러 document가 있어도 전부 파싱한다.
multi-document YAML은 K8s에서 흔하다 (여러 리소스를 하나의 파일에 선언).

`safe_load_all`의 `safe`가 중요하다.
`yaml.load`는 임의 Python 객체를 생성할 수 있어서 보안 위험이 있고,
`safe_load`는 기본 데이터 타입만 생성한다.

### Deployment의 template.spec을 읽는 이유

Kubernetes Deployment의 실제 컨테이너 설정은
`spec.template.spec.containers`에 있다.
직접 `spec.containers`가 아니라 `spec.template.spec.containers`다.

코드에서 이 경로를 처리하는 부분:
```python
if isinstance(spec, dict) and isinstance(spec.get("template"), dict):
    spec = spec["template"].get("spec", {})
```

이 로직이 없으면 Deployment를 스캔할 때 컨테이너를 찾지 못한다.

## 실제로 만들어 본 뒤에 체감한 것

EKS를 한 번도 만져보지 않았는데, manifest 검사만으로도
실제 보안 감사에서 나오는 finding들을 대부분 재현할 수 있었다는 게 놀라웠다.

특히 `privileged: true`와 `capabilities.add: ["ALL"]`이 별개 규칙이라는 점이 흥미로웠다.
효과는 비슷한데, 설정 방법이 다르기 때문에 둘 다 잡아야 한다.
이런 미묘한 차이를 코드로 구현하면서 K8s 보안 모델에 대한 이해가 깊어졌다.

## 이 과제의 위치

- **과제 05 → 이 과제**: CSPM Rule Engine이 Terraform을 다뤘다면, 이 과제는 K8s manifest를 다룬다
- **이 과제 → 과제 10**: Control Plane의 K8s ingestion API가 같은 scan_manifest 로직을 사용한다

## 한계와 v1 범위

- PodSecurity Admission(PSA) 전체를 재현하지는 않는다.
- NetworkPolicy, RBAC 검사는 포함하지 않았다.
- 실제 컨테이너 이미지를 pull해서 레이어를 분석하지 않는다.
- Helm chart나 Kustomize overlay는 다루지 않는다.

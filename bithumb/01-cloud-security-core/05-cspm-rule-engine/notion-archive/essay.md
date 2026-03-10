# Misconfiguration을 코드로 잡아내기

## CSPM이란 결국 무엇인가

CSPM(Cloud Security Posture Management)이라는 용어는 거창하지만,
실제로 하는 일은 의외로 단순하다.

"이 설정이 안전한가?"라는 질문에 자동으로 답하는 것이다.

S3 버킷이 퍼블릭으로 열려 있으면 안 된다. Security Group이 인터넷 전체에서 SSH를 허용하면 안 된다.
스토리지 암호화가 꺼져 있으면 안 된다. 이런 "안 되는 것"들을 규칙으로 만들고,
인프라 설정에 그 규칙을 적용해서 finding을 생성하는 것이 CSPM의 핵심이다.

이 과제는 그 핵심을 최소한으로 구현하는 것이다.
화려한 DSL이나 대시보드 없이, Terraform plan JSON과 access key snapshot을 읽어서
바로 triage 가능한 finding을 만드는 규칙 엔진을 코드로 작성한다.

## 두 가지 입력 소스

### Terraform plan JSON

과제 02에서 `terraform plan → terraform show -json`으로 만든 plan JSON이
이 과제의 첫 번째 입력이다.

plan JSON 안의 `planned_values.root_module.resources` 배열을 순회하면서,
각 리소스의 `type`과 `values`를 검사한다.

Terraform이 "어떤 리소스를 어떤 설정으로 만들려고 하는지"를 미리 알려 주기 때문에,
실제로 배포하기 전에 위험 설정을 걸러낼 수 있다.
이것이 "shift left" — 문제를 최대한 앞 단계에서 잡는 것 — 의 실제 구현이다.

### access key snapshot

Terraform이 커버하지 못하는 운영 상태 정보도 있다.
대표적인 것이 IAM access key의 나이다.

access key가 90일을 넘기면 교체해야 한다는 것은 대부분의 보안 기준에서 합의된 규칙이다.
이 정보는 Terraform plan에 들어 있지 않으므로, 별도의 snapshot JSON으로 입력받는다.

plan 기반 규칙과 snapshot 기반 규칙을 섞어 보면,
CSPM이 "정적 분석만 하는 도구"가 아니라 "운영 상태까지 포함하는 도구"라는 감각이 생긴다.

## 네 가지 탐지 규칙

### CSPM-001: S3 퍼블릭 접근 차단 미설정

`aws_s3_bucket_public_access_block` 리소스에서
`block_public_acls`, `block_public_policy`, `ignore_public_acls`, `restrict_public_buckets`
네 플래그가 전부 `true`가 아니면 발동한다.

네 플래그 중 하나라도 `false`면 위험하다.
처음에는 각각을 개별 finding으로 만들려고 했지만,
"퍼블릭 차단이 완전하지 않다"는 하나의 finding으로 묶는 것이 운영자 입장에서 더 유용했다.

### CSPM-002: SSH/RDP 인터넷 노출

`aws_security_group`의 ingress 규칙에서
22번(SSH) 또는 3389번(RDP) 포트가 `0.0.0.0/0`으로 열려 있으면 발동한다.

이 규칙은 과제 02의 insecure/main.tf에서 의도적으로 만든 설정을 정확히 잡아낸다.

### CSPM-003: 스토리지 암호화 미설정

`aws_db_instance`나 `aws_ebs_volume`에서 `storage_encrypted`가 `false`이면 발동한다.
데이터 저장 시 암호화는 대부분의 컴플라이언스 기준에서 필수 요구사항이다.

### CSPM-004: access key 나이 초과

access key snapshot에서 `age_days`가 90일을 초과하면 발동한다.
임계값은 기본 90일이지만 파라미터로 변경 가능하다.

## 좋은 규칙의 기준

이 과제를 통해 체감한 "좋은 CSPM 규칙"의 기준은 세 가지다.

**1. false positive가 적어야 한다.**
`Resource=*`이더라도 읽기 전용 액션만 있으면 finding을 내지 않는 것처럼,
규칙의 입력 스키마를 좁혀서 오탐을 줄여야 한다.

**2. 설명 가능해야 한다.**
finding의 `title`을 읽었을 때, 운영자가 "아, 이것 때문에 걸렸구나"를 바로 이해할 수 있어야 한다.

**3. 액션과 연결 가능해야 한다.**
finding을 보고 "그래서 어떻게 고치나?"라는 질문에 답할 수 있어야 한다.
이 과제의 finding은 과제 06(Remediation Pack Runner)에서 dry-run 조치안으로 연결된다.

## 실제로 만들어 본 뒤에 체감한 것

insecure plan에서 3개 finding(CSPM-001, 002, 003)이 나오고,
secure plan에서 0개 finding이 나오는 것을 확인한 순간이 가장 만족스러웠다.

"같은 종류의 리소스인데 설정만 다르면 결과가 달라진다"는 것이
CSPM의 핵심을 가장 직관적으로 보여 주는 결과였다.

그리고 access key 규칙을 추가하면서, Terraform plan만으로는 커버할 수 없는 영역이 있다는 것도 체감했다.
CSPM은 IaC(Infrastructure as Code) 분석과 운영 상태 분석을 둘 다 포함해야 완전하다.

## 이 과제의 위치

- **과제 02 → 이 과제**: Terraform plan JSON이 이 규칙 엔진의 입력이 된다
- **과제 04 → 이 과제**: IAM policy finding과 같은 Finding 구조를 공유한다
- **이 과제 → 과제 06**: finding을 입력받아 remediation dry-run을 생성한다
- **이 과제 → 과제 10**: Control Plane의 scan worker가 같은 scan_plan 로직을 사용한다

## 한계와 v1 범위

- 규칙 셋은 S3/SG/encryption/access key age 네 가지로 제한한다.
- 규칙 정의를 외부 설정 파일로 분리하지 않았다 (코드에 하드코딩).
- CIS Benchmark나 AWS Config rules와의 매핑은 포함하지 않았다.
- severity 결정 로직이 없다 (전부 HIGH 또는 MEDIUM으로 고정).

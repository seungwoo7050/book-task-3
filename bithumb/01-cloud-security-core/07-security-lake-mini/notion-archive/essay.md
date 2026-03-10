# 로그를 모으는 것과 이상 행위를 찾는 것

## 과제 03과 이 과제의 차이

과제 03에서는 CloudTrail과 VPC Flow Logs를 정규화해서 DuckDB에 넣었다.
"서로 다른 포맷의 로그를 하나의 테이블에서 질의할 수 있게 만드는 것"이 목표였다.

이 과제는 그 다음 질문에 답한다.
"이 로그에서 **의심스러운 행위**를 자동으로 찾을 수 있는가?"

Security Lake의 핵심은 로그를 모으는 것이 아니다.
모은 로그에 detection query를 적용해서, 사람이 직접 모든 로그를 읽지 않아도
주의가 필요한 이벤트를 alert로 올려 주는 것이다.

이 과제는 그 detection—alert 흐름을 로컬에서 최소한으로 구현한다.

## 다섯 가지 detection query

"어떤 이벤트가 의심스러운가?"를 결정하는 것은 detection engineering의 핵심이다.
이 과제에서는 AWS 환경에서 가장 흔하고 위험한 다섯 가지 이벤트를 detection 대상으로 선택했다.

### LAKE-001: CreateAccessKey

새로운 IAM access key가 생성되었다.
공격자가 계정을 탈취한 후 가장 먼저 하는 행동 중 하나가 펄시스턴스를 위한 키 생성이다.
정상 운영에서도 발생할 수 있지만, 반드시 누가 왜 만들었는지 확인해야 한다.

### LAKE-002: PutBucketAcl

S3 버킷의 ACL이 변경되었다.
데이터 유출의 전조가 될 수 있는 이벤트다. "이 변경이 의도된 것인지" 확인이 필요하다.

### LAKE-003: AuthorizeSecurityGroupIngress

Security Group에 새로운 인바운드 규칙이 추가되었다.
공격자가 내부 네트워크로 접근 경로를 열 수 있는 이벤트다.

### LAKE-004: DeleteTrail

CloudTrail 자체가 삭제되었다.
이건 "로그를 없애려는 시도"로, 공격자가 자신의 흔적을 지우려는 것일 수 있다.
detection 대상 중 가장 높은 위험도를 가진다.

### LAKE-005: Root ConsoleLogin

root 계정으로 콘솔 로그인이 발생했다.
root 계정은 일상적으로 사용하면 안 되는 계정이다.
이 이벤트가 발생하면 "왜 root를 사용했는지" 반드시 확인해야 한다.

## 설계 선택

### 모든 detection을 하나의 SQL로 처리한 이유

다섯 가지 detection rule을 각각 별도 쿼리로 만들 수도 있었지만,
하나의 `CASE WHEN` 문으로 처리했다. 이유는 두 가지다.

1. **DuckDB에서는 한 번 스캔이 효율적이다.** 테이블을 다섯 번 읽는 것보다 한 번 읽으면서 분류하는 게 낫다.
2. **rule이 독립적이지만 출력은 같은 형태다.** 모든 alert가 `control_id`, `event_name`, `actor`, `occurred_at` 네 필드를 가지므로, 하나의 결과 셋으로 합치는 게 자연스럽다.

### Alert 구조를 따로 정의한 이유

과제 04, 05에서 사용한 Finding과 비슷하지만, Alert는 다른 구조다.
- Finding: 정적 분석 결과 ("이 설정이 위험하다")
- Alert: 행위 탐지 결과 ("이 행동이 의심스럽다")

Alert에는 `event_name`과 `actor`가 필수적이고,
Finding에는 `resource_type`과 `resource_id`가 필수적이다.
이 차이를 구조로 드러내는 것이 데이터 모델의 명확성에 중요하다.

과제 10(Control Plane)에서는 이 둘을 하나의 `findings` 테이블에 통합하는데,
그 시점에서 `source` 필드가 "어디서 온 finding인지"를 구분해 준다.

### Parquet 출력을 유지한 이유

과제 03과 마찬가지로, 적재 시 Parquet 파일도 함께 생성한다.
이 파일이 있으면 DuckDB 없이도 다른 도구(pandas, Spark, Athena)로 분석할 수 있다.
Security Lake의 실제 저장 포맷이 Parquet이기도 해서, 이 습관이 유용하다.

## 실제로 만들어 본 뒤에 체감한 것

fixture에 다섯 가지 의심스러운 이벤트를 전부 넣고 detection query를 돌렸을 때,
`LAKE-001`부터 `LAKE-005`까지 순서대로 alert가 나오는 것을 확인한 순간이 가장 만족스러웠다.

"로그를 SQL로 질의하면 이상 행위를 자동으로 찾을 수 있다"는 것이
말로 들었을 때는 당연하게 느껴지는데, 직접 쿼리를 작성하고 결과를 보면 정말 다르다.
특히 LAKE-005(root ConsoleLogin)는 `actor LIKE '%:root'` 조건으로 잡는데,
이 한 줄이 "root 계정 남용 탐지"라는 실제 보안 요구사항을 구현한다는 게 인상적이었다.

## 이 과제의 위치

- **과제 03 → 이 과제**: 정규화 + DuckDB 패턴을 재사용하되, detection query와 alert 생성이 추가된다
- **이 과제 → 과제 10**: Control Plane의 CloudTrail ingestion이 같은 적재 + detection 흐름을 사용한다
- **이 과제 → 과제 10**: alert를 finding으로 변환해서 DB에 저장하는 확장이 capstone에서 이루어진다

## 한계와 v1 범위

- VPC Flow Logs는 포함하지 않았다 (과제 03에서 다룸).
- multi-table join (로그 소스 간 상관 분석)은 capstone에서 확장한다.
- detection query가 하드코딩되어 있다. 외부 YAML/JSON으로 관리하지 않는다.
- 시계열 기반 이상 탐지(baseline 대비 이탈)는 범위 밖이다.
- alert의 severity 결정 로직이 없다 (모든 alert가 동일 레벨).

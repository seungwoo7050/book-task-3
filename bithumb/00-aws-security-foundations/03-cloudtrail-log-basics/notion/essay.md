# 로그를 "읽는 것"에서 "질의하는 것"으로

## 왜 이 과제를 만들었나

CloudTrail 로그를 JSON 파일로 열어서 눈으로 읽는 건 어렵지 않다.
`eventName`이 뭔지, `userIdentity`가 누군지, `eventTime`이 언제인지는 필드 이름만 봐도 알 수 있다.

그런데 "지난 한 시간 동안 누가 무엇을 했는지"를 질문하려면 이야기가 달라진다.
JSON 파일을 grep으로 뒤지는 것과 SQL로 질의하는 것 사이에는 엄청난 생산성 차이가 있다.

이 과제는 그 전환 — "로그를 읽는 것"에서 "로그를 질의하는 것"으로 — 을 체감하는 과제다.
CloudTrail 이벤트와 VPC Flow Logs라는 서로 다른 포맷의 로그를 하나의 정규화된 테이블에 넣고,
DuckDB로 요약 질의를 돌리는 것이 목표다.

## 정규화라는 발상

CloudTrail과 VPC Flow Logs는 포맷이 완전히 다르다.

CloudTrail은 `eventTime`, `eventSource`, `eventName`, `userIdentity`라는 구조화된 필드를 가지고 있고,
VPC Flow Logs는 `timestamp`, `source_ip`, `destination_port`, `action` 같은 네트워크 계층 필드를 가지고 있다.

이 둘을 같은 테이블에 넣으려면 공통 스키마가 필요하다.
그래서 `EventRecord`라는 데이터 클래스를 정의했다:

- `occurred_at`: 이벤트 발생 시점
- `source`: 로그 출처 (cloudtrail, vpc-flow-logs)
- `event_name`: 어떤 이벤트인지
- `actor`: 누가 했는지
- `resource_id`: 어떤 리소스에 대한 것인지
- `action_result`: 결과 (허용/거부/출처 태그)

이 여섯 필드만 뽑아내면, 원본 포맷이 달라도 같은 SQL로 질의할 수 있다.
"어떤 actor가 가장 많은 이벤트를 발생시켰는지", "특정 시간 범위에 몇 건의 이벤트가 있었는지"를
하나의 쿼리로 답할 수 있게 되는 것이다.

이 발상이 정규화(normalization)이고, 이후 Security Lake 과제에서 그대로 확장된다.

## DuckDB와 Parquet를 선택한 이유

로그를 적재할 저장소로 DuckDB를 선택한 이유는 세 가지다.

**1. 설치가 필요 없다.** `pip install duckdb`만으로 끝난다. PostgreSQL이나 SQLite처럼 별도 프로세스가 필요 없고,
Python 프로세스 안에서 바로 SQL을 실행할 수 있다.

**2. Parquet 내보내기가 한 줄이다.** `COPY table TO 'path' (FORMAT PARQUET)` 한 줄로 columnnar 포맷 파일이 만들어진다.
Parquet는 AWS Security Lake의 기본 저장 포맷이기도 해서, 로컬에서 익혀 두면 실제 환경과 감각이 이어진다.

**3. SQL 문법이 표준에 가깝다.** GROUP BY, COUNT, 시간 범위 필터 같은 기본 질의가 PostgreSQL과 거의 같은 문법으로 동작한다.

## 설계 선택

### ETL을 하나의 파일에 담은 이유

`etl.py` 하나에 정규화, 적재, 요약 함수를 전부 넣었다.
과제 규모가 작기 때문에 모듈을 쪼개는 것보다 흐름을 한눈에 보는 게 더 중요했다.

함수 순서가 곧 파이프라인 순서다:
1. `normalize_cloudtrail_events()` — CloudTrail JSON → EventRecord 리스트
2. `normalize_vpc_flow_logs()` — VPC Flow Logs JSON → EventRecord 리스트
3. `ingest_records()` — EventRecord 리스트 → DuckDB 테이블 + Parquet 파일
4. `summarize_by_event_name()` — 이벤트 이름별 집계
5. `summarize_by_actor()` — actor별 집계
6. `within_time_range()` — 시간 범위 내 이벤트 수

### fixture 데이터를 직접 만든 이유

실제 AWS CloudTrail 로그를 사용하지 않고 fixture JSON을 직접 만들었다.
AWS 계정이 없어도 테스트할 수 있어야 하는 것이 이 트랙의 설계 원칙이기 때문이다.

fixture에는 의도적으로 다양한 이벤트를 넣었다:
- `CreateAccessKey`: IAM 키 생성 (잠재적으로 의심스러운 행위)
- `PutBucketAcl`: S3 버킷 ACL 변경 (데이터 노출 위험)
- VPC Flow Logs의 22번/443번 포트 트래픽

이 이벤트들은 과제 07(Security Lake Mini)에서 detection query의 대상이 된다.

## 실제로 만들어 본 뒤에 체감한 것

처음에는 "로그 정규화"가 단순한 필드 매핑 작업이라고 생각했다.
그런데 실제로 CloudTrail의 `requestParameters`에서 `resource_id`를 뽑는 과정에서,
같은 이벤트 종류라도 `bucketName`으로 올 수도 있고 `userName`으로 올 수도 있다는 걸 알게 됐다.

이런 불규칙성을 코드에서 처리하고 나니, "정규화는 단순 매핑이 아니라 비즈니스 규칙을 결정하는 작업"이라는 걸 체감했다.
어떤 필드를 `resource_id`로 삼을지, fallback은 어떻게 할지, 이런 판단이 정규화의 핵심이었다.

또한 DuckDB로 SQL을 돌려 본 순간, grep으로 로그를 뒤지던 것과 차원이 다르다는 걸 느꼈다.
`GROUP BY actor`로 누가 가장 활발한지 한 줄로 확인하고,
시간 범위 필터로 특정 시간대만 잘라내는 게 이렇게 편한지 몰랐다.

## 이 과제의 위치

- **과제 01, 02 → 이 과제**: IAM 정책과 Terraform 설정을 이해한 뒤, 이제 "무슨 일이 일어났는지"를 추적하는 로그로 넘어간다
- **이 과제 → 과제 07**: 여기서 만든 정규화 + DuckDB 적재 패턴이 Security Lake Mini에서 detection query와 alert 생성으로 확장된다
- **이 과제 → 과제 10**: Control Plane의 CloudTrail ingestion API가 같은 정규화 흐름을 사용한다

## 한계와 v1 범위

- 실제 CloudTrail 스키마의 모든 필드를 보존하지는 않는다. 정규화에 필요한 최소 필드만 추출한다.
- VPC Flow Logs의 실제 포맷(공백 구분 텍스트)이 아닌 JSON fixture를 사용한다.
- 시계열 분석이나 이상 탐지 알고리즘은 포함하지 않는다. 기본 요약 질의까지가 범위다.

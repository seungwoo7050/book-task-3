# 모든 Finding을 고치지 않아도 된다 — 예외 관리의 필요성

## 왜 이 과제를 만들었나

보안 도구는 위험을 찾는다. 과제 04부터 08까지,
모든 프로젝트는 "위험을 탐지해서 finding을 생성한다"에 집중했다.
하지만 실제 보안 운영에서 모든 finding이 즉시 수정 대상은 아니다.

- **허용된 위험**: 비즈니스 필요에 의해 의도적으로 유지하는 설정
- **일시적 예외**: 마이그레이션 기간에만 필요한 과도기 설정
- **보상 통제**: 다른 보안 장치가 동일한 위험을 커버하고 있는 경우

이런 경우에 finding을 "해제"하면 안 되고, "예외(exception)"로 관리해야 한다.
예외에는 반드시 사유가 있고, 증거(evidence)가 붙고,
누가 언제 승인했는지 감사 기록(audit trail)이 남아야 한다.

이 과제는 그 "예외 관리 시스템"을 최소 단위로 구현한다.

## ExceptionManager의 핵심 흐름

### 1. 예외 생성 (create)

```
exception = manager.create_exception(
    finding_id="...",
    reason="마이그레이션 기간 중 임시 허용",
    expires=datetime(2025, 9, 1)
)
```

예외를 생성하면 아직 유효하지 않다. `status`는 `"pending"`이다.
예외를 만드는 사람과 승인하는 사람이 같으면 안 되기 때문이다.
(실제 프로덕션에서는 '4-eyes principle'이라는 원칙.)

이 구현에서는 단순화를 위해 같은 사람이 할 수 있지만,
"생성과 승인이 별개 동작"이라는 구조는 유지했다.

### 2. 승인 (approve)

```
manager.approve_exception(exception_id, approved_by="security-lead")
```

승인이 일어나면:
- `status`가 `"approved"`로 바뀐다
- audit 이벤트가 추가된다: `{"type": "approved", "by": "security-lead", "at": ...}`
- 이 시점부터 `is_suppressed(finding_id)`가 `True`를 반환한다

### 3. 억제 확인 (is_suppressed)

```
manager.is_suppressed(finding_id) → True/False
```

이 함수는 만료일도 검사한다.
`expires`가 `datetime.now()`보다 과거면, 승인된 예외라도 `False`를 반환한다.
이게 **자동 만료**의 핵심이다.

### 4. 증거 첨부 (add_evidence)

```
manager.add_evidence(exception_id, {
    "type": "screenshot",
    "url": "s3://bucket/evidence/001.png"
})
```

예외에는 증거를 아무 때나 추가할 수 있다.
증거의 형식은 자유(딕셔너리)이지만,
감사 시점에 "이 예외가 왜 승인되었는지"를 보여주는 용도다.

## append-only라는 설계 감각

ExceptionManager의 audit 이벤트 리스트는 append-only다.
이벤트를 수정하거나 삭제하는 메서드가 없다.

이건 의도적이다.
감사 로그에서 가장 중요한 속성은 **불변성(immutability)**이다.
"누군가 로그를 조작했을 가능성"을 원천 차단해야
규제 준수와 포렌식에서 증거력이 있다.

이 in-memory 구현에서는 프로세스가 재시작되면 전부 날아가지만,
"append-only"라는 구조적 제약을 코드 수준에서 보여준다.
과제 10(Control Plane)에서 PostgreSQL로 영속화할 때,
이 제약은 INSERT-only 테이블로 매핑된다.

## 왜 in-memory인가

이 과제의 저장소는 Python 딕셔너리다. DB가 없다.

이유:
1. **예외 관리의 비즈니스 로직**에 집중하기 위해
2. 영속화는 과제 10(capstone)의 책임이다
3. 단위 테스트가 외부 의존성 없이 실행된다

실무에서는 이 로직을 서비스 레이어에 놓고,
저장소 레이어는 DB로 교체한다.
이 과제가 서비스 레이어의 프로토타입이라고 보면 된다.

## 테스트가 증명하는 것

테스트는 두 가지 시나리오를 확인한다:

**시나리오 1: 만료 전 억제**
- exception 생성 → 승인 → `is_suppressed()` → `True`
- `expires`를 과거 날짜로 바꿈 → `is_suppressed()` → `False`
- 즉, 시간이 지나면 자동으로 예외가 풀린다

**시나리오 2: 증거와 감사 이벤트**
- exception 생성 → evidence 첨부 → 승인
- `evidence` 리스트에 항목이 추가되었는지 확인
- `audit_events` 리스트에 이벤트가 추가되었는지 확인
- 이것이 append-only의 실증이다

## 이 과제의 위치

- **앞선 과제 04~08**: finding을 탐지하는 "공격면(attack surface) 분석"이었다
- **이 과제**: 탐지된 finding 중 일부를 의도적으로 억제하는 "운영 관리" 영역이다
- **과제 10**: ExceptionManager의 로직이 FastAPI 엔드포인트와 PostgreSQL 위에서 작동한다

## 한계와 v1 범위

- 영속화 없음 (프로세스 재시작 시 데이터 소실)
- 역할 기반 접근 통제(RBAC) 없음 — 누구든 생성/승인 가능
- 예외 취소(revoke) 기능 없음
- 만료 후 finding 자동 재활성화 알림 없음

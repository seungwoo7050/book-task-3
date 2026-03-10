# 관측성·신뢰성 입문 가이드

특정 기술 스택에 종속되지 않는 공통 관측성 기준이다. 로컬 데모 프로젝트부터 캡스톤 제출까지 동일한 원칙을 적용한다.

---

## 1. 최소 SLI/SLO 모델

SLI(Service Level Indicator)는 "지금 잘 동작하고 있는가"를 수치로 표현한 신호다. SLO(Service Level Objective)는 그 신호에 대한 목표 경계값이다.

### 1.1 데모 프로젝트 기준 최소 SLI 세트

| SLI 유형 | 정의 | 측정 방법 |
|----------|------|-----------|
| **지연시간** | 성공한 요청의 응답 시간 | 애플리케이션 미들웨어 or 프록시 로그 |
| **에러율** | 전체 요청 중 5xx 응답 비율 | HTTP 상태 코드 집계 |
| **가용성** | 시간 창 내 서비스 UP 비율 | healthcheck endpoint 성공 여부 |

### 1.2 데모 프로젝트 기준 최소 SLO

```
지연시간  : p99 < 500ms  (smoke/baseline 구간 기준)
에러율    : < 1%         (정상 부하 구간 기준)
가용성    : > 99%        (테스트 실행 전 구간 기준)
```

> **캡스톤 제출**: 제출 전 로드 테스트 결과에서 SLO 달성 여부를 증거로 첨부한다.
> 세부 측정은 [load-testing.md](load-testing.md) 참고.

### 1.3 슬랙 산정 원칙

- 데모와 로컬 환경에서는 SLO를 낮게 잡되 명시적으로 기록한다.
- 목표와 실제의 차이를 숨기지 않는다. 차이 자체가 개선 근거가 된다.
- 데이터 없이 SLO를 선언하지 않는다. smoke 테스트 결과를 먼저 확보하고 기준선을 정한다.

---

## 2. 로깅 / 메트릭 / 트레이싱 최소 구성

세 신호가 없으면 "증상은 알지만 원인을 모른다"는 상태가 된다. 최소 하나씩 갖춰야 장애 원인 추적이 가능하다.

### 2.1 로깅

**최소 요건**

- 모든 요청에 `method`, `path`, `status_code`, `duration_ms` 기록
- 에러 로그에 `stack trace` 또는 `error.message` 포함
- 구조화 로그 (JSON 한 줄) 권장 — grep 대신 jq로 필터 가능

**스택별 빠른 적용**

| 스택 | 도구 예시 |
|------|-----------|
| Python / FastAPI | `structlog`, `uvicorn` access log |
| Go | `slog` (표준 라이브러리), `zerolog` |
| Node.js | `pino`, `winston` |
| C++ | stdout JSON 직접 출력 (간단한 경우) |

**로그 보존 최소 기준 (로컬)**

```
로컬 파일 로테이션 : 7일 or 100MB
구조화 로그 검색  : docker compose logs --since 1h | jq '.status_code'
```

### 2.2 메트릭

**최소 요건**

- 요청 수 (counter)
- 요청 지연시간 히스토그램 (histogram)
- 에러 수 (counter)
- 외부 의존 연결 상태 (gauge)

**노출 방식**

```
/metrics  →  Prometheus exposition format (plain text)
```

스택에 무관하게 `/metrics` 엔드포인트 하나만 있으면 Prometheus + Grafana 스택으로 시각화 가능하다.

### 2.3 트레이싱

데모 수준에서는 분산 트레이싱보다 **요청 ID(correlation ID)** 전파로 시작한다.

```
요청 진입 시  → X-Request-ID 헤더 생성 또는 수신
모든 로그에  → request_id 필드 포함
외부 호출 시 → 동일 request_id를 다음 서비스로 전달
```

분산 트레이싱이 필요하면: OpenTelemetry SDK → Jaeger (로컬) 또는 OTLP 엔드포인트.

---

## 3. 스택 비종속 체크리스트

### 3.1 계측 체크리스트

```
[ ] /health 또는 /healthz 엔드포인트 응답 확인
[ ] /metrics 엔드포인트 (또는 로그 기반 메트릭) 존재
[ ] 요청 로그에 duration_ms 포함
[ ] 에러 로그에 stack trace 포함
[ ] request_id 전파 구현 (다중 서비스 경우)
[ ] DB / Redis / 큐 연결 상태 로깅
```

### 3.2 알림 체크리스트

```
[ ] 에러율 임계치 초과 시 로그 레벨 ERROR 발행
[ ] healthcheck 연속 실패 시 컨테이너 재시작 (Docker Compose restart 정책)
[ ] p99 임계치 초과 기록 → 로드 테스트 보고서에 첨부
```

### 3.3 예시: Docker Compose healthcheck

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
  interval: 10s
  timeout: 5s
  retries: 3
  start_period: 15s
```

---

## 4. 인시던트 생명주기 템플릿

로컬 장애 훈련과 캡스톤 제출 증거에 공통으로 사용한다.
실제 장애 시나리오 실행은 [failure-injection.md](failure-injection.md) 참고.

### 4.1 단계별 정의

```
감지  → 어떤 신호로 문제를 인지했는가?
분류  → 영향 범위와 심각도를 어떻게 판단했는가?
완화  → 어떤 조치로 서비스를 회복시켰는가?
분석  → 근본 원인은 무엇이고 재발 방지 조치는 무엇인가?
```

### 4.2 인시던트 보고서 템플릿

```markdown
## 인시던트 보고서

**제목**: [한 줄 요약]
**발생**: YYYY-MM-DD HH:MM (로컬 시각)
**해결**: YYYY-MM-DD HH:MM
**총 지속 시간**: X분

### 감지
- 감지 신호: [로그 / 알림 / 수동 확인]
- 감지 시점: HH:MM
- 확인 명령:
  ```
  [실제 실행한 명령 붙여넣기]
  ```

### 분류
- 영향 범위: [전체 서비스 / 특정 기능 / 특정 사용자]
- 심각도: P1 / P2 / P3
- 주요 SLI 위반: [지연시간 / 에러율 / 가용성]

### 완화
- 조치 순서:
  1. [조치 1]
  2. [조치 2]
- 서비스 회복 시점: HH:MM
- 실행 명령:
  ```
  [실제 실행한 명령 붙여넣기]
  ```

### 사후 분석
- 근본 원인: [한 문장]
- 기여 요인:
  - [요인 1]
  - [요인 2]
- 재발 방지:
  - [ ] [액션 1]
  - [ ] [액션 2]
- 런북 업데이트 필요 여부: Y / N
```

---

## 5. Evidence Package — README 첨부 섹션

캡스톤 또는 데모 제출 README에 아래 섹션을 포함한다.

```markdown
## 운영 증거 (Evidence Package)

### 변경 전/후 메트릭

| 지표 | 변경 전 | 변경 후 | 목표 |
|------|---------|---------|------|
| p99 지연시간 | Xms | Yms | < 500ms |
| 에러율 | X% | Y% | < 1% |
| 처리량 (RPS) | X | Y | — |

> 측정 조건: [스크립트명 또는 테스트 단계], [날짜], [환경]

### 장애 타임라인

| 시각 | 이벤트 |
|------|--------|
| T+0  | 장애 감지 |
| T+Xm | 원인 식별 |
| T+Ym | 완화 조치 적용 |
| T+Zm | 서비스 회복 |

### 런북 링크

- [장애 시나리오 실행 방법](../../guides/devops/failure-injection.md)
- [로드 테스트 실행 방법](../../guides/testing/load-testing.md)
- [인시던트 보고서](./docs/incident-YYYYMMDD.md)
```

---

## 관련 문서

- [failure-injection.md](failure-injection.md) — 재현 가능한 로컬 장애 시나리오
- [load-testing.md](../testing/load-testing.md) — 성능 측정과 SLO 검증
- [submission-readiness-rubric.md](../submission/submission-readiness-rubric.md) — 제출 판정 기준

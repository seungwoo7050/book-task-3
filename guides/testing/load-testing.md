# 로드 테스트 가이드

소규모이지만 근거 있는 성능 검증을 위한 가이드다. SLO 기준선 설정과 제출 증거 확보가 주목적이다. SLI/SLO 정의는 [observability-reliability.md](../devops/observability-reliability.md)를 참고한다.

---

## 1. 스택별 도구 선택

| 스택 | 권장 도구 | 이유 |
|------|-----------|------|
| Python / Go / Node 백엔드 | **k6** | JavaScript 스크립트, CI 통합 쉬움, 체계적인 단계 설정 |
| Python 백엔드 (팀 친화) | **Locust** | Python 코드로 시나리오 작성, 웹 UI 내장 |
| C++ 서버 | **간단한 C++ 클라이언트 하네스** | 프로토콜이 HTTP가 아닌 경우 직접 작성 필요 |
| 범용 (간단한 HTTP) | `hey`, `wrk`, `ab` | 단일 엔드포인트 빠른 확인용 |

> 도구가 없어도 `curl` 루프로 smoke 테스트 수준은 가능하다.

### 1-A: k6 빠른 시작

```bash
# 설치 (macOS)
brew install k6

# 기본 실행
k6 run script.js
```

**기본 스크립트 구조**

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  // stages는 아래 '테스트 단계' 섹션에서 정의
};

export default function () {
  const res = http.get('http://localhost:8080/api/items');
  check(res, {
    'status 200': (r) => r.status === 200,
    'duration < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

### 1-B: Locust 빠른 시작

```bash
pip install locust
locust -f locustfile.py --headless -u 20 -r 5 --run-time 60s \
  --host http://localhost:8080
```

**기본 locustfile**

```python
from locust import HttpUser, task, between

class AppUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def get_items(self):
        self.client.get("/api/items")
```

### 1-C: C++ 클라이언트 하네스

HTTP가 아닌 커스텀 프로토콜 서버를 테스트할 때 사용한다.

```cpp
// harness.cpp — 최소 구조
#include <chrono>
#include <iostream>
// [프로토콜별 연결 코드]

int main(int argc, char* argv[]) {
    int target_rps = std::stoi(argv[1]);   // ex: 100
    int duration_s = std::stoi(argv[2]);   // ex: 60
    int errors = 0;
    int requests = 0;

    auto start = std::chrono::steady_clock::now();
    while (/* elapsed < duration_s */) {
        // 연결 → 요청 전송 → 응답 수신
        // 지연시간 측정 후 히스토그램 버킷에 기록
        requests++;
    }

    std::cout << "requests=" << requests
              << " errors=" << errors << "\n";
}
```

---

## 2. 테스트 단계

### 단계 정의

| 단계 | 목적 | 부하 수준 | 지속 시간 |
|------|------|-----------|-----------|
| **smoke** | 정상 동작 최소 확인 | VU 1–2 또는 RPS 1–5 | 30–60초 |
| **baseline** | SLO 달성 기준선 측정 | 예상 정상 부하 | 3–5분 |
| **stress** | 한계점(saturation) 탐색 | 점진적으로 증가 | 5–10분 |

### k6 단계별 설정 예시

```javascript
// smoke
export const options = {
  vus: 2,
  duration: '30s',
};

// baseline (stages 사용)
export const options = {
  stages: [
    { duration: '1m', target: 20 },   // 워밍업
    { duration: '3m', target: 20 },   // 유지
    { duration: '30s', target: 0 },   // 쿨다운
  ],
  thresholds: {
    http_req_duration: ['p(99)<500'],  // p99 < 500ms
    http_req_failed: ['rate<0.01'],    // 에러율 < 1%
  },
};

// stress
export const options = {
  stages: [
    { duration: '2m', target: 50 },
    { duration: '2m', target: 100 },
    { duration: '2m', target: 200 },
    { duration: '1m', target: 0 },
  ],
};
```

---

## 3. 중단 기준 (Stop Criteria)

테스트를 계속 진행하면 안 되는 조건이다.

| 단계 | 중단 조건 |
|------|-----------|
| smoke | 에러율 > 5% |
| smoke | 서비스 응답 없음 (연결 거부) |
| baseline | 에러율 > 1% 이상으로 지속 |
| baseline | p99 > 목표의 2배 이상 |
| stress | 컨테이너 OOM 재시작 발생 |
| stress | 에러율 > 20% |
| 공통 | 로컬 DB 또는 의존 서비스 다운 |

k6에서는 `thresholds` + `abortOnFail`로 자동 중단 가능:

```javascript
thresholds: {
  http_req_failed: [{ threshold: 'rate<0.01', abortOnFail: true }],
},
```

---

## 4. 필수 출력 지표

### 4.1 지표 정의

| 지표 | 의미 | k6 메트릭명 |
|------|------|------------|
| **p50** | 중간 응답 시간 | `http_req_duration{p:50}` |
| **p95** | 95% 요청의 응답 시간 | `http_req_duration{p:95}` |
| **p99** | 99% 요청의 응답 시간 | `http_req_duration{p:99}` |
| **처리량 (RPS)** | 초당 완료 요청 수 | `http_reqs` rate |
| **에러율** | 실패 요청 비율 | `http_req_failed` rate |
| **포화 지표** | CPU / 메모리 / DB 연결 수 | 외부 `docker stats` 또는 `/metrics` |

### 4.2 결과 저장

```bash
# k6 결과를 JSON으로 저장
k6 run --out json=results.json script.js

# 요약 출력
k6 run script.js | tee load-test-output.txt
```

### 4.3 포화 지표 수집

```bash
# 테스트 실행 중 별도 터미널에서
watch -n 2 'docker stats --no-stream'

# DB 연결 수 (PostgreSQL 예시)
docker compose exec postgres psql -U dev -c \
  "SELECT count(*) FROM pg_stat_activity;"
```

---

## 5. 결과 해석 (Interpretation)

### 5.1 병목 후보 식별

| 증상 | 병목 후보 |
|------|-----------|
| CPU 100%, 지연 증가 | 애플리케이션 로직 최적화 필요 |
| DB 연결 소진, 지연 증가 | 연결 풀 크기 또는 쿼리 최적화 |
| 메모리 증가 → OOM | 메모리 누수 또는 캐시 미한도 |
| 네트워크 처리량 한계 | I/O 병목 또는 페이로드 크기 문제 |
| p50은 낮지만 p99가 급등 | 특정 요청 처리 시간 분산 큼 |

### 5.2 병목 가설 정리 템플릿

```markdown
## 병목 분석

**테스트 단계**: [smoke / baseline / stress]
**관찰한 증상**: [p99 Xms 초과 / 에러율 X%]

### 가설 목록

| # | 가설 | 근거 | 검증 방법 |
|---|------|------|-----------|
| 1 | DB 연결 풀 소진 | DB 연결 수 급증 | 연결 풀 크기 늘리고 재테스트 |
| 2 | 특정 엔드포인트 슬로우 쿼리 | p99만 높고 p50은 낮음 | EXPLAIN ANALYZE 실행 |

### 선택한 가설과 이유
[가설 1번 선택 — DB 연결 수가 max_connections에 근접했기 때문]

### 다음 액션
- [ ] 연결 풀 크기를 X에서 Y로 조정
- [ ] 조정 후 baseline 재실행
- [ ] 결과 비교표 업데이트
```

### 5.3 결과 보고서 템플릿

```markdown
## 로드 테스트 결과

**실행 일자**: YYYY-MM-DD
**환경**: Docker Compose 로컬
**스크립트**: [파일명]

### 단계별 결과

| 단계 | p50 | p95 | p99 | RPS | 에러율 |
|------|-----|-----|-----|-----|--------|
| smoke | Xms | Xms | Xms | X | X% |
| baseline | Xms | Xms | Xms | X | X% |
| stress | Xms | Xms | Xms | X | X% |

### SLO 달성 여부

| SLO | 목표 | 실제 | 달성 |
|-----|------|------|------|
| p99 지연시간 | < 500ms | Xms | Y/N |
| 에러율 | < 1% | X% | Y/N |

### 포화 지점
[stress 단계에서 에러율 급등한 VU 수: X]

### 병목 분석 요약
[분석 내용 또는 병목 분석 템플릿 링크]
```

---

## 관련 문서

- [observability-reliability.md](../devops/observability-reliability.md) — SLI/SLO 정의와 Evidence Package
- [failure-injection.md](../devops/failure-injection.md) — 장애 중 성능 측정 시나리오
- [submission-readiness-rubric.md](../submission/submission-readiness-rubric.md) — 제출 판정에서 요구하는 테스트 증거

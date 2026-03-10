# 로컬 장애 주입 가이드

재현 가능한 로컬 장애 훈련 시나리오다. Docker Compose 기반 환경에서 실행하며, 각 시나리오를 완료하면 인시던트 보고서 초안을 작성한다. 관측성 계측 전제 조건은 [observability-reliability.md](observability-reliability.md)를 먼저 확인한다.

---

## 사전 조건

```bash
# 서비스가 정상 상태로 올라와 있어야 한다
docker compose ps

# 헬스체크 통과 확인
curl -sf http://localhost:8080/health && echo "OK"

# 메트릭 수집 중 확인 (있는 경우)
curl -s http://localhost:8080/metrics | grep -c "^#"
```

---

## 시나리오 1 — 의존 서비스 장애

### 1-A: DB Down

**목적**: 애플리케이션이 DB 연결 실패를 어떻게 처리하는지 확인.

**Setup**

```bash
# PostgreSQL 컨테이너를 강제 정지
docker compose stop postgres
```

**예상 증상 신호**

- 애플리케이션 로그에 `connection refused` 또는 `dial tcp: connection refused` 출력
- `/health` 엔드포인트 응답: DB 상태 `unhealthy`
- HTTP 응답 코드 500 또는 503
- 에러율 SLI 급등

**완화 경로**

```bash
# DB 재기동
docker compose start postgres

# DB 준비 확인 후 앱 로그 확인
docker compose logs postgres --since 30s
docker compose logs app --since 30s
```

**검증**

```bash
# 서비스 정상 복구 확인
curl -sf http://localhost:8080/health | jq

# 에러율 복귀 확인 (메트릭 있는 경우)
curl -s http://localhost:8080/metrics | grep 'http_requests_total.*status="5'
```

**인시던트 후 보고서 항목**

```
근본 원인 : DB 컨테이너 정지
영향      : DB를 사용하는 모든 엔드포인트 응답 불가
완화 조치 : DB 컨테이너 재기동
재발 방지 : DB healthcheck + depends_on condition: service_healthy 적용 확인
```

---

### 1-B: Redis Down

**목적**: 캐시/세션/큐 레이어 단절 시 애플리케이션의 폴백 동작 확인.

**Setup**

```bash
docker compose stop redis
```

**예상 증상 신호**

- Redis를 캐시로 사용하는 경우: 응답 지연 증가 (DB 직접 쿼리로 폴백)
- Redis를 세션 스토어로 사용하는 경우: 로그인 상태 유실
- Redis를 Celery/BullMQ 브로커로 사용하는 경우: 작업 큐 정지, 워커 로그에 연결 재시도 메시지

**완화 경로**

```bash
docker compose start redis
docker compose logs redis --since 30s
```

**검증**

```bash
# Redis 연결 확인
docker compose exec redis redis-cli ping

# 큐 워커 재시작이 필요한 경우
docker compose restart worker
```

**인시던트 후 보고서 항목**

```
근본 원인 : Redis 컨테이너 정지
영향      : 캐시 미스 또는 큐 처리 중단
완화 조치 : Redis 재기동 및 필요 시 워커 재시작
재발 방지 : Redis healthcheck 적용, Redis 없는 경우 폴백 로직 문서화
```

---

### 1-C: Queue Lag

**목적**: 메시지 큐 처리 지연이 누적될 때 시스템이 어떻게 반응하는지 확인.

**Setup**

```bash
# 워커를 정지하여 메시지를 쌓는다
docker compose stop worker

# 요청을 발생시켜 큐에 메시지를 쌓는다 (예: 비동기 작업 endpoint 반복 호출)
for i in $(seq 1 50); do
  curl -s -X POST http://localhost:8080/api/jobs -d '{"type":"process"}' \
    -H "Content-Type: application/json" > /dev/null
done

# 큐 깊이 확인 (RabbitMQ 예시)
# docker compose exec rabbitmq rabbitmqctl list_queues name messages
```

**예상 증상 신호**

- 큐 깊이 증가
- 작업 완료 응답 없음 (polling하는 경우 timeout)
- 워커 로그 없음

**완화 경로**

```bash
# 워커 재기동
docker compose start worker
docker compose logs worker --follow --since 10s
```

**검증**

```bash
# 워커가 메시지를 소비하는지 확인
docker compose logs worker --since 30s | grep "processed\|completed"
```

**인시던트 후 보고서 항목**

```
근본 원인 : 워커 프로세스 정지
영향      : 비동기 작업 미처리 누적
완화 조치 : 워커 재기동 후 백로그 처리
재발 방지 : 큐 깊이 메트릭 모니터링, 워커 restart: unless-stopped 설정
```

---

## 시나리오 2 — 리소스 압박

Docker Compose의 `deploy.resources` 제약을 사용한다.  
적용 후에는 `docker compose up -d` 로 재기동이 필요하다.

### 2-A: CPU 제한

**Setup** (`compose.override.yml` 또는 직접 수정)

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: "0.25"      # 논리 코어의 25%로 제한
```

```bash
docker compose up -d app
```

**예상 증상 신호**

- 응답 지연 증가
- CPU throttling 로그 (cgroup v2 환경)
- p99 지연시간 SLO 위반

**검증**

```bash
# 컨테이너 CPU 사용률 확인
docker stats app --no-stream

# 로드 테스트로 성능 저하 측정
# → load-testing.md의 baseline 단계 실행
```

**완화 경로**: 제한 값을 올리거나 제약 제거 후 `docker compose up -d app`

---

### 2-B: 메모리 제한

**Setup**

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          memory: "128m"
```

```bash
docker compose up -d app
```

**예상 증상 신호**

- OOM(Out Of Memory) kill → 컨테이너 재시작
- `docker compose ps`에서 `Restarting` 상태
- `docker inspect app | jq '.[0].State.OOMKilled'` 결과 `true`

**검증**

```bash
docker inspect $(docker compose ps -q app) | jq '.[0].State.OOMKilled'
docker compose logs app --since 1h | grep -i "OOM\|killed\|memory"
```

**완화 경로**: 메모리 한도 상향 또는 애플리케이션 메모리 누수 수정

---

### 2-C: 디스크 압박 시뮬레이션

**Setup** (임시 대용량 파일로 루트 볼륨 채우기 — 프로덕션 환경에서는 절대 실행하지 말 것)

```bash
# 컨테이너 내부 임시 파일 생성
docker compose exec app dd if=/dev/zero of=/tmp/fill.dat bs=1M count=500
```

**예상 증상 신호**

- 로그 쓰기 실패: `write /var/log/app.log: no space left on device`
- DB 쓰기 실패 (DB 볼륨이 가득 찬 경우)

**검증**

```bash
docker compose exec app df -h /
```

**완화 경로**

```bash
docker compose exec app rm /tmp/fill.dat
```

---

## 시나리오 3 — 네트워크 장애

`tc` 명령 또는 Docker 네트워크 제한을 사용한다. 컨테이너 내부에 `iproute2` 패키지가 있어야 한다.

### 3-A: 네트워크 지연 주입

**Setup**

```bash
# DB 컨테이너에 100ms 지연 추가
docker compose exec postgres sh -c \
  "tc qdisc add dev eth0 root netem delay 100ms"
```

**예상 증상 신호**

- 모든 DB 쿼리에 +100ms 추가 지연
- p99 지연시간 증가
- 타임아웃 설정이 짧으면 간헐적 에러 발생

**기대되는 시스템 동작**

- 연결 풀이 있는 경우: 기존 연결 재사용으로 일부 요청은 정상
- 타임아웃보다 짧은 지연: 지연만 증가, 에러 없음
- 타임아웃보다 긴 지연: 에러율 증가

**검증**

```bash
# 지연 주입 확인
docker compose exec postgres tc qdisc show dev eth0

# 앱 응답 시간 확인
time curl -s http://localhost:8080/api/items
```

**완화 경로**

```bash
docker compose exec postgres sh -c \
  "tc qdisc del dev eth0 root"
```

---

### 3-B: 패킷 손실 주입

**Setup**

```bash
# DB 컨테이너에 10% 패킷 손실 추가
docker compose exec postgres sh -c \
  "tc qdisc add dev eth0 root netem loss 10%"
```

**예상 증상 신호**

- 간헐적 연결 실패
- 에러율 불규칙 상승 (재시도가 없으면 더 높음)
- 타임아웃 후 에러 로그

**기대되는 시스템 동작**

- TCP 재전송으로 일부 복구되지만 지연 증가
- 연결 풀 재사용 시 패킷 손실이 기존 연결에도 영향
- 재시도 로직이 있는 경우 투명하게 처리될 수 있음

**검증**

```bash
docker compose exec postgres tc qdisc show dev eth0
docker compose logs app --since 30s | grep -i "error\|timeout\|retry"
```

**완화 경로**

```bash
docker compose exec postgres sh -c \
  "tc qdisc del dev eth0 root"
```

---

## 인시던트 후 보고서 공통 템플릿

각 시나리오 완료 후 아래 템플릿으로 기록한다.  
전체 포맷은 [observability-reliability.md — 인시던트 생명주기 템플릿](observability-reliability.md#4-인시던트-생명주기-템플릿)을 사용한다.

```markdown
## 장애 훈련 기록

**시나리오**: [1-A DB Down / 1-B Redis Down / ...]
**실행 일자**: YYYY-MM-DD
**환경**: Docker Compose 로컬

### 관찰 사항
- 감지 신호: [실제 확인한 로그 또는 메트릭]
- 복구 소요 시간: X분

### 시스템 동작 요약
- 예상과 일치 여부: Y / N
- 차이 내용: [차이가 있다면 기술]

### 개선 필요 항목
- [ ] [식별된 취약점 1]
- [ ] [식별된 취약점 2]
```

---

## 관련 문서

- [observability-reliability.md](observability-reliability.md) — SLI/SLO 기준과 인시던트 전체 포맷
- [docker-compose.md](docker-compose.md) — Compose healthcheck, 리소스 제한 설정법
- [load-testing.md](../testing/load-testing.md) — 장애 중 성능 측정

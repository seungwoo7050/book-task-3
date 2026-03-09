# 지식 인덱스 — Game Store Capstone에서 다룬 개념들

## 캡스톤 프로젝트

이전 단계에서 개별적으로 학습한 기술들을 하나의 완성된 서비스로 통합하는 프로젝트. 기술의 조합과 트레이드오프를 경험하는 것이 목적.

## Internal Package

Go의 접근 제어 메커니즘. `internal/` 디렉토리 하위 패키지는 해당 모듈 외부에서 import 불가. 컴파일 타임에 강제. 서비스의 내부 구현이 외부에 노출되는 것을 방지.

## Store Pattern

여러 repository 메서드를 하나의 struct에 묶는 패턴. 인터페이스로 추상화해 테스트에서 mock 주입 가능. 이 프로젝트에서는 `repository.Store`가 전체 SQL 접근을 담당.

## Request Hash

동일 멱등성 키에 다른 요청이 매핑되는 것을 감지하기 위한 해시. SHA256으로 `playerID|itemID`를 해시. 멱등성 키 테이블에 함께 저장. 충돌 시 `ErrIdempotencyKeyConflict`.

## Fixed-Window Rate Limiting

시간 윈도우(예: 1초) 내에서 요청 수를 세는 방식. 구현이 간단하지만 윈도우 경계에서 burst 가능. Token Bucket이나 Sliding Window보다 단순하지만 덜 정교함.

## statusRecorder

`http.ResponseWriter`를 감싸서 응답 상태 코드를 캡처하는 패턴. `WriteHeader`를 오버라이드해 코드를 저장. 로깅 미들웨어에서 요청-응답 쌍을 기록할 때 필요.

## DisallowUnknownFields

`json.Decoder`의 설정. JSON에 Go struct에 없는 필드가 있으면 에러. 오타 감지, 입력 검증 강화.

## Defense in Depth

애플리케이션과 DB 양쪽에서 유효성을 검증하는 원칙. 예: 잔액 부족 체크를 서비스에서 하고(`Balance < Price`), DB에서도 CHECK 제약(`CHECK (balance >= 0)`)으로 보장. 한쪽이 뚫려도 다른 쪽이 지킴.

## google/uuid

Google이 관리하는 Go UUID 라이브러리. `uuid.NewString()`으로 UUIDv4 생성. DB의 `gen_random_uuid()` 대신 애플리케이션에서 생성하면 INSERT 전에 ID를 알 수 있어 응답 구성에 유리.

## PollOnce 공개 메서드

Relay의 `PollOnce`를 public으로 두어 테스트에서 ticker 없이 단일 배치를 실행 가능. 시간 의존성을 제거해 테스트를 결정적(deterministic)으로 만듦.

## 에러 매핑 패턴

서비스 레이어의 도메인 에러 → HTTP handler에서 상태 코드 매핑. `errors.Is`, `errors.As`를 사용한 타입 기반 분기. 서비스가 HTTP를 모르고, handler가 비즈니스 로직을 모름.

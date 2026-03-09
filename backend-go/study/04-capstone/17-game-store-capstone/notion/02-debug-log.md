# 디버그 기록 — 통합에서 드러나는 문제들

## Request Hash와 멱등성 키 충돌

같은 `Idempotency-Key`로 다른 요청을 보내면? `request_hash`를 비교해서 `ErrIdempotencyKeyConflict`를 반환. 클라이언트에게 409를 돌려준다.

```go
func buildRequestHash(playerID, itemID string) string {
    h := sha256.Sum256([]byte(playerID + "|" + itemID))
    return hex.EncodeToString(h[:])
}
```

`|` 구분자 없이 concat하면 `"ab"+"cd" == "a"+"bcd"`가 되어 해시 충돌 가능. 구분자가 중요하다.

## 동시 멱등성 키 INSERT

두 요청이 동시에 같은 멱등성 키로 들어오면:
1. 둘 다 `GetIdempotencyKey` → `sql.ErrNoRows`
2. 둘 다 전체 로직 실행
3. 하나는 `InsertIdempotencyKey` 성공, 다른 하나는 `ErrIdempotencyKeyExists`
4. 실패한 쪽은 `retryableTxError` 반환 → 재시도
5. 재시도 시 `GetIdempotencyKey`에서 캐시된 응답 반환

이 설계로 "같은 키 동시 요청"이 안전하게 처리된다.

## Fixed-Window Rate Limiter의 한계

프로젝트 11에서 Token Bucket을 구현했지만 캡스톤에서는 Fixed-Window로 단순화했다. 문제: 윈도우 경계에서 버스트가 발생한다. 예를 들어 limit=10/s일 때, 0.9초에 10개 + 1.0초에 10개 = 0.2초 내에 20개 통과.

프로덕션이라면 Token Bucket이나 Sliding Window가 더 적절하지만, 캡스톤의 "운영 기본 요소" 범위에서는 Fixed-Window로 충분.

## decoder.DisallowUnknownFields

```go
decoder := json.NewDecoder(r.Body)
decoder.DisallowUnknownFields()
```

알 수 없는 JSON 필드가 있으면 에러를 반환. 타이포가 있는 요청을 조기에 잡아낸다. 예: `"playr_id"` → 에러.

## google/uuid vs 수동 생성

`github.com/google/uuid`의 `uuid.NewString()`으로 구매 ID와 outbox 이벤트 ID를 생성. DB의 `gen_random_uuid()`를 사용하지 않고 애플리케이션에서 생성한 이유: INSERT 전에 ID를 알아야 응답 구조체를 미리 만들 수 있기 때문.

## Balance CHECK 제약

```sql
balance BIGINT NOT NULL CHECK (balance >= 0)
```

애플리케이션에서 `player.Balance < item.Price`를 체크하지만, DB에도 CHECK 제약을 걸었다. Defense in depth. 만약 애플리케이션 버그로 음수가 되려 하면 DB에서 에러 반환.

## statusRecorder 패턴

```go
type statusRecorder struct {
    http.ResponseWriter
    status int
}
```

`loggingMiddleware`에서 응답 상태 코드를 기록하기 위한 래퍼. `WriteHeader`를 가로채서 `status` 필드에 저장. 표준 라이브러리의 `http.ResponseWriter`는 작성된 상태 코드를 노출하지 않으므로 이런 래핑이 필요.

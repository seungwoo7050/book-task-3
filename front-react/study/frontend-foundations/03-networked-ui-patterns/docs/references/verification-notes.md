# Verification Notes

## Unit Tests

- abort된 request가 `AbortError`로 종료되는지 본다.
- request tracker가 최신 토큰만 유효하게 보는지 확인한다.

## Integration Tests

- search 변경이 URL에 반영되고 detail이 같이 로드되는지 확인한다.
- simulated failure 후 retry가 성공 상태로 돌아오는지 확인한다.

## E2E Tests

- query-param navigation과 detail selection을 브라우저에서 확인한다.
- simulated failure -> retry -> keyboard open flow가 실제로 통과하는지 본다.

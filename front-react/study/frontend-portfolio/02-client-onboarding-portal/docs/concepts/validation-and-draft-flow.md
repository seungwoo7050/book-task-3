# Validation And Draft Flow

이 앱은 입력 정확도와 복구 가능성을 같이 보여 주는 쪽을 택했다.

## Validation

- sign-in은 email / password 최소 조건만 검증한다.
- workspace profile은 필수 입력과 email 형식을 Zod로 검증한다.
- invite는 valid email과 역할 선택을 요구한다.

## Draft Save

- workspace profile은 `Save draft`를 눌렀을 때 local storage 기반 mock service에 저장된다.
- 새로고침 뒤에도 profile query가 같은 draft를 읽어 form을 복원한다.
- 이 방식은 auto-save보다 덜 화려하지만, 언제 저장되었는지 사용자에게 설명하기 쉽다.

## Submit Retry

- review step에는 demo용 "next submit failure" 토글이 있다.
- 첫 실패 뒤에는 retry가 즉시 가능해야 하므로 pending/error state를 명확히 정리한다.

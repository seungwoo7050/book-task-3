# Verification Notes

검증은 semantic correctness와 keyboard flow를 동시에 본다.

## Unit / DOM Tests

- validation helper가 짧은 workspace name과 잘못된 email을 잡는지 확인한다.
- shell 렌더 후 landmark와 labeled control이 존재하는지 본다.
- invalid submit 시 `aria-invalid`, error text, focus 이동이 모두 맞는지 확인한다.

## E2E Tests

- landmark, label, help text, responsive grid 변화를 브라우저에서 확인한다.
- keyboard-only로 invalid submit을 만든 뒤, 수정하고 다시 저장하는 흐름을 시연한다.

## Known Limits

- 자동화 테스트는 실제 스크린리더 읽기 순서를 완전히 대체하지 않는다.
- responsive 검증은 grid column change를 기준으로 하며, 모든 viewport를 exhaustive하게 검사하지는 않는다.

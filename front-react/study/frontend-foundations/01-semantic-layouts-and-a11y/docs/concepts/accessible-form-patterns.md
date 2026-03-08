# Accessible Form Patterns

이 프로젝트의 form은 validation 로직보다 관계를 먼저 보이게 만든다.

## Label, Help, Error Pairing

- 각 입력은 `label[for]`와 실제 `id`를 가진다.
- help text와 error text는 `aria-describedby`로 연결한다.
- error가 없을 때도 error element는 같은 자리에 남기되 `hidden`으로 처리한다.

이 구조를 고정하면 validation UI를 바꿔도 관계가 흐트러지지 않는다.

## Validation And Focus

- submit 시 전체 검증을 수행한다.
- 에러가 있으면 첫 번째 invalid input으로 포커스를 되돌린다.
- blur 시에는 해당 필드만 얇게 재검증한다.

이 패턴은 "실패를 알려 준다"보다 "실패 뒤에 다음 행동이 명확하다"는 점에서 중요하다.

## Keyboard Reachability

- skip link를 첫 focusable element로 둔다.
- nav link, form input, action button 순으로 tab 이동이 이어진다.
- 포커스 outline은 제거하지 않는다.

이 단계의 keyboard flow는 최소 범위다. 다음 프로젝트에서 selection, inline edit, delegated events가 추가된다.

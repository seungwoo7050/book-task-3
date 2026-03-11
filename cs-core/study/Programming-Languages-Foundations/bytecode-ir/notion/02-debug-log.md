# 02 Debug Log

## 다시 깨질 수 있는 지점

- compile-time name resolution을 너무 공격적으로 하면 short-circuit 오른쪽의 미정 이름까지 미리 실패시킬 수 있습니다.
- `let` shadowing에서 compile-time binding 복구를 잊으면 주변 expression이 잘못된 local slot을 읽게 됩니다.
- capture source가 local인지 outer capture인지 구분하지 않으면 nested closure에서 값이 섞입니다.
- disassembly golden은 instruction offset 하나만 바뀌어도 깨지므로 lowering 규칙을 바꾸면 테스트를 같이 갱신해야 합니다.

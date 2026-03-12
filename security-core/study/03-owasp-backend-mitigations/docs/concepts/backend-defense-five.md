# backend defense five

## 1. Injection

사용자 입력이 query structure를 바꾸면 injection risk가 생깁니다. 이 프로젝트는 ORM 종류가 아니라 parameterized query 여부만 봅니다.

## 2. Broken access control

authenticated user가 맞더라도 “이 리소스를 읽어도 되는가”는 별도 질문입니다. ownership/scope check가 빠지면 IDOR 성격의 문제가 됩니다.

## 3. SSRF

서버가 대신 outbound request를 보내는 순간 allowlist와 private IP 차단이 필요해집니다. 둘 중 하나만 있으면 internal metadata나 lateral movement 경로가 남을 수 있습니다.

## 4. Debug exposure

stacktrace, ORM error, internal path가 그대로 반환되면 공격자는 내부 구조를 더 쉽게 추측할 수 있습니다.

## 5. Path traversal

파일 다운로드나 export endpoint는 `../` 같은 경로 조작을 안전하게 정규화하지 않으면 쉽게 무너집니다.


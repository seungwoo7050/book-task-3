# 공개 문서

상태: `verified`

이 디렉터리는 request lifecycle과 query navigation을 어떤 규칙으로 설계했는지 설명한다. mock API를 썼더라도 비동기 UI 설계가 제품처럼 읽히도록 근거를 남긴다.

## 문서 목록

- [concepts/request-lifecycle.md](concepts/request-lifecycle.md): loading/error/empty/retry를 어떤 상태 전이로 나눴는지
- [concepts/query-navigation.md](concepts/query-navigation.md): search/category/item을 URL에 반영한 이유
- [references/verification-notes.md](references/verification-notes.md): abort, race, retry, keyboard smoke 검증 기록

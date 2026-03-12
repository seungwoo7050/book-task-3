# 공개 문서

상태: `verified`

이 디렉터리는 diff/patch 범위와 render/commit 분리를 설명한다. 구현 README가 "무엇을 만들었는가"를 말한다면, 여기서는 "왜 이런 파이프라인으로 나눴는가"를 설명한다.

## 문서 목록

- [concepts/diff-and-patch-scope.md](concepts/diff-and-patch-scope.md): prop/child diff와 patch 범위를 어디까지 가져갔는지
- [concepts/render-vs-commit.md](concepts/render-vs-commit.md): render phase와 commit phase를 왜 분리했는지
- [references/verification-notes.md](references/verification-notes.md): diff, patch, scheduler 검증 기준

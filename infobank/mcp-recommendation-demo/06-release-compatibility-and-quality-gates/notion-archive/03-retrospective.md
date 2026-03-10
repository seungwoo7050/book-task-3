# Release Compatibility & Quality Gates — 회고

## 잘 된 것

### gate가 배포 판단을 객관적으로 만든다

"이 버전 배포해도 되나요?"라는 질문에 gate 결과로 답할 수 있다.
PASS이면 배포, FAIL이면 사유를 확인하고 수정.
사람의 주관적 판단에 의존하지 않는다.

### artifact가 감사 추적(audit trail)이 된다

모든 gate 실행 결과를 JSON으로 보존하면,
나중에 "이 버전은 왜 배포되었는가?"를 추적할 수 있다.
v3에서 audit log와 결합하면 더 강력해진다.

## 아쉬운 것

### compatibility gate가 semver에만 의존한다

실제 호환성은 API 인터페이스 변경, 행동 변경 등을 확인해야 하는데,
현재는 버전 번호만 본다. 이건 semver를 올바르게 사용한다는 가정에 의존한다.

### release gate의 eval threshold가 고정이다

모든 도구에 같은 threshold를 적용하므로,
중요도가 높은 도구와 낮은 도구를 구분하지 못한다.

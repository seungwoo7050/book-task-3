# Type Modeling Notes

이 프로젝트의 핵심은 "입력 형태"와 "정리된 내부 형태"를 분리하는 습관이다.

- `BookDraft`는 외부 입력이므로 불완전하거나 중복된 값을 가질 수 있다.
- `NormalizedBook`은 내부에서 믿고 쓸 수 있는 구조이므로 slug, summary, 정규화된 tags를 가진다.
- 비동기 inventory 조회는 실패 가능성이 있으므로 `throw` 하나로 전체를 중단하지 않고 항목 단위 결과로 흡수한다.

이 패턴은 뒤의 DTO 검증, controller/service 경계, repository 반환 타입 설계의 기초가 된다.

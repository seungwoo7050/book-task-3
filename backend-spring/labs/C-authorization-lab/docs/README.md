# C-authorization-lab 설계 메모

이 문서는 인가 랩이 현재 어디까지 구현되었고 어떤 단계가 다음 순서인지 정리한다.

## 현재 구현 범위

- organization 생성
- invite 발급과 수락 흐름
- role 변경 endpoint

## 의도적 단순화

- authorization rule은 service logic에 두고 Spring method security는 아직 적용하지 않았다
- membership state는 인메모리로 유지한다
- ownership check를 설명하는 데 필요한 최소 구조만 남겼다

## 다음 개선 후보

- `@PreAuthorize` 같은 method security로 재구성
- membership과 invitation persistence 추가
- denial-path 테스트 보강

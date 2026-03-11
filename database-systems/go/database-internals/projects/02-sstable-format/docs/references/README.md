# References

## 1. Historical assignment family: LSM Tree Core

- 출처 유형: 과거 과제군
- 확인일: 2026-03-10
- 왜 참고했는가: SSTable record layout과 footer 중심 문제 구성을 복원하기 위해 참고했습니다.
- 무엇을 반영했는가: 현재 문제 문서에서 immutable file format과 lookup metadata 책임을 별도 단계로 정리했습니다.

## 2. Database Internals, Chapter 3

- 출처 유형: 책
- 확인일: 2026-03-10
- 왜 참고했는가: SSTable과 immutable run의 의미를 설명하는 배경 자료로 참고했습니다.
- 무엇을 반영했는가: 문서에서 file format이 LSM read path 전체에 어떻게 이어지는지 설명을 보강했습니다.

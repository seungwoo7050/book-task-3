# 04. 지식 인덱스

## 핵심 개념과 다시 볼 이유

- saved return address overwrite 구조: phase별 payload가 결국 어떤 리턴 경로를 덮는지 먼저 정리해야 한다.
- code injection과 ROP의 차이: 실행 가능한 스택 가정이 깨지는 순간 문제 모델이 완전히 바뀐다.
- gadget chain 계약: gadget은 조각 자체보다 "무엇을 준비하고 무엇을 보존하는가"로 읽어야 한다.
- `%rsp` 기반 상대 주소 계산: 절대 주소 암기보다 스택 기준 상대 위치 계산이 훨씬 오래 남는다.
- 공개 가능한 exploit 문서의 경계: 재현성을 높이되, 비공개 타깃에 바로 적용 가능한 정보는 남기지 않는다.

## 재현 중 막히면 먼저 확인할 것

- payload 분류: `../docs/concepts/payload-models.md`
- ROP와 상대 주소: `../docs/concepts/rop-and-relative-addressing.md`
- 공개 정책: `../docs/references/publication-policy.md`
- 현재 검증 순서: `../docs/references/verification.md`

## 이후 프로젝트와 연결되는 메모

- 보안 과제는 정답 문자열보다 공격 모델을 설명할 수 있을 때 문서 가치가 커진다.
- 이후 포트폴리오에서도 exploit 설명은 raw payload보다 구조 도식과 검증 경로 중심이 더 안전하다.

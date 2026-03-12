# Historical Source Audit

이 문서는 초기 원본 자산이 현재 `Node-Backend-Architecture` 트랙으로 어떻게 재구성되었는지 기록한다. 현재 학습 진입점은 `study/` 아래 새 구조이며, 이 문서는 역사적 근거를 남기는 용도다.

## 재구성 원칙

- 언어, 런타임, HTTP 브리지를 앞에 추가해 초보 진입 장벽을 낮췄다.
- 비교 학습 가치가 큰 구간만 Express/NestJS 이중 레인을 유지했다.
- 운영성과 포트폴리오 표면은 applied 단계로 분리했다.

## 현재 판단

- 원본 자산은 문제 자료와 비교 학습 힌트로는 유효했다.
- 그러나 현재 공개 표면에서는 `문제 -> 답 -> 검증` 계약이 먼저 보여야 하므로 새로운 README와 카탈로그가 기준이 된다.
- 원본 출처 문자열과 상세 대응표는 [study/Node-Backend-Architecture/docs/source-provenance.md](../study/Node-Backend-Architecture/docs/source-provenance.md)에 모아 둔다.

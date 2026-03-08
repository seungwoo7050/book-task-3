# Migration Playbook

## Sequence

1. `legacy/` 자산을 읽기 전용 기준으로 둔다.
2. `study/`에 새 번호 체계와 상태 모델을 먼저 만든다.
3. 문제 명세와 구현 코드를 옮긴다.
4. README를 새 학습 목표와 검증 기준에 맞게 다시 쓴다.
5. Makefile과 실행 명령을 새 경로에 맞게 고친다.
6. `verified` 여부는 실제 명령 실행 결과로만 부여한다.

## Public vs Private

- tracked README/docs: 문제, 제약, 실행법, 상태, 학습 포인트
- `notion/`: 시행착오, 긴 디버그 로그, 개인 학습 메모

## Verification Rule

- 적어도 1개 build/run 명령과 1개 test 명령이 실제로 통과해야 `verified`
- 외부 인프라 의존이 큰 프로젝트는 `partial` 허용
- 한계와 필요한 로컬 환경은 README에 명시


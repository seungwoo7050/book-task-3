# 문제 프레이밍

## 이 프로젝트가 답하려는 질문

finding이 있다고 해서 항상 즉시 수정해야 하는 것은 아닙니다. 이 프로젝트는 허용된 위험, 일시적 예외, 보상 통제 같은
상황을 “무시”가 아니라 “관리” 대상으로 다루기 위해, 예외 생성/승인/증거 첨부/감사 이력을 모델링하는 것이 목표입니다.

## 실제 입력과 출력

입력:
- finding과 연결되는 scope 정보
- 예외 사유와 만료 기간
- 승인자 정보
- 증거 제목과 URI

출력:
- `ExceptionRecord`
- `Evidence`
- `AuditEvent`
- 특정 scope가 억제 상태인지에 대한 판단

## 강한 제약

- 저장소는 메모리 기반입니다.
- 역할 기반 접근 통제와 revoke 기능은 없습니다.
- 대신 append-only audit와 expiry 기반 suppression 로직은 분명해야 합니다.

## 완료로 보는 기준

- 예외 생성 후 승인되면 suppression이 `True`가 되어야 합니다.
- 시간이 지나 만료되면 suppression이 다시 `False`가 되어야 합니다.
- 증거 추가와 audit event append가 별도 경로로 남아야 합니다.

## 확인에 쓰는 근거

- 문제 설명: [../problem/README.md](../problem/README.md)
- 핵심 테스트: [../python/tests/test_manager.py](../python/tests/test_manager.py)
- 이전 배경 설명: [../notion-archive/essay.md](../notion-archive/essay.md)

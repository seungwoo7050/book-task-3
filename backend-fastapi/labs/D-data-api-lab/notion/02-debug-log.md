# 디버그 로그

## 실패 사례

초기에는 soft delete된 프로젝트에도 task가 생성되거나, 같은 version으로 두 번 업데이트했을 때 충돌이 제대로 드러나지 않는 문제가 있었다.

## 원인

- 삭제된 프로젝트를 조회할 때 `deleted_at` 경계를 같이 확인하지 않았다.
- version 증가 시점을 잘못 두면 stale update를 안정적으로 감지할 수 없다.

## 수정

- task 생성 전에 프로젝트 존재 여부와 soft delete 여부를 함께 확인하도록 정리했다.
- 업데이트 전에 version을 검증하고, 성공 경로에서 version 증가를 명시적으로 처리했다.

## 검증 근거

- stale update는 409를 반환하는 테스트로 확인한다.
- 이 실패는 soft delete와 version 충돌 규칙을 서비스 계층에서 명시적으로 관리해야 한다는 점을 보여 준다.

마지막 실제 실행 기록은 [../../../docs/verification-report.md](../../../docs/verification-report.md)를 따른다.

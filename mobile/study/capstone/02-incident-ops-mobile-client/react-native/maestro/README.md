# Maestro Flows

이 디렉터리는 최종 클라이언트 수동/디바이스 검증용 flow를 보관한다.

- Bundle ID: `org.reactjs.native.example.IncidentOpsMobileClient`

- `01-portfolio-core.yaml`: reporter -> operator -> approver 승인 시나리오와 발표용 스크린샷 캡처
- `02-portfolio-outbox-recovery.yaml`: 잘못된 backend target을 이용한 outbox 장애/복구 시나리오 캡처
- `smoke-login-create.yaml`: 로그인 후 incident 생성
- `approval-review.yaml`: approval review 탭과 detail flow 검토

## Capture Command

```bash
export PATH="$PATH:$HOME/.maestro/bin"
maestro test maestro/01-portfolio-core.yaml \
  --device "<simulator-udid>" \
  --test-output-dir ../../docs/assets/portfolio
maestro test maestro/02-portfolio-outbox-recovery.yaml \
  --device "<simulator-udid>" \
  --test-output-dir ../../docs/assets/portfolio
```

# 디버그 로그

## 1. JWT validation gap과 token storage risk를 같은 시나리오에서 어떻게 다룰지

현실에서는 종종 같이 발생하지만, 학습용 fixture에서는 control ID를 명확히 보이게 하기 위해 어떤 시나리오는 한두 가지
finding만 반환하도록 단순화했습니다.

## 2. refresh rotation과 reuse detection은 분리해서 체크해야 했다

둘 다 refresh token과 관련 있지만, 하나는 발급 정책이고 다른 하나는 탈취 징후 감지라서 같은 boolean으로 합치면 설명력이 떨어집니다.


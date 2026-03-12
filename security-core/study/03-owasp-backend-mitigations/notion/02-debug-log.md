# 디버그 로그

## 1. SSRF는 allowlist와 private IP block을 같이 봐야 했다

둘 중 하나만 누락돼도 outbound request의 위험이 남기 때문에, evaluator는 둘을 하나의 control ID 아래에서 함께 점검합니다.

## 2. Broken access control은 “로그인 여부”가 아니라 “리소스 범위 검증”으로 정의해야 했다

auth 자체를 모델링하면 범위가 커지므로, 이 프로젝트는 ownership/scope enforcement 존재 여부만 평가합니다.


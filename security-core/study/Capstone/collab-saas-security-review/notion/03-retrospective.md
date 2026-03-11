# 회고

- capstone을 실제 서버로 키우지 않았기 때문에 foundations와 같은 실행 습관을 유지할 수 있었다.
- 이 구조는 "어떤 finding을 먼저 고칠까"를 설명하는 데 집중하게 만들고, DB나 worker 같은 부차적 복잡성을 피하게 해 준다.
- 이후 더 무거운 보안 프로젝트를 만든다면 이 capstone의 remediation board를 입력으로 다른 워크플로우를 추가하는 편이 자연스럽다.

## 남은 한계

- remediation board는 정렬과 설명을 제공하지만, 실제 team ownership이나 SLA는 아직 모델링하지 않는다.
- dependency triage는 bundle에 이미 영향 받는 advisory가 정리돼 있다는 가정 위에서만 동작한다.
- crypto category는 password KDF, MAC, key lifecycle까지만 다루고 nonce, AEAD, signature는 포함하지 않는다.

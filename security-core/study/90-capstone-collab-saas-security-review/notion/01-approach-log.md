# 접근 기록

## 선택한 방향

- 다른 레포의 capstone처럼 "앞선 학습 단위를 다시 조합한다"는 원칙은 유지한다.
- 다만 `security-core`는 foundation 전체가 CLI/fixture 중심이므로, capstone도 같은 질감을 유지했다.
- auth, backend, dependency는 기존 evaluator vocabulary를 동일하게 재구현하고, crypto만 capstone 전용 review 항목을 추가했다.
- review 결과를 사람이 읽는 queue로 바꾸기 위해 remediation board와 markdown report를 별도 산출물로 뒀다.

## 버린 방향

- FastAPI + DB를 붙이는 방식은 foundations와 결이 달라져서 버렸다.
- 앞선 프로젝트 패키지를 직접 import하는 방식은 capstone 자체의 설명력을 약하게 만들어 버렸다.
- live advisory API를 붙이는 방식은 재현성을 깨뜨리고 입력 provenance를 흐리므로 제외했다.

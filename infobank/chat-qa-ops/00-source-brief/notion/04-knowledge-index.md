# Source Brief — 지식 인덱스

## 핵심 개념

### 문서 중심 기획을 코드 계약으로 고정하기

프로젝트 초기에 "이건 뭘 만드는 프로젝트인가?"를 정할 때, 보통 README나 기획 문서에 자연어로 쓴다.
이 stage에서는 그 자연어를 **frozen dataclass**로 옮겨서, 테스트가 통과해야만 변경이 인정되도록 만들었다.
핵심 교훈: 문서는 읽히지만, 코드는 **실행되고 검증된다**.

### Baseline snapshot과 curriculum rationale의 분리

baseline(`v0-initial-demo`)은 "지금 결과물은 여기다"를 말하고, curriculum rationale은 "왜 이 순서로 학습하는가"를 말한다.
이 둘이 같은 문서에 섞이면 "현재 상태"와 "설계 이유"가 구분되지 않는다.
source brief는 이 둘을 `baseline_version`과 `REFERENCE_SPINE`으로 각각 분리한다.

### Reference spine을 stable navigation으로 유지하기

읽어야 할 문서를 5개로 제한한 것의 의미는 "이 5개만 읽으면 전체를 이해할 수 있다"는 약속이다.
spine이 10개, 20개로 늘어나면 navigation 역할을 잃는다.

## 참고 자료

### Reference Spine

- **경로**: `docs/reference-spine.md`
- **왜 읽었나**: source brief가 어떤 문서를 canonical source로 삼는지 확인하기 위해
- **배운 것**: 트랙 전체의 문제 정의와 제출 방향은 소수의 상위 문서에 집중되어 있었다
- **이후 영향**: stage 00에서 reference spine을 상수 목록으로 유지하도록 결정

### Project Selection Rationale

- **경로**: `docs/project-selection-rationale.md`
- **왜 읽었나**: 왜 상담 품질 관리 주제가 최종 capstone인지 확인하기 위해
- **배운 것**: 이 트랙은 상담 챗봇 기능보다 **평가와 운영 툴링**에 학습 초점이 있다
- **이후 영향**: source brief의 capstone goal을 "QA Ops 플랫폼"으로 고정

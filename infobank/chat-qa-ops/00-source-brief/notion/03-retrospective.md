# Source Brief — 회고: 첫 stage를 끝내고 나서

## 잘 된 것

### 후속 stage에서 참조할 baseline과 stack이 명확해졌다

이건 기대한 대로였다. stage 01에서 rubric을 설계할 때 "우리의 primary stack이 뭐지?"라고 묻지 않아도 됐다.
`build_source_brief().primary_stack`을 호출하면 답이 나온다.

### legacy 의도와 새 curriculum rationale이 같은 파일에서 연결됐다

`reference_spine`에 `legacy-intent-audit.md`와 `curriculum-map.md`를 함께 넣어서, "과거에 뭘 하려 했는지"와 "지금 뭘 하려는지"가 한 곳에서 읽힌다.

## 아쉬운 것

### 실행 시스템이 아니라 navigation contract라서 체감 기능이 적다

솔직히 이 stage를 끝내고 나면 "뭘 만든 건데?"라는 느낌이 든다.
화면에 보이는 게 없고, API가 뜨는 것도 아니다. 하지만 이 불편함은 의도적이다.
stage 00의 역할은 **방향을 잠그는 것**이지, 결과물을 보여주는 게 아니다.

### reference spine의 내용 품질은 별도 문서 관리에 의존한다

spine에 들어간 다섯 문서가 실제로 잘 쓰여 있는지는 이 stage에서 보장하지 않는다.
"어떤 문서를 보라"고 가리키는 것과, "그 문서가 좋다"는 것은 별개의 문제다.

## 나중에 다시 볼 것

- 만약 다른 study track(예: MCP 추천 최적화)이 추가되면, `SourceBrief` schema를 공통 모듈로 승격하는 것을 고려할 수 있다.
- 현재는 chat-qa-ops 전용이지만, 구조 자체는 범용적이다.

# msglab — 이 과제에서 남긴 지식

작성일: 2026-03-08

## 핵심 규칙 정리

### IRC line 구조

IRC 메시지 한 줄은 대략 이런 형태를 따른다:

```text
[:prefix] COMMAND [param] [param] [:trailing with spaces]
```

여기서 중요한 규칙이 하나 있다: **trailing parameter만 공백을 포함할 수 있다**. `:` 뒤에 오는 모든 텍스트는 공백을 포함한 하나의 parameter로 취급된다. 이 규칙을 모르면 `PRIVMSG #ch :hello world`에서 "hello"와 "world"가 별개 parameter로 분리될 수 있다.

### partial line 처리의 중요성

socket에서 한 번 `recv`를 했다고 항상 메시지 한 줄이 완성되는 것은 아니다. TCP는 byte stream이므로, 메시지가 여러 read에 걸쳐 올 수도 있고, 반대로 여러 메시지가 한 번의 read에 합쳐서 올 수도 있다.

따라서 parser는 **`\n`으로 끝나는 완전한 line만 소비하고, 마지막 incomplete fragment는 반드시 남겨야 한다.** 이 계약을 어기면 메시지 손실이 발생한다.

### command 대문자 정규화

IRC command는 case-insensitive하다. 하지만 매번 비교할 때 대소문자를 무시하는 것보다, **파싱 시점에 대문자로 정규화**하는 편이 dispatch를 단순하게 만든다. `msglab`의 `Message` 생성자는 command를 항상 대문자로 바꾼다.

## 이 과제에서 체화한 설계 원칙

- **prefix를 읽은 뒤 임시 상태를 반드시 초기화하라.** 이 실수 하나로 command 해석 전체가 깨질 수 있다. 눈으로만 읽으면 안 보이고, prefix가 있는 테스트 케이스를 돌려야 드러난다.
- **parser가 상위 런타임 상수에 과도하게 의존하면 독립 테스트가 어려워진다.** parser는 자기가 필요한 문법 규칙을 스스로 관리하는 편이 낫다.
- **validator는 parser layer에 두는 편이 좋다.** "왜 거절되었는지"를 가장 일찍 드러낼 수 있기 때문이다. 실행기(Executor)까지 가서야 invalid nickname을 발견하면 디버깅이 어려워진다.
- **테스트는 구조적 변형을 교차 검증해야 한다.** 정상 입력만 넣어보는 것으로는 parser의 edge case를 잡지 못한다.

## 참고 자료

| 자료 | 경로 | 왜 봤는가 | 무엇을 배웠는가 | 프로젝트에 어떤 영향을 줬는가 |
| --- | --- | --- | --- | --- |
| Legacy Message parser | `legacy/src/Message.cpp` | prefix/command/params 추출 순서 확인 | 레거시 구조의 장점과 버그 가능성을 동시에 봤다 | prefix parsing 버그를 찾는 기준이 되었다 |
| Legacy Parser helpers | `legacy/src/Parser.cpp` | frame split 방식과 helper 범위 확인 | parser가 너무 많은 계층을 끌어오고 있었다 | `msglab`에서 독립 parser로 단순화했다 |
| Message header | `legacy/src/inc/Message.hpp` | 데이터 모델 최소 범위 확인 | game 관련 필드는 parser lab에 불필요했다 | `Message`에서 lab 범위 밖 필드를 제거했다 |
| msglab tests | `study/msglab/cpp/tests/test_parser.cpp` | 실제 검증 범위 기록 | prefix, validator, partial line, transcript 커버리지에 arena helper 검증 추가 | knowledge index와 회고의 기준이 되었다 |

## 빠른 자가 점검 리스트

- [ ] prefix 뒤 임시 상태를 초기화했는가?
- [ ] trailing parameter가 손실되지 않는가?
- [ ] incomplete frame을 버리지 않는가?
- [ ] validator 규칙이 실행기보다 먼저 드러나도록 설계했는가?
- [ ] command 비교에 case 문제가 남아있지 않은가?

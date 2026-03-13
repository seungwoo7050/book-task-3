# msglab series map

이 시리즈는 `msglab`이 문자열 처리 보조 유틸이 아니라 독립된 parser boundary라는 점을 source-first로 다시 확인하기 위한 지도다.

## 이 프로젝트가 답하는 질문

- 줄 단위 입력을 메시지 frame으로 자르는 책임과 command validation 책임을 어디서 끊어야 할까
- IRC command와 arena command를 같은 parser surface에서 다루려면 무엇을 고정하고 무엇을 generic으로 남겨야 할까

## 읽는 순서

1. [10-chronology-message-model-and-framing.md](10-chronology-message-model-and-framing.md)
2. [20-chronology-validation-and-command-normalization.md](20-chronology-validation-and-command-normalization.md)
3. [30-chronology-transcript-coverage-and-boundaries.md](30-chronology-transcript-coverage-and-boundaries.md)

## 참조한 실제 파일

- `study/shared-core/02-msglab/README.md`
- `study/shared-core/02-msglab/problem/README.md`
- `study/shared-core/02-msglab/cpp/README.md`
- `study/shared-core/02-msglab/cpp/Makefile`
- `study/shared-core/02-msglab/cpp/include/inc/Message.hpp`
- `study/shared-core/02-msglab/cpp/include/inc/Parser.hpp`
- `study/shared-core/02-msglab/cpp/src/Message.cpp`
- `study/shared-core/02-msglab/cpp/src/Parser.cpp`
- `study/shared-core/02-msglab/cpp/tests/test_parser.cpp`
- `study/shared-core/02-msglab/docs/README.md`

## Canonical CLI

```bash
cd study/shared-core/02-msglab/cpp
make clean && make test
```

## Git Anchor

- `2026-03-09 73372bd Add project: backend-fastapi, backend-spring, cpp-server`
- `2026-03-10 7dc71a8 docs: enhance cpp-server`
- `2026-03-11 a9c65b3 Track 2에 대한 전반적인 개선 완료 (infobank, bithumb, game-server)`

## 추론 원칙

- 실제 commit은 parser 세부 단계까지 쪼개져 있지 않으므로 chronology는 `Message` 표면 -> `Parser` helper -> transcript test 확장 순서로 복원한다.
- `HELLO`, `INPUT`, `REJOIN` 같은 arena command는 "특수 label을 추가했다"가 아니라 "generic command token을 보존했다"는 관점으로 설명한다.


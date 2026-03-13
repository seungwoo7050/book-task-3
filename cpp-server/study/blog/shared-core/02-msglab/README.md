# msglab Source-First Blog

`msglab`은 network I/O를 잠시 옆으로 밀어 두고, 입력 경계만 따로 붙잡아 보는 lab이다. 여기서 풀고 싶은 문제는 "한 줄 메시지를 어디서 끊고, 무엇을 `Message`로 남기고, 어떤 검증을 parser 근처에서 끝낼 것인가"다. 이 바닥이 먼저 고정돼야 뒤쪽 IRC와 game server 문서에서도 문자열 처리 버그와 네트워크 버그를 섞어 보지 않게 된다.

이 시리즈 역시 근거는 문서 감각이 아니라 실제 흔적이다. [`problem/README.md`](../../../shared-core/02-msglab/problem/README.md), [`cpp/README.md`](../../../shared-core/02-msglab/cpp/README.md), [`docs/README.md`](../../../shared-core/02-msglab/docs/README.md), 실제 소스, 테스트, 직접 실행한 CLI만 사용했다. 저장 시각은 남아 있지 않아 chronology는 `Phase` 단위로 복원했지만, `Message` 모델과 `Parser` helper, transcript 테스트가 서로를 어떻게 요구하는지는 코드에서 그대로 드러난다.

## 검증 명령

```sh
cd /Users/woopinbell/work/book-task-3/cpp-server/study/shared-core/02-msglab/cpp
make clean && make test
```

최근 확인 결과:

- `./msglab_tests`
- `msglab parser tests passed.`

## 읽기 순서

- [00-series-map.md](00-series-map.md)
- [evidence-ledger.md](evidence-ledger.md)
- [structure-plan.md](structure-plan.md)
- [10-message-model-and-framing.md](10-message-model-and-framing.md)
- [20-validation-and-command-normalization.md](20-validation-and-command-normalization.md)
- [30-transcript-coverage-and-boundaries.md](30-transcript-coverage-and-boundaries.md)

## 핵심 근거 파일

- [`cpp/include/inc/Message.hpp`](../../../shared-core/02-msglab/cpp/include/inc/Message.hpp)
- [`cpp/include/inc/Parser.hpp`](../../../shared-core/02-msglab/cpp/include/inc/Parser.hpp)
- [`cpp/src/Message.cpp`](../../../shared-core/02-msglab/cpp/src/Message.cpp)
- [`cpp/src/Parser.cpp`](../../../shared-core/02-msglab/cpp/src/Parser.cpp)
- [`cpp/tests/test_parser.cpp`](../../../shared-core/02-msglab/cpp/tests/test_parser.cpp)

